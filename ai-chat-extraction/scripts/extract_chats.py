#!/usr/bin/env python3
"""
extract_chats.py — Universal AI chat export → Obsidian vault extractor.

Turns official data exports from ChatGPT, Claude, Gemini (Google Takeout),
and generic chat files into one clean Markdown note per conversation, with
YAML frontmatter, filed under  <vault>/raw/conversations/<platform>/<year>/.

This is the "raw layer" of the karpathian extraction structure:
raw (immutable) → wiki (LLM-maintained) → schema (CLAUDE.md).

Usage:
    python3 extract_chats.py --source chatgpt --input ~/Downloads/chatgpt-export.zip --vault ~/Vault
    python3 extract_chats.py --source claude  --input ~/Downloads/claude-export.zip  --vault ~/Vault
    python3 extract_chats.py --source gemini  --input ~/Takeout/MyActivity.json      --vault ~/Vault
    python3 extract_chats.py --source generic --input ~/old-chats-folder/            --vault ~/Vault
    python3 extract_chats.py --source auto    --input <anything above>               --vault ~/Vault

No third-party dependencies — Python 3.9+ standard library only.
"""

import argparse
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROLE_LABELS = {
    "user": "🧑 You",
    "human": "🧑 You",
    "assistant": "🤖 Assistant",
    "system": "⚙️ System",
    "tool": "🔧 Tool",
}

PLATFORM_NAMES = {
    "chatgpt": "ChatGPT",
    "claude": "Claude",
    "gemini": "Gemini",
    "grok": "Grok",
    "perplexity": "Perplexity",
    "copilot": "Copilot",
    "generic": "Other",
}


# ---------------------------------------------------------------- helpers

def slugify(title: str, max_len: int = 60) -> str:
    """Filesystem-safe, human-readable slug for filenames."""
    title = (title or "Untitled").strip()
    title = re.sub(r'[<>:"/\\|?*\[\]#^]', "", title)
    title = re.sub(r"\s+", " ", title).strip()
    if len(title) > max_len:
        title = title[:max_len].rsplit(" ", 1)[0]
    return title or "Untitled"


def ts_to_date(ts) -> str:
    """Epoch float/int or ISO string → YYYY-MM-DD (UTC)."""
    if ts is None:
        return "unknown-date"
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
        s = str(ts).replace("Z", "+00:00")
        return datetime.fromisoformat(s).strftime("%Y-%m-%d")
    except (ValueError, OSError, OverflowError):
        return "unknown-date"


def yaml_escape(s: str) -> str:
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def read_json_from(path: Path, inner_name: str):
    """Read a JSON file directly, or find it inside an export .zip."""
    if path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as zf:
            candidates = [n for n in zf.namelist() if n.endswith(inner_name)]
            if not candidates:
                raise FileNotFoundError(f"{inner_name} not found inside {path.name}")
            with zf.open(candidates[0]) as f:
                return json.load(f)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- parsers
# Each parser yields dicts:
#   {id, title, created, updated, messages: [{role, text, time}]}

def parse_chatgpt(path: Path):
    """OpenAI export: conversations.json — a tree in `mapping`, linearized by
    backtracking from `current_node` to the root (the branch you last used)."""
    data = read_json_from(path, "conversations.json")
    for conv in data:
        mapping = conv.get("mapping") or {}
        node_id = conv.get("current_node")
        # walk current_node → root, then reverse
        chain = []
        seen = set()
        while node_id and node_id in mapping and node_id not in seen:
            seen.add(node_id)
            node = mapping[node_id]
            msg = node.get("message")
            if msg:
                chain.append(msg)
            node_id = node.get("parent")
        chain.reverse()

        messages = []
        for msg in chain:
            role = (msg.get("author") or {}).get("role", "unknown")
            if role == "system":
                continue  # hidden system scaffolding — never user content
            text = _chatgpt_content_to_text(msg.get("content") or {})
            if not text.strip():
                continue
            messages.append({
                "role": role,
                "text": text,
                "time": msg.get("create_time"),
            })
        if not messages:
            continue
        yield {
            "id": conv.get("conversation_id") or conv.get("id") or "",
            "title": conv.get("title") or "Untitled",
            "created": conv.get("create_time"),
            "updated": conv.get("update_time"),
            "messages": messages,
        }


