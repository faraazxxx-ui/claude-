#!/usr/bin/env python3
"""Export the full contents of this repository plus the output of every Claude
Code chat session that has run against it, into one Markdown file and one JSON
file.

What counts as a "chat session": every Claude Code / Copilot session on this
repo runs on its own branch and (usually) opens a pull request. So each non-default
remote branch is treated as one session, and its outputs are the files that branch
added or changed relative to its merge-base with the default branch. Sessions whose
work was already merged are listed with their commits; their file contents live in
the repository snapshot.

Usage:
    python3 tools/export_repo_and_chats.py \
        --out-dir export \
        --prs /path/to/pull_requests.json \
        --transcript-dir ~/.claude/projects/-home-user-claude-

Both --prs and --transcript-dir are optional; the export degrades gracefully
without them (git data alone is enough for a complete file export).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# git helpers
# ---------------------------------------------------------------------------

TEXT_MAX_BYTES = 8 * 1024 * 1024  # refuse to inline anything wildly large

EXT_LANG = {
    ".py": "python", ".js": "javascript", ".jsx": "jsx", ".ts": "typescript",
    ".tsx": "tsx", ".json": "json", ".md": "markdown", ".markdown": "markdown",
    ".html": "html", ".htm": "html", ".css": "css", ".scss": "scss",
    ".sh": "bash", ".bash": "bash", ".zsh": "bash", ".yml": "yaml",
    ".yaml": "yaml", ".toml": "toml", ".ini": "ini", ".cfg": "ini",
    ".csv": "csv", ".tsv": "tsv", ".sql": "sql", ".txt": "text",
    ".xml": "xml", ".svg": "xml", ".rb": "ruby", ".go": "go", ".rs": "rust",
    ".java": "java", ".c": "c", ".h": "c", ".cpp": "cpp", ".hpp": "cpp",
    ".gitignore": "text", ".env": "text",
}


def git(*args: str, binary: bool = False, check: bool = True):
    """Run a git command, returning stdout as text (or bytes if binary)."""
    proc = subprocess.run(
        ["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode('utf-8', 'replace')[:400]}"
        )
    if proc.returncode != 0:
        return None
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


def language_for(path: str) -> str:
    return EXT_LANG.get(os.path.splitext(path)[1].lower(), "")


def looks_binary(blob: bytes) -> bool:
    if b"\0" in blob[:8192]:
        return True
    try:
        blob.decode("utf-8")
    except UnicodeDecodeError:
        return True
    return False


def describe_blob(path: str, blob: bytes, blob_sha: str = "") -> dict:
    """Build the per-file record used by both the JSON and Markdown outputs."""
    rec = {
        "path": path,
        "size_bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
        "git_blob_sha": blob_sha,
        "language": language_for(path),
    }
    if looks_binary(blob):
        rec.update(kind="binary", content=None, lines=None)
    elif len(blob) > TEXT_MAX_BYTES:
        rec.update(kind="oversized-text", content=None, lines=None)
    else:
        text = blob.decode("utf-8", "replace")
        rec.update(kind="text", content=text, lines=text.count("\n") + 1)
    return rec


def list_tree(ref: str) -> list[tuple[str, str]]:
    """Return [(blob_sha, path)] for every file in ref, recursively."""
    raw = git("ls-tree", "-r", "-z", ref)
    entries = []
    for entry in raw.split("\0"):
        if not entry:
            continue
        meta, path = entry.split("\t", 1)
        _mode, obj_type, obj_sha = meta.split()
        if obj_type == "blob":
            entries.append((obj_sha, path))
    return sorted(entries, key=lambda e: e[1])


def read_blob(ref: str, path: str) -> bytes | None:
    return git("show", f"{ref}:{path}", binary=True, check=False)


def commits_for(rng: str) -> list[dict]:
    """Parse `git log` for a revision range into structured records."""
    sep, fsep = "\x1e", "\x1f"
    fmt = fsep.join(["%H", "%h", "%an", "%ae", "%aI", "%cI", "%s", "%b"]) + sep
    raw = git("log", f"--format={fmt}", rng, check=False) or ""
    out = []
    for chunk in raw.split(sep):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        parts = chunk.split(fsep)
        if len(parts) < 8:
            continue
        out.append({
            "sha": parts[0], "short_sha": parts[1],
            "author_name": parts[2], "author_email": parts[3],
            "authored_at": parts[4], "committed_at": parts[5],
            "subject": parts[6], "body": parts[7].strip(),
        })
    return out


# ---------------------------------------------------------------------------
# chat-session assembly
# ---------------------------------------------------------------------------

SESSION_SLUG_RE = re.compile(r"^(claude|copilot)/(?P<slug>.+)$")


def session_agent(branch_ref: str) -> str:
    short = branch_ref.split("/", 1)[1] if "/" in branch_ref else branch_ref
    if short.startswith("claude/"):
        return "Claude Code"
    if short.startswith("copilot/"):
        return "GitHub Copilot"
    return "unknown"


def collect_sessions(default_ref: str, prs_by_head: dict) -> list[dict]:
    refs = [
        r for r in (git("for-each-ref", "--format=%(refname:short)",
                        "refs/remotes/origin") or "").split()
        if r != default_ref and not r.endswith("/HEAD")
    ]
    sessions = []
    for ref in sorted(refs):
        branch = ref.split("/", 1)[1]
        base = (git("merge-base", default_ref, ref, check=False) or "").strip()
        commits = commits_for(f"{default_ref}..{ref}") if base else []
        merged = not commits

        changed = []
        if base:
            raw = git("diff", "--name-status", "-z", base, ref, check=False) or ""
            tokens = [t for t in raw.split("\0") if t]
            i = 0
            while i < len(tokens):
                status = tokens[i]
                if status.startswith(("R", "C")) and i + 2 < len(tokens):
                    changed.append((status, tokens[i + 2]))
                    i += 3
                elif i + 1 < len(tokens):
                    changed.append((status, tokens[i + 1]))
                    i += 2
                else:
                    break

        outputs = []
        for status, path in changed:
            blob = read_blob(ref, path)
            if blob is None:  # deleted on this branch
                outputs.append({
                    "path": path, "change_status": status, "kind": "deleted",
                    "size_bytes": 0, "sha256": None, "git_blob_sha": "",
                    "language": language_for(path), "content": None, "lines": None,
                })
                continue
            rec = describe_blob(path, blob)
            rec["change_status"] = status
            outputs.append(rec)

        pr = prs_by_head.get(branch)
        m = SESSION_SLUG_RE.match(branch)
        sessions.append({
            "branch": branch,
            "remote_ref": ref,
            "agent": session_agent(ref),
            "session_slug": m.group("slug") if m else branch,
            "tip_commit": (git("rev-parse", ref) or "").strip(),
            "merge_base": base,
            "work_merged_into_default": merged,
            "commit_count": len(commits),
            "commits": commits,
            "pull_request": pr,
            "output_file_count": len(outputs),
            "output_text_bytes": sum(o["size_bytes"] for o in outputs
                                     if o["kind"] == "text"),
            "outputs": outputs,
        })
    return sessions


# ---------------------------------------------------------------------------
# live transcript
# ---------------------------------------------------------------------------

# harness bookkeeping, not conversation content
SKIP_ATTACHMENT_TYPES = {
    "deferred_tools_delta", "agent_listing_delta", "mcp_instructions_delta",
    "skill_listing", "task_reminder",
}


def _stringify(value, limit: int = 0) -> str:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, indent=1, ensure_ascii=False, default=str)
    if limit and len(text) > limit:
        text = text[:limit] + f"\n... [truncated, {len(text)} chars total]"
    return text


def parse_transcript(path: str) -> dict:
    """Turn a Claude Code .jsonl transcript into an ordered message list."""
    meta, messages, prompts = {}, [], []
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            for key in ("sessionId", "cwd", "version", "gitBranch", "entrypoint"):
                if rec.get(key) and key not in meta:
                    meta[key] = rec[key]

            rtype = rec.get("type")
            if rtype == "queue-operation":
                if rec.get("operation") == "enqueue" and rec.get("content"):
                    prompts.append({"timestamp": rec.get("timestamp"),
                                    "text": rec["content"]})
                continue
            if rtype == "attachment":
                atype = (rec.get("attachment") or {}).get("type")
                if atype in SKIP_ATTACHMENT_TYPES:
                    continue
                messages.append({
                    "index": len(messages), "line": lineno, "role": "system",
                    "kind": "attachment", "attachment_type": atype,
                    "timestamp": rec.get("timestamp"),
                    "blocks": [{"type": "attachment",
                                "value": rec.get("attachment")}],
                })
                continue

            msg = rec.get("message")
            if not isinstance(msg, dict):
                continue

            content = msg.get("content")
            blocks = []
            if isinstance(content, str):
                blocks.append({"type": "text", "text": content})
            else:
                for blk in content or []:
                    if not isinstance(blk, dict):
                        blocks.append({"type": "text", "text": str(blk)})
                        continue
                    btype = blk.get("type")
                    if btype == "text":
                        blocks.append({"type": "text", "text": blk.get("text", "")})
                    elif btype == "thinking":
                        blocks.append({"type": "thinking",
                                       "text": blk.get("thinking", "")})
                    elif btype == "tool_use":
                        blocks.append({"type": "tool_use", "id": blk.get("id"),
                                       "name": blk.get("name"),
                                       "input": blk.get("input")})
                    elif btype == "tool_result":
                        blocks.append({"type": "tool_result",
                                       "tool_use_id": blk.get("tool_use_id"),
                                       "is_error": bool(blk.get("is_error")),
                                       "content": blk.get("content")})
                    else:
                        blocks.append({"type": btype or "unknown", "value": blk})

            if not blocks:
                continue
            messages.append({
                "index": len(messages), "line": lineno,
                "role": msg.get("role"), "kind": rtype,
                "model": msg.get("model"), "timestamp": rec.get("timestamp"),
                "uuid": rec.get("uuid"), "blocks": blocks,
            })

    return {
        "transcript_file": os.path.basename(path),
        "session_id": meta.get("sessionId"),
        "cwd": meta.get("cwd"),
        "claude_code_version": meta.get("version"),
        "git_branch": meta.get("gitBranch"),
        "user_prompts": prompts,
        "message_count": len(messages),
        "messages": messages,
    }


# ---------------------------------------------------------------------------
# markdown rendering
# ---------------------------------------------------------------------------

def fence_for(text: str) -> str:
    """Pick a fence longer than any backtick run inside `text`."""
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def code_block(text: str, lang: str = "") -> str:
    fence = fence_for(text)
    body = text if text.endswith("\n") else text + "\n"
    return f"{fence}{lang}\n{body}{fence}\n"


def anchor(text: str) -> str:
    slug = re.sub(r"[^a-z0-9\s-]", "", text.lower()).strip()
    return re.sub(r"\s+", "-", slug)


def human_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.2f} MB"


def render_file_record(rec: dict, heading_level: int = 4) -> list[str]:
    h = "#" * heading_level
    out = [f"{h} `{rec['path']}`", ""]
    facts = [f"**Size:** {human_bytes(rec['size_bytes'])}"]
    if rec.get("lines"):
        facts.append(f"**Lines:** {rec['lines']}")
    if rec.get("change_status"):
        facts.append(f"**Change:** `{rec['change_status']}`")
    if rec.get("sha256"):
        facts.append(f"**SHA-256:** `{rec['sha256'][:16]}…`")
    out += [" · ".join(facts), ""]

    if rec["kind"] == "text":
        out.append(code_block(rec["content"], rec["language"]))
    elif rec["kind"] == "binary":
        out.append(
            "> Binary asset — content not inlined. Retrieve with "
            f"`git show <ref>:{rec['path']}`.\n"
        )
    elif rec["kind"] == "deleted":
        out.append("> Deleted on this branch.\n")
    else:
        out.append("> Text file exceeds the inline size limit; see repository.\n")
    out.append("")
    return out


def render_transcript_blocks(msg: dict, tool_result_limit: int) -> list[str]:
    out = []
    for blk in msg["blocks"]:
        btype = blk["type"]
        if btype == "text":
            out += [blk["text"].strip(), ""]
        elif btype == "thinking":
            out += ["<details><summary>Reasoning</summary>", "",
                    code_block(blk["text"].strip(), "text"),
                    "</details>", ""]
        elif btype == "tool_use":
            out += [f"**Tool call — `{blk.get('name')}`**", "",
                    code_block(_stringify(blk.get("input"), 4000), "json")]
        elif btype == "tool_result":
            label = "Tool result (error)" if blk.get("is_error") else "Tool result"
            out += [f"<details><summary>{label}</summary>", "",
                    code_block(_stringify(blk.get("content"), tool_result_limit),
                               "text"),
                    "</details>", ""]
        elif btype == "attachment":
            out += [f"<details><summary>Attachment</summary>", "",
                    code_block(_stringify(blk.get("value"), 2000), "json"),
                    "</details>", ""]
    return out


def render_markdown(data: dict, tool_result_limit: int) -> str:
    exp, stats = data["export"], data["statistics"]
    snap = data["repository_snapshot"]
    L: list[str] = []

    L += [
        f"# Repository & Chat Export — `{exp['repository']}`", "",
        f"Complete export of the `{snap['branch']}` branch plus the output of every "
        "Claude Code / Copilot chat session recorded against this repository.", "",
        "| | |", "|---|---|",
        f"| Repository | [{exp['repository']}]({exp['repository_url']}) |",
        f"| Visibility | **{exp['visibility']}** |",
        f"| Default branch | `{snap['branch']}` @ `{snap['commit'][:10]}` |",
        f"| Generated | {exp['generated_at']} |",
        f"| Generated by | {exp['generator']} |",
        "",
        "## Contents at a glance", "",
        "| Metric | Count |", "|---|---:|",
        f"| Files on `{snap['branch']}` | {stats['snapshot_file_count']} |",
        f"| — text files inlined in full | {stats['snapshot_text_files']} |",
        f"| — binary assets (manifested) | {stats['snapshot_binary_files']} |",
        f"| Text inlined from snapshot | {human_bytes(stats['snapshot_text_bytes'])} |",
        f"| Chat sessions (branches) | {stats['session_count']} |",
        f"| — with an open/closed pull request | {stats['sessions_with_pr']} |",
        f"| — work already merged to `{snap['branch']}` | {stats['sessions_merged']} |",
        f"| Session output files | {stats['session_output_files']} |",
        f"| Text inlined from sessions | {human_bytes(stats['session_output_bytes'])} |",
        f"| Commits in history | {stats['commit_count']} |",
        f"| Pull requests | {stats['pr_count']} |",
        "",
        "## Sections", "",
        "1. [Part 1 — Repository snapshot](#part-1--repository-snapshot)",
        "2. [Part 2 — Chat session outputs](#part-2--chat-session-outputs)",
        "3. [Part 3 — Live session transcript](#part-3--live-session-transcript)",
        "4. [Part 4 — Commit history](#part-4--commit-history)",
        "5. [Part 5 — Pull request index](#part-5--pull-request-index)",
        "",
        "> **Note on binary assets.** Charts (`.png`) and the PowerPoint deck are "
        "listed with size and SHA-256 but not base64-inlined, to keep this export "
        "readable and diffable. They remain in the repository at the paths shown.",
        "",
        "---", "",
    ]

    # ---------------- Part 1 ----------------
    L += [f"# Part 1 — Repository snapshot", "",
          f"Branch `{snap['branch']}` at commit `{snap['commit']}`.", ""]

    by_dir: dict[str, list[dict]] = {}
    for rec in snap["files"]:
        by_dir.setdefault(os.path.dirname(rec["path"]) or "(repository root)",
                          []).append(rec)

    L += ["## 1.1 File inventory", "",
          "| Directory | Files | Text | Binary | Size |",
          "|---|---:|---:|---:|---:|"]
    for d in sorted(by_dir):
        recs = by_dir[d]
        L.append(
            f"| `{d}` | {len(recs)} "
            f"| {sum(1 for r in recs if r['kind'] == 'text')} "
            f"| {sum(1 for r in recs if r['kind'] == 'binary')} "
            f"| {human_bytes(sum(r['size_bytes'] for r in recs))} |"
        )
    L += ["", "## 1.2 File contents", ""]

    for d in sorted(by_dir):
        L += [f"### {d}", ""]
        for rec in sorted(by_dir[d], key=lambda r: r["path"]):
            L += render_file_record(rec, heading_level=4)

    binaries = [r for r in snap["files"] if r["kind"] == "binary"]
    L += ["## 1.3 Binary asset manifest", ""]
    if binaries:
        L += ["| Path | Size | SHA-256 |", "|---|---:|---|"]
        for r in sorted(binaries, key=lambda r: -r["size_bytes"]):
            L.append(f"| `{r['path']}` | {human_bytes(r['size_bytes'])} "
                     f"| `{r['sha256']}` |")
    else:
        L.append("_No binary assets._")
    L += ["", "---", ""]

    # ---------------- Part 2 ----------------
    sessions = data["chat_sessions"]
    L += ["# Part 2 — Chat session outputs", "",
          "Each branch below is one agent chat session against this repository. "
          "Outputs are the files that session added or changed, reproduced in full.",
          "", "## 2.1 Session index", "",
          "| # | Session branch | Agent | PR | State | Commits | Output files |",
          "|---:|---|---|---:|---|---:|---:|"]
    for i, s in enumerate(sessions, 1):
        pr = s.get("pull_request") or {}
        prnum = f"[#{pr['number']}]({pr['html_url']})" if pr else "—"
        if pr:
            state = "merged" if pr.get("merged") else (pr.get("state") or "?")
        else:
            state = "merged" if s["work_merged_into_default"] else "branch only"
        L.append(
            f"| {i} | [`{s['branch']}`](#session-{i}-{anchor(s['branch'])}) "
            f"| {s['agent']} | {prnum} | {state} "
            f"| {s['commit_count']} | {s['output_file_count']} |"
        )
    L += [""]

    for i, s in enumerate(sessions, 1):
        pr = s.get("pull_request") or {}
        L += [f"## Session {i} — `{s['branch']}`", "",
              "| | |", "|---|---|",
              f"| Agent | {s['agent']} |",
              f"| Tip commit | `{s['tip_commit'][:12]}` |",
              f"| Merge base | `{(s['merge_base'] or '')[:12]}` |",
              f"| Unmerged commits | {s['commit_count']} |",
              f"| Output files | {s['output_file_count']} |"]
        if pr:
            L += [f"| Pull request | [#{pr['number']}]({pr['html_url']}) — "
                  f"{pr.get('title', '')} |",
                  f"| PR state | {'merged' if pr.get('merged') else pr.get('state')} |",
                  f"| Opened | {(pr.get('created_at') or '')[:10]} |"]
            if pr.get("additions") is not None:
                L.append(f"| Diff | +{pr.get('additions')} / "
                         f"−{pr.get('deletions')} across "
                         f"{pr.get('changed_files')} files |")
        L += [""]

        if pr.get("body"):
            L += ["### Session summary (pull request description)", "",
                  pr["body"].strip(), ""]

        if s["commits"]:
            L += ["### Commits", ""]
            for c in s["commits"]:
                L.append(f"- `{c['short_sha']}` {c['authored_at'][:10]} — "
                         f"{c['subject']} _({c['author_name']})_")
                if c["body"]:
                    for para in c["body"].splitlines():
                        if para.strip():
                            L.append(f"  > {para.strip()}")
            L += [""]
        elif s["work_merged_into_default"]:
            L += ["### Commits", "",
                  f"_This session's commits are already contained in "
                  f"`{snap['branch']}`; see Part 4._", ""]

        L += ["### Outputs", ""]
        if s["outputs"]:
            for rec in s["outputs"]:
                L += render_file_record(rec, heading_level=4)
        else:
            L += ["_No files differ from the merge base — the work was merged "
                  "and is present in Part 1._", ""]
        L += ["---", ""]

    # ---------------- Part 3 ----------------
    L += ["# Part 3 — Live session transcript", ""]
    tr = data.get("live_session_transcript")
    if not tr:
        L += ["_No Claude Code transcript was available in this environment._", ""]
    else:
        L += ["The chat session that produced this export.", "",
              "| | |", "|---|---|",
              f"| Session ID | `{tr.get('session_id')}` |",
              f"| Working directory | `{tr.get('cwd')}` |",
              f"| Branch | `{tr.get('git_branch')}` |",
              f"| Claude Code version | {tr.get('claude_code_version')} |",
              f"| Messages | {tr.get('message_count')} |", ""]
        if tr.get("user_prompts"):
            L += ["### User prompts", ""]
            for p in tr["user_prompts"]:
                L += [f"- `{(p.get('timestamp') or '')[:19]}` — {p['text']}"]
            L += [""]
        L += ["### Message log", ""]
        for msg in tr["messages"]:
            ts = (msg.get("timestamp") or "")[:19]
            role = (msg.get("role") or "?").upper()
            L += [f"#### [{msg['index']}] {role} · {ts}", ""]
            L += render_transcript_blocks(msg, tool_result_limit)
        L += ["---", ""]

    # ---------------- Part 4 ----------------
    L += ["# Part 4 — Commit history", "",
          f"All {len(data['commit_history'])} commits reachable from "
          f"`{snap['branch']}`, newest first.", "",
          "| Commit | Date | Author | Subject |", "|---|---|---|---|"]
    for c in data["commit_history"]:
        subject = c["subject"].replace("|", "\\|")
        L.append(f"| `{c['short_sha']}` | {c['authored_at'][:10]} "
                 f"| {c['author_name']} | {subject} |")
    L += ["", "---", ""]

    # ---------------- Part 5 ----------------
    prs = data["pull_requests"]
    L += ["# Part 5 — Pull request index", ""]
    if not prs:
        L += ["_No pull request metadata was supplied._", ""]
    else:
        L += ["| PR | State | Opened | Branch | Title |",
              "|---:|---|---|---|---|"]
        for pr in sorted(prs, key=lambda p: -p["number"]):
            state = "merged" if pr.get("merged") else (pr.get("state") or "?")
            head = (pr.get("head") or {}).get("ref", "")
            title = (pr.get("title") or "").replace("|", "\\|")
            L.append(f"| [#{pr['number']}]({pr.get('html_url', '')}) | {state} "
                     f"| {(pr.get('created_at') or '')[:10]} | `{head}` | {title} |")
        L += [""]
        for pr in sorted(prs, key=lambda p: -p["number"]):
            L += [f"## PR #{pr['number']} — {pr.get('title', '')}", "",
                  f"`{(pr.get('head') or {}).get('ref', '')}` → "
                  f"`{(pr.get('base') or {}).get('ref', '')}` · "
                  f"**{'merged' if pr.get('merged') else pr.get('state')}** · "
                  f"opened {(pr.get('created_at') or '')[:10]} · "
                  f"[view on GitHub]({pr.get('html_url', '')})", ""]
            if pr.get("body"):
                L += [pr["body"].strip(), ""]
            else:
                L += ["_No description._", ""]

    L += ["", f"_End of export — {exp['generated_at']}._", ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", default="export")
    ap.add_argument("--basename", default="REPO_AND_CHAT_EXPORT")
    ap.add_argument("--ref", default="origin/main",
                    help="ref to snapshot (default: origin/main)")
    ap.add_argument("--prs", help="path to a JSON array of pull request objects")
    ap.add_argument("--transcript-dir",
                    help="directory holding Claude Code .jsonl transcripts")
    ap.add_argument("--repository", default="", help="owner/name, for the header")
    ap.add_argument("--visibility", default="unknown")
    ap.add_argument("--tool-result-limit", type=int, default=4000,
                    help="max chars per tool result in the Markdown output "
                         "(JSON always keeps the full value)")
    args = ap.parse_args()

    ref = args.ref
    if git("rev-parse", "--verify", ref, check=False) is None:
        ref = "HEAD"
        print(f"warning: {args.ref} not found, snapshotting HEAD", file=sys.stderr)

    repository = args.repository
    if not repository:
        url = (git("remote", "get-url", "origin", check=False) or "").strip()
        m = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
        repository = m.group(1) if m else "unknown/unknown"

    # --- pull requests -----------------------------------------------------
    prs = []
    if args.prs and os.path.exists(args.prs):
        with open(args.prs, encoding="utf-8") as fh:
            prs = json.load(fh)
    prs_by_head = {(p.get("head") or {}).get("ref"): p for p in prs
                   if (p.get("head") or {}).get("ref")}

    # --- snapshot ----------------------------------------------------------
    print(f"snapshotting {ref} …", file=sys.stderr)
    files = []
    for blob_sha, path in list_tree(ref):
        blob = read_blob(ref, path)
        if blob is None:
            continue
        files.append(describe_blob(path, blob, blob_sha))

    snapshot = {
        "branch": ref.split("/", 1)[-1] if "/" in ref else ref,
        "ref": ref,
        "commit": (git("rev-parse", ref) or "").strip(),
        "file_count": len(files),
        "files": files,
    }

    # --- sessions ----------------------------------------------------------
    print("collecting chat sessions …", file=sys.stderr)
    sessions = collect_sessions(ref, prs_by_head)

    # --- transcript --------------------------------------------------------
    transcript = None
    if args.transcript_dir:
        tdir = os.path.expanduser(args.transcript_dir)
        cands = [os.path.join(tdir, f) for f in os.listdir(tdir)
                 if f.endswith(".jsonl")] if os.path.isdir(tdir) else []
        if cands:
            newest = max(cands, key=os.path.getmtime)
            print(f"parsing transcript {newest} …", file=sys.stderr)
            transcript = parse_transcript(newest)

    history = commits_for(ref)

    stats = {
        "snapshot_file_count": len(files),
        "snapshot_text_files": sum(1 for f in files if f["kind"] == "text"),
        "snapshot_binary_files": sum(1 for f in files if f["kind"] == "binary"),
        "snapshot_text_bytes": sum(f["size_bytes"] for f in files
                                   if f["kind"] == "text"),
        "snapshot_binary_bytes": sum(f["size_bytes"] for f in files
                                     if f["kind"] == "binary"),
        "session_count": len(sessions),
        "sessions_with_pr": sum(1 for s in sessions if s.get("pull_request")),
        "sessions_merged": sum(1 for s in sessions
                               if s["work_merged_into_default"]),
        "session_output_files": sum(s["output_file_count"] for s in sessions),
        "session_output_bytes": sum(s["output_text_bytes"] for s in sessions),
        "commit_count": len(history),
        "pr_count": len(prs),
        "transcript_message_count": (transcript or {}).get("message_count", 0),
    }

    data = {
        "export": {
            "generated_at": datetime.now(timezone.utc)
                            .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "generator": "tools/export_repo_and_chats.py",
            "repository": repository,
            "repository_url": f"https://github.com/{repository}",
            "visibility": args.visibility,
            "schema_version": 1,
        },
        "statistics": stats,
        "repository_snapshot": snapshot,
        "chat_sessions": sessions,
        "live_session_transcript": transcript,
        "commit_history": history,
        "pull_requests": prs,
    }

    os.makedirs(args.out_dir, exist_ok=True)
    json_path = os.path.join(args.out_dir, args.basename + ".json")
    md_path = os.path.join(args.out_dir, args.basename + ".md")

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(render_markdown(data, args.tool_result_limit))

    print(f"\nwrote {md_path}  ({human_bytes(os.path.getsize(md_path))})",
          file=sys.stderr)
    print(f"wrote {json_path} ({human_bytes(os.path.getsize(json_path))})",
          file=sys.stderr)
    print(json.dumps(stats, indent=1), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
