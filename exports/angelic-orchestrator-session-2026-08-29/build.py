#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders transcript.md, transcript.json, transcript.sql from data.py plus live
reads of the repo's artifact files. Run with: python3 build.py
Single source of truth = data.py + the live repo files it points at; this
script only renders, it never originates narrative content.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

REPO = "/home/user/claude-"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

ARTIFACT_DESCRIPTIONS = {
    "skills/voice-capture-setup/SKILL.md": "The corrected, verified voice-dictation setup skill (turn 2's main deliverable). Current version, post YAML fix (commit 34485e7).",
    "skills/voice-capture-setup/references/verified_facts.md": "Dated ledger: confirmed facts, corrected claims, explicitly-unverified items.",
    "skills/voice-capture-setup/references/sony_batch_pipeline.md": "Corrected Sony-recorder batch pipeline install steps (fixes the 3 broken shell commands in source_doc_sony_pipeline).",
    "spine/hub.md": "Gate 0 index and the five fixed orchestrator rules.",
    "spine/goal.md": "The current-push/done-condition/out-of-scope target. STATUS: UNSET as of this export.",
    "spine/verify.md": "The standing 10-line pass/fail rubric used in turn 5's grading pass.",
    "spine/progress.md": "Current state as of the last pass; append-only; now holds 3 dated blocks spanning turns 2, 5 and the external fb3bb92 commit.",
    "spine/telemetry.md": "One append-only line per session; 4 lines as of this export.",
    "spine/failure.md": "What went wrong and what would have caught it; 2 entries, both from 2026-08-29.",
    "spine/learnings.md": "What is now durably known; 5 entries, the last 2 added by a different session on 2026-11-12.",
}


def git_blob_info(relpath):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%H|%ai", "--", relpath],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout.strip()
        sha, date = out.split("|", 1)
        return {"last_commit": sha, "last_commit_date": date}
    except Exception as e:
        return {"last_commit": None, "last_commit_date": None, "error": str(e)}


def load_artifacts():
    items = []
    for rel in D.REPO_ARTIFACT_PATHS:
        full = os.path.join(REPO, rel)
        with open(full, "r", encoding="utf-8") as f:
            content = f.read()
        info = git_blob_info(rel)
        items.append({
            "path": rel,
            "description": ARTIFACT_DESCRIPTIONS.get(rel, ""),
            "content": content,
            "bytes": len(content.encode("utf-8")),
            "lines": content.count("\n") + 1,
            **info,
        })
    return items


def assemble():
    return {
        "meta": D.META,
        "commits": D.COMMITS,
        "turns": D.TURNS,
        "deltas": D.DELTAS,
        "thinking_comparison": D.THINKING_COMPARISON,
        "gate_grades": D.GATE_GRADES,
        "open_items": D.OPEN_ITEMS,
        "source_documents": [
            {"name": "source_doc_sony_pipeline", "origin": "uploaded file, auto-read via @-mention in turn 1", "content": D.SOURCE_DOC_SONY_PIPELINE},
            {"name": "source_doc_pasted_conversation", "origin": "pasted inline by the user in turn 1, as the claims to be checked", "content": D.SOURCE_DOC_PASTED_CONVERSATION},
        ],
        "artifacts": load_artifacts(),
    }