def _chatgpt_content_to_text(content: dict) -> str:
    ctype = content.get("content_type", "text")
    parts = content.get("parts") or []
    if ctype == "text":
        return "\n\n".join(p for p in parts if isinstance(p, str))
    if ctype == "code":
        lang = content.get("language") or ""
        return f"```{lang}\n{content.get('text', '')}\n```"
    if ctype == "execution_output":
        return f"```\n{content.get('text', '')}\n```"
    if ctype == "multimodal_text":
        chunks = []
        for p in parts:
            if isinstance(p, str):
                chunks.append(p)
            elif isinstance(p, dict):
                if p.get("content_type") == "image_asset_pointer":
                    chunks.append("*[image attached — not included in export text]*")
                elif "text" in p:
                    chunks.append(str(p["text"]))
        return "\n\n".join(chunks)
    if ctype in ("thoughts", "reasoning_recap", "user_editable_context",
                 "model_editable_context", "tether_browsing_display"):
        return ""  # internal scaffolding, skip
    # unknown types: best effort
    if parts:
        return "\n\n".join(str(p) for p in parts if isinstance(p, str))
    return content.get("text", "") or ""


def parse_claude(path: Path):
    """Anthropic export: conversations.json — flat list, `chat_messages` array."""
    data = read_json_from(path, "conversations.json")
    for conv in data:
        messages = []
        for msg in conv.get("chat_messages") or []:
            # newer exports use content blocks; older ones a plain `text` field
            blocks = msg.get("content") or []
            text = "\n\n".join(
                b.get("text", "") for b in blocks
                if isinstance(b, dict) and b.get("type") == "text"
            ) or msg.get("text", "")
            if not text.strip():
                continue
            messages.append({
                "role": msg.get("sender", "unknown"),
                "text": text,
                "time": msg.get("created_at"),
            })
        if not messages:
            continue
        yield {
            "id": conv.get("uuid", ""),
            "title": conv.get("name") or "Untitled",
            "created": conv.get("created_at"),
            "updated": conv.get("updated_at"),
            "messages": messages,
        }


def parse_gemini(path: Path):
    """Google Takeout → My Activity → Gemini Apps → MyActivity.json.
    Takeout logs your prompts (and sometimes responses) as activity records,
    not full transcripts — one note per day is the most useful shape."""
    data = read_json_from(path, ".json")
    by_day = {}
    for rec in data:
        title = rec.get("title", "")
        time = rec.get("time")
        day = ts_to_date(time)
        prompt = re.sub(r"^Prompted\s+", "", title).strip()
        if not prompt:
            continue
        msgs = by_day.setdefault(day, [])
        msgs.append({"role": "user", "text": prompt, "time": time})
        for sub in rec.get("subtitles") or []:
            name = sub.get("name", "")
            if name and not name.startswith(("Watched", "Visited")):
                msgs.append({"role": "assistant", "text": name, "time": time})
    for day, messages in sorted(by_day.items()):
        yield {
            "id": f"gemini-{day}",
            "title": f"Gemini activity {day}",
            "created": messages[0]["time"] if messages else None,
            "updated": messages[-1]["time"] if messages else None,
            "messages": messages,
        }


def parse_generic(path: Path):
    """Fallback: a folder (or single file) of .md / .txt / .json chat files.
    Each file becomes one conversation note, content passed through as-is.
    Use for platforms without structured exports (Perplexity thread copies,
    Grok saves, Copilot pastes, browser-extension dumps...)."""
    files = [path] if path.is_file() else sorted(
        p for p in path.rglob("*") if p.suffix.lower() in (".md", ".txt", ".json")
    )
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if not text.strip():
            continue
        mtime = f.stat().st_mtime
        yield {
            "id": f.stem,
            "title": f.stem.replace("_", " ").replace("-", " ").strip(),
            "created": mtime,
            "updated": mtime,
            "messages": [{"role": "assistant", "text": text, "time": mtime}],
        }


