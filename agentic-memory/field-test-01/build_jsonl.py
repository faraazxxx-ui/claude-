#!/usr/bin/env python3
"""Build BigQuery-ready JSONL from 01-ATOMIC-NOTES.md.

Single source of truth is the markdown. Re-run this after editing notes:
    python3 build_jsonl.py

Emits notes.jsonl (newline-delimited, one documents row per note), schema.json
(verbatim from Personal_Data_Embedding_Living_AI_Guide.md Stage 2.2), and a
validation report on stdout. No embeddings are generated — that is Stage 4.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_MD = os.path.join(HERE, "01-ATOMIC-NOTES.md")

# Guide Stage 2.2, verbatim field list.
SCHEMA = [
    {"name": "document_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
    {"name": "content", "type": "STRING", "mode": "NULLABLE"},
    {"name": "source_type", "type": "STRING", "mode": "REQUIRED",
     "description": "email | note | pdf | chat | social | browser"},
    {"name": "life_domain", "type": "STRING", "mode": "NULLABLE",
     "description": "career | finance | health | learning | personal | creative "
                    "| relationships | home | digital | reference"},
    {"name": "metadata", "type": "RECORD", "mode": "NULLABLE", "fields": [
        {"name": "source", "type": "STRING", "mode": "NULLABLE"},
        {"name": "author", "type": "STRING", "mode": "NULLABLE"},
        {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "modified_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "tags", "type": "STRING", "mode": "REPEATED"},
        {"name": "importance_score", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "triage_category", "type": "STRING", "mode": "NULLABLE"},
    ]},
    {"name": "embeddings", "type": "FLOAT", "mode": "REPEATED",
     "description": "Vector embeddings array (768-3072 dimensions)"},
    {"name": "chunk_index", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "ingestion_timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
]

LIFE_DOMAINS = {"career", "finance", "health", "learning", "personal",
                "creative", "relationships", "home", "digital", "reference"}
SOURCE_TYPES = {"email", "note", "pdf", "chat", "social", "browser"}

CLAUDE_CONVS = {"C1", "C2", "C3", "C4", "C5"}
CHATGPT_CONVS = {"C6", "C7", "C8"}

# Conversation dates. C6-C8 are stamped in the exports; C1-C5 are only known
# from their export stamp, so those rows carry the date:approx tag rather than
# implying a conversation date we cannot see.
CONV_DATE = {
    "C1": ("2026-05-11T00:00:00Z", True), "C2": ("2026-05-11T00:00:00Z", True),
    "C3": ("2026-05-11T00:00:00Z", True), "C4": ("2026-05-11T00:00:00Z", True),
    "C5": ("2026-05-11T00:00:00Z", True),
    "C6": ("2025-10-14T00:00:00Z", False), "C7": ("2025-10-14T00:00:00Z", False),
    "C8": ("2025-10-14T00:00:00Z", False),
}

# Pattern -> supporting notes, mirroring 02-PATTERN-MAP.md.
PATTERNS = {
    "P1": ["N01", "N07", "N27"],
    "P2": ["N02", "N08"],
    "P3": ["N03", "N24"],
    "P4": ["N04", "N05", "N12", "N22", "N23"],
    "P5": ["N09", "N10"],
    "P6": ["N06", "N25", "N26", "N27", "N28"],
    "P7": ["N32", "N12", "N31"],
    "P8": ["N20", "N30"],
}
# Patterns whose stall carries an observed, avoidable cost.
ACT_NOW = {"P6", "P1", "P3"}


def conv_ids(source_line):
    """Extract C-ids from a Source line, expanding ranges like C1-C5."""
    found = set()
    for a, b in re.findall(r"C(\d)\s*[\u2013\u2014-]\s*C(\d)", source_line):
        for n in range(int(a), int(b) + 1):
            found.add("C%d" % n)
    for n in re.findall(r"\bC([1-8])\b", source_line):
        found.add("C" + n)
    return sorted(found)


def parse_notes(text):
    notes = []
    blocks = re.split(r"\n### ", text)
    for blk in blocks[1:]:
        head, _, rest = blk.partition("\n")
        m = re.match(r"(N\d{2})\s*[\u2013\u2014-]\s*(.+)", head.strip())
        if not m:
            continue
        note = {"id": m.group(1), "title": m.group(2).strip()}
        for key, field in (("Type", "type"), ("Source", "source"),
                           ("Body", "body"), ("Confidence", "confidence"),
                           ("Gap", "gap")):
            fm = re.search(r"^- \*\*%s:\*\*\s*(.+?)(?=\n- \*\*|\n---|\Z)" % key,
                           rest, re.S | re.M)
            note[field] = re.sub(r"\s+", " ", fm.group(1)).strip() if fm else ""
        notes.append(note)
    return notes


def life_domain(note, convs):
    is_content = note["type"].lower().startswith("content")
    if not convs:
        return "reference"
    if is_content:
        return "finance" if set(convs) <= CHATGPT_CONVS else "health"
    return "digital"


def importance(note, pats):
    """Stated rule, not a judgment call: supporting an act-now pattern is 9,
    otherwise High confidence is 7 and Medium is 5. Whole numbers only."""
    if any(p in ACT_NOW for p in pats):
        return 9.0
    return 7.0 if note["confidence"].lower().startswith("high") else 5.0


def main():
    text = open(NOTES_MD, encoding="utf-8").read()
    notes = parse_notes(text)
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                           capture_output=True, text=True).stdout.strip()

    rows, problems = [], []
    for note in notes:
        convs = conv_ids(note["source"])
        pats = sorted(p for p, ns in PATTERNS.items() if note["id"] in ns)
        plats = sorted(
            ({"platform:claude"} if set(convs) & CLAUDE_CONVS else set()) |
            ({"platform:chatgpt"} if set(convs) & CHATGPT_CONVS else set()))
        conf = "high" if note["confidence"].lower().startswith("high") else "medium"
        has_gap = note["gap"].lower() not in ("", "none", "none.")

        dates = [CONV_DATE[c] for c in convs if c in CONV_DATE]
        created = min(d for d, _ in dates) if dates else None
        approx = any(a for _, a in dates)

        tags = (["type:" + note["type"].split("(")[0].strip().lower().replace(" / ", "-").replace(" ", "-"),
                 "conf:" + conf] + plats +
                ["src:" + c.lower() for c in convs] +
                ["pattern:" + p.lower() for p in pats])
        if has_gap:
            tags.append("gap")
        if approx:
            tags.append("date:approx")

        content = "\n\n".join([
            note["body"],
            "Source: " + note["source"],
            "Confidence: " + note["confidence"],
            "Gap: " + (note["gap"] if has_gap else "none"),
        ])

        row = {
            "document_id": note["id"],
            "title": note["title"],
            "content": content,
            "source_type": "chat",
            "life_domain": life_domain(note, convs),
            "metadata": {
                "source": ", ".join(convs) if convs else "R1, R2",
                "author": "Dr Mohammed Faraaz Rahman",
                "created_at": created,
                "modified_at": None,
                "tags": tags,
                "importance_score": importance(note, pats),
                "triage_category": "behavioral-map",
            },
            "embeddings": [],
            "chunk_index": 0,
            "ingestion_timestamp": stamp,
        }
        rows.append(row)

        if not row["document_id"]:
            problems.append("%s: missing document_id" % note["id"])
        if row["source_type"] not in SOURCE_TYPES:
            problems.append("%s: source_type not in enum" % note["id"])
        if row["life_domain"] not in LIFE_DOMAINS:
            problems.append("%s: life_domain not in enum" % note["id"])
        if not row["ingestion_timestamp"]:
            problems.append("%s: missing ingestion_timestamp" % note["id"])
        if not row["title"] or not row["content"]:
            problems.append("%s: empty title or content" % note["id"])
        if not convs and note["id"] != "N34":
            problems.append("%s: no source conversation (orphan claim)" % note["id"])

    with open(os.path.join(HERE, "notes.jsonl"), "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(os.path.join(HERE, "schema.json"), "w", encoding="utf-8") as fh:
        json.dump(SCHEMA, fh, indent=2)
        fh.write("\n")

    print("rows: %d" % len(rows))
    print("orphan claims: %d" % sum(
        1 for r in rows if r["metadata"]["source"] in ("", None)))
    dom = {}
    for r in rows:
        dom[r["life_domain"]] = dom.get(r["life_domain"], 0) + 1
    print("life_domain: " + ", ".join("%s=%d" % kv for kv in sorted(dom.items())))
    print("validation: " + ("PASS" if not problems else "FAIL"))
    for p in problems:
        print("  - " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