def write_json(full):
    path = os.path.join(OUT, "transcript.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(full, f, ensure_ascii=False, indent=2)
    print("wrote", path, os.path.getsize(path), "bytes")


def md_escape_table_cell(s):
    return s.replace("\n", "<br>").replace("|", "\\|")


def write_markdown(full):
    m = full["meta"]
    L = []
    L.append(f"# {m['title']}\n")
    L.append(f"**Repo:** `{m['repo']}` · **Branch:** `{m['branch']}` · **PR:** [{m['pr']}]({m['pr_url']})  ")
    L.append(f"**Session span:** {m['session_span']} · **Export generated:** {m['generated_at']}\n")
    L.append("**Models involved:**")
    for mi in m["models_involved"]:
        L.append(f"- {mi}")
    L.append("")
    L.append("## Why this export exists (user's own words, verbatim)\n")
    L.append("> " + m["purpose_as_stated_by_user"].replace("\n", "\n> "))
    L.append("")
    L.append("## Privacy note\n")
    L.append(m["privacy_note"] + "\n")

    L.append("---\n\n## 1. Turn-by-turn transcript\n")
    L.append("Full inputs, harness side-effects, and outputs, in order. Nothing paraphrased; condensed only where a turn would otherwise repeat a table shown elsewhere in this document (cross-referenced instead).\n")
    for t in full["turns"]:
        L.append(f"### Turn {t['turn']} — {t['date']} — {t['speaker']} — {t['model']}\n")
        L.append(f"*Channel: {t['channel']}*\n")
        L.append("**Input:**\n")
        L.append("```\n" + t["raw_text"].strip() + "\n```\n")
        if t.get("harness_side_effect"):
            L.append(f"**Harness side-effect:** {t['harness_side_effect']}\n")
        L.append("**Output / action taken:**\n")
        L.append(t["assistant_text"].strip() + "\n")
        if t.get("notes"):
            L.append(f"*Note: {t['notes']}*\n")
        L.append("")

    L.append("---\n\n## 2. Deltas — every correction made, with source\n")
    L.append("| Category | Was claimed | Actually | Source |")
    L.append("|---|---|---|---|")
    for d in full["deltas"]:
        L.append(f"| {md_escape_table_cell(d['category'])} | {md_escape_table_cell(d['was_claimed'])} | {md_escape_table_cell(d['actually'])} | {md_escape_table_cell(d['source'])} |")
    L.append("")

    L.append("---\n\n## 3. Your thinking vs. my thinking\n")
    L.append("Where Dr. Rahman's stated or implied intent and the assistant's actual interpretation could have diverged, turn by turn — including the one case (turn 5) where the assistant acted on an inference from structure (a model switch) rather than from words, stated explicitly rather than silently assumed.\n")
    for tc in full["thinking_comparison"]:
        L.append(f"### Turn {tc['turn']}\n")
        L.append(f"- **User intent as stated:** {tc['user_intent_as_stated']}")
        L.append(f"- **Assistant interpretation:** {tc['assistant_interpretation']}")
        L.append(f"- **Divergence:** {tc['divergence']}")
        L.append(f"- **How handled:** {tc['how_handled']}")
        L.append("")

    L.append("---\n\n## 4. Gate grades — turn 5's independent-verifier pass against `spine/verify.md`\n")
    L.append("| # | Line | Verdict | Basis |")
    L.append("|---|---|---|---|")
    for g in full["gate_grades"]:
        L.append(f"| {g['line']} | {md_escape_table_cell(g['name'])} | **{g['verdict']}** | {md_escape_table_cell(g['basis'])} |")
    L.append("")

    L.append("---\n\n## 5. Open items — unresolved as of this export\n")
    L.append("| Item | Owner | Age | Blocking |")
    L.append("|---|---|---|---|")
    for o in full["open_items"]:
        L.append(f"| {md_escape_table_cell(o['item'])} | {md_escape_table_cell(o['owner'])} | {md_escape_table_cell(o['age'])} | {md_escape_table_cell(o['blocking'])} |")
    L.append("")

    L.append("---\n\n## 6. Commits\n")
    L.append("| SHA | Date | Author | Message |")
    L.append("|---|---|---|---|")
    for c in full["commits"]:
        L.append(f"| `{c['sha']}` | {c['date']} | {md_escape_table_cell(c['author'])} | {md_escape_table_cell(c['message'])} |")
    L.append("")

    L.append("---\n\n## 7. Source documents (full text, as received)\n")
    for sd in full["source_documents"]:
        L.append(f"### {sd['name']}\n")
        L.append(f"*Origin: {sd['origin']}*\n")
        L.append("```\n" + sd["content"].strip() + "\n```\n")

    L.append("---\n\n## 8. Artifacts (full current file contents, read live from the repo at export time)\n")
    for a in full["artifacts"]:
        L.append(f"### `{a['path']}`\n")
        L.append(f"*{a['description']}*  ")
        L.append(f"*Last commit: `{a['last_commit'][:7] if a['last_commit'] else 'n/a'}` ({a['last_commit_date']}) · {a['lines']} lines, {a['bytes']} bytes*\n")
        L.append("```markdown\n" + a["content"].rstrip() + "\n```\n")

    text = "\n".join(L)
    path = os.path.join(OUT, "transcript.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path, os.path.getsize(path), "bytes")
    return text


def sql_str(s):
    return "'" + s.replace("'", "''") + "'"


def write_sql(full):
    L = []
    L.append("-- Angelic-orchestrator voice-capture session export — SQL schema + data.")
    L.append("-- SQLite-flavored (TEXT/INTEGER only); loads cleanly in any standard SQL engine.")
    L.append("-- Generated from data.py + live repo reads — see transcript.md/.json for the same data in other shapes.")
    L.append("")
    L.append("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);")
    L.append("CREATE TABLE commits (sha TEXT PRIMARY KEY, full_sha TEXT, date TEXT, author TEXT, message TEXT);")
    L.append("CREATE TABLE turns (turn INTEGER PRIMARY KEY, date TEXT, model TEXT, speaker TEXT, channel TEXT, raw_text TEXT, harness_side_effect TEXT, assistant_text TEXT, notes TEXT);")
    L.append("CREATE TABLE deltas (id INTEGER PRIMARY KEY, category TEXT, was_claimed TEXT, actually TEXT, source TEXT);")
    L.append("CREATE TABLE thinking_comparison (turn INTEGER PRIMARY KEY, user_intent_as_stated TEXT, assistant_interpretation TEXT, divergence TEXT, how_handled TEXT);")
    L.append("CREATE TABLE gate_grades (line INTEGER PRIMARY KEY, name TEXT, verdict TEXT, basis TEXT);")
    L.append("CREATE TABLE open_items (id INTEGER PRIMARY KEY, item TEXT, owner TEXT, age TEXT, blocking TEXT);")
    L.append("CREATE TABLE source_documents (name TEXT PRIMARY KEY, origin TEXT, content TEXT);")
    L.append("CREATE TABLE artifacts (path TEXT PRIMARY KEY, description TEXT, last_commit TEXT, last_commit_date TEXT, lines INTEGER, bytes INTEGER, content TEXT);")
    L.append("")

    for k, v in full["meta"].items():
        if isinstance(v, list):
            v = " | ".join(v)
        L.append(f"INSERT INTO meta (key, value) VALUES ({sql_str(k)}, {sql_str(str(v))});")
    L.append("")

    for c in full["commits"]:
        L.append(
            "INSERT INTO commits (sha, full_sha, date, author, message) VALUES ("
            f"{sql_str(c['sha'])}, {sql_str(c['full_sha'])}, {sql_str(c['date'])}, "
            f"{sql_str(c['author'])}, {sql_str(c['message'])});"
        )
    L.append("")

    for t in full["turns"]:
        L.append(
            "INSERT INTO turns (turn, date, model, speaker, channel, raw_text, harness_side_effect, assistant_text, notes) VALUES ("
            f"{t['turn']}, {sql_str(t['date'])}, {sql_str(t['model'])}, {sql_str(t['speaker'])}, "
            f"{sql_str(t['channel'])}, {sql_str(t['raw_text'])}, "
            f"{sql_str(t.get('harness_side_effect') or '')}, {sql_str(t['assistant_text'])}, "
            f"{sql_str(t.get('notes') or '')});"
        )
    L.append("")

    for i, d in enumerate(full["deltas"], start=1):
        L.append(
            f"INSERT INTO deltas (id, category, was_claimed, actually, source) VALUES ("
            f"{i}, {sql_str(d['category'])}, {sql_str(d['was_claimed'])}, {sql_str(d['actually'])}, {sql_str(d['source'])});"
        )
    L.append("")

    for tc in full["thinking_comparison"]:
        L.append(
            "INSERT INTO thinking_comparison (turn, user_intent_as_stated, assistant_interpretation, divergence, how_handled) VALUES ("
            f"{tc['turn']}, {sql_str(tc['user_intent_as_stated'])}, {sql_str(tc['assistant_interpretation'])}, "
            f"{sql_str(tc['divergence'])}, {sql_str(tc['how_handled'])});"
        )
    L.append("")

    for g in full["gate_grades"]:
        L.append(
            f"INSERT INTO gate_grades (line, name, verdict, basis) VALUES ("
            f"{g['line']}, {sql_str(g['name'])}, {sql_str(g['verdict'])}, {sql_str(g['basis'])});"
        )
    L.append("")

    for i, o in enumerate(full["open_items"], start=1):
        L.append(
            f"INSERT INTO open_items (id, item, owner, age, blocking) VALUES ("
            f"{i}, {sql_str(o['item'])}, {sql_str(o['owner'])}, {sql_str(o['age'])}, {sql_str(o['blocking'])});"
        )
    L.append("")

    for sd in full["source_documents"]:
        L.append(
            f"INSERT INTO source_documents (name, origin, content) VALUES ("
            f"{sql_str(sd['name'])}, {sql_str(sd['origin'])}, {sql_str(sd['content'])});"
        )
    L.append("")

    for a in full["artifacts"]:
        L.append(
            "INSERT INTO artifacts (path, description, last_commit, last_commit_date, lines, bytes, content) VALUES ("
            f"{sql_str(a['path'])}, {sql_str(a['description'])}, {sql_str(a['last_commit'] or '')}, "
            f"{sql_str(a['last_commit_date'] or '')}, {a['lines']}, {a['bytes']}, {sql_str(a['content'])});"
        )
    L.append("")

    text = "\n".join(L)
    path = os.path.join(OUT, "transcript.sql")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path, os.path.getsize(path), "bytes")


def main():
    full = assemble()
    write_json(full)
    write_markdown(full)
    write_sql(full)
    print("DONE. turns=%d deltas=%d artifacts=%d" % (len(full["turns"]), len(full["deltas"]), len(full["artifacts"])))


if __name__ == "__main__":
    main()