PARSERS = {
    "chatgpt": parse_chatgpt,
    "claude": parse_claude,
    "gemini": parse_gemini,
    "generic": parse_generic,
}


def detect_source(path: Path) -> str:
    """Best-effort sniffing for --source auto."""
    try:
        if path.is_dir():
            return "generic"
        if path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
            if any("users.json" in n or "projects.json" in n for n in names):
                return "claude"
            return "chatgpt"
        data = read_json_from(path, ".json")
        if isinstance(data, list) and data:
            first = data[0]
            if "mapping" in first:
                return "chatgpt"
            if "chat_messages" in first:
                return "claude"
            if "header" in first and "Gemini" in str(first.get("header", "")):
                return "gemini"
            if "title" in first and "time" in first:
                return "gemini"
    except (OSError, json.JSONDecodeError, zipfile.BadZipFile):
        pass
    return "generic"


# ---------------------------------------------------------------- writer

def write_note(conv: dict, platform: str, out_root: Path, overwrite: bool) -> str:
    """Render one conversation to Markdown. Returns 'written'|'skipped'."""
    date = ts_to_date(conv["created"])
    year = date[:4] if date != "unknown-date" else "undated"
    short_id = re.sub(r"[^A-Za-z0-9]", "", str(conv["id"]))[:8] or "noid"
    slug = slugify(conv["title"])
    out_dir = out_root / platform / year
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{date} {slug} ({short_id}).md"
    if out_path.exists() and not overwrite:
        return "skipped"

    platform_name = PLATFORM_NAMES.get(platform, platform.title())
    n = len(conv["messages"])
    lines = [
        "---",
        "type: conversation",
        f"platform: {platform}",
        f"title: {yaml_escape(conv['title'])}",
        f"date: {date}",
        f"updated: {ts_to_date(conv['updated'])}",
        f"conversation_id: {yaml_escape(conv['id'])}",
        f"message_count: {n}",
        "tags: [ai-chat, raw]",
        "distilled: false",
        "notion_synced: false",
        "last_resurfaced: never",
        "---",
        "",
        f"# {conv['title']}",
        "",
        f"> **{platform_name}** · {date} · {n} messages · id `{short_id}`",
        "",
        "---",
        "",
    ]
    for msg in conv["messages"]:
        label = ROLE_LABELS.get(msg["role"], f"❓ {msg['role']}")
        lines.append(f"## {label}")
        lines.append("")
        lines.append(msg["text"].strip())
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return "written"


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--source", default="auto", choices=["auto", *PARSERS.keys()],
                    help="Export format (default: auto-detect)")
    ap.add_argument("--input", required=True, help="Export file/zip/folder")
    ap.add_argument("--vault", required=True, help="Obsidian vault root")
    ap.add_argument("--outdir", default="raw/conversations",
                    help="Output folder inside vault (default: raw/conversations)")
    ap.add_argument("--platform-label", default=None,
                    help="Override platform folder name for --source generic "
                         "(e.g. perplexity, grok, copilot)")
    ap.add_argument("--overwrite", action="store_true",
                    help="Re-write notes that already exist")
    args = ap.parse_args()

    in_path = Path(args.input).expanduser()
    if not in_path.exists():
        sys.exit(f"ERROR: input not found: {in_path}")

    source = args.source if args.source != "auto" else detect_source(in_path)
    platform = args.platform_label or source
    out_root = Path(args.vault).expanduser() / args.outdir

    print(f"→ source={source}  platform folder={platform}")
    print(f"→ writing to {out_root / platform}/")

    written = skipped = failed = 0
    for conv in PARSERS[source](in_path):
        try:
            result = write_note(conv, platform, out_root, args.overwrite)
            if result == "written":
                written += 1
            else:
                skipped += 1
        except Exception as e:  # one bad conversation must never kill the run
            failed += 1
            print(f"  ! failed: {conv.get('title', '?')[:50]} — {e}", file=sys.stderr)

    print(f"✓ done: {written} written, {skipped} already existed, {failed} failed")
    if written:
        print("  Next step: open the vault in Obsidian, then run distill_wiki.py "
              "(or `claude` inside the vault) to build the wiki layer.")


if __name__ == "__main__":
    main()
