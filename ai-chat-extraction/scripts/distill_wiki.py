#!/usr/bin/env python3
"""
distill_wiki.py — Karpathian INGEST: raw conversations → wiki layer.

Two backends:

  --backend cli   (default) Drives Claude Code (`claude -p`) inside your vault.
                  CLAUDE.md in the vault root defines the INGEST operation, so
                  Claude updates/creates wiki pages, cross-links, index.md and
                  log.md exactly per your schema. Uses your existing Claude
                  Code login — no API key needed.

  --backend api   Calls the Anthropic API directly (model claude-opus-4-8) for
                  a fast first-pass distillation: one structured summary note
                  per conversation into wiki/distilled/, with entities/concepts
                  extracted as wikilinks. Good for bulk-processing years of
                  history cheaply before the deeper CLI ingest.
                  Requires: pip install anthropic  +  ANTHROPIC_API_KEY
                  (or an `ant auth login` profile).

Usage:
    python3 distill_wiki.py --vault ~/Vault --batch 10
    python3 distill_wiki.py --vault ~/Vault --backend api --batch 50
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def find_undistilled(vault: Path):
    raw = vault / "raw" / "conversations"
    if not raw.exists():
        sys.exit(f"ERROR: {raw} not found — run extract_chats.py first.")
    notes = []
    for p in sorted(raw.rglob("*.md")):
        head = p.read_text(encoding="utf-8", errors="replace")[:2000]
        if "distilled: false" in head:
            notes.append(p)
    return notes


def mark_distilled(path: Path):
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("distilled: false", "distilled: true", 1),
                    encoding="utf-8")


# ---------------------------------------------------------------- CLI backend

def run_cli(vault: Path, batch: int):
    prompt = (
        f"Run the INGEST operation defined in CLAUDE.md on the next {batch} "
        f"raw conversation notes that still have `distilled: false` (oldest "
        f"first). Follow the schema exactly: update/create wiki pages with "
        f"provenance, update wiki/index.md, append to wiki/log.md, flip "
        f"`distilled: true` on each processed note. Finish with a short "
        f"summary and ONE next action."
    )
    print(f"→ launching Claude Code in {vault} (batch of {batch})…")
    result = subprocess.run(
        ["claude", "-p", prompt, "--permission-mode", "acceptEdits"],
        cwd=vault,
    )
    if result.returncode != 0:
        sys.exit("ERROR: claude CLI failed. Is Claude Code installed and "
                 "logged in? (https://code.claude.com)")


# ---------------------------------------------------------------- API backend

DISTILL_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string",
                    "description": "3-6 sentence summary of the conversation"},
        "key_insights": {"type": "array", "items": {"type": "string"}},
        "entities": {"type": "array", "items": {"type": "string"},
                     "description": "People, orgs, products, tools mentioned"},
        "concepts": {"type": "array", "items": {"type": "string"},
                     "description": "Ideas, methods, themes worth a wiki page"},
        "action_items": {"type": "array", "items": {"type": "string"},
                         "description": "Things the user said they'd do"},
        "tags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "key_insights", "entities", "concepts",
                 "action_items", "tags"],
    "additionalProperties": False,
}

DISTILL_PROMPT = """You are distilling one archived AI conversation into a \
permanent knowledge-base entry for its owner. Extract only what is durable: \
decisions, insights, facts about named entities, recurring themes, and \
unfinished action items. Ignore pleasantries and dead ends. Entity and \
concept names should be short Title Case phrases suitable as wiki page names.

Conversation follows:

{conversation}"""


def run_api(vault: Path, notes, batch: int):
    try:
        import anthropic
    except ImportError:
        sys.exit("ERROR: pip install anthropic")

    client = anthropic.Anthropic()
    out_dir = vault / "wiki" / "distilled"
    out_dir.mkdir(parents=True, exist_ok=True)
    done = 0

    for path in notes[:batch]:
        text = path.read_text(encoding="utf-8", errors="replace")
        # keep well inside the context window for very long conversations
        if len(text) > 400_000:
            text = text[:400_000] + "\n\n[truncated]"
        try:
            response = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=8000,
                output_config={"format": {"type": "json_schema",
                                          "schema": DISTILL_SCHEMA}},
                messages=[{"role": "user",
                           "content": DISTILL_PROMPT.format(conversation=text)}],
            )
        except anthropic.RateLimitError:
            print("  ! rate limited — stopping here; re-run to continue.")
            break
        except anthropic.APIStatusError as e:
            print(f"  ! API error {e.status_code} on {path.name} — skipping",
                  file=sys.stderr)
            continue

        if response.stop_reason == "refusal":
            print(f"  ! refused: {path.name} — skipping", file=sys.stderr)
            continue

        data = json.loads(next(b.text for b in response.content
                               if b.type == "text"))
        write_distilled_note(out_dir, path, data)
        mark_distilled(path)
        done += 1
        print(f"  ✓ {path.name}")

    print(f"✓ distilled {done} conversations → {out_dir}")
    print("  Deeper pass later: run distill_wiki.py --backend cli (or just "
          "`claude` in the vault and say 'ingest').")


def write_distilled_note(out_dir: Path, raw_path: Path, data: dict):
    links = lambda items: "\n".join(f"- [[{i}]]" for i in items) or "- (none)"
    bullets = lambda items: "\n".join(f"- {i}" for i in items) or "- (none)"
    tags = ", ".join(t.replace(" ", "-").lower() for t in data.get("tags", []))
    body = f"""---
type: synthesis
title: "Distilled — {raw_path.stem}"
description: "First-pass distillation of [[{raw_path.stem}]]"
tags: [distilled, {tags}]
created: {date.today().isoformat()}
updated: {date.today().isoformat()}
sources: ["[[{raw_path.stem}]]"]
confidence: medium
---

# Distilled — {raw_path.stem}

{data['summary']}

## Key insights
{bullets(data['key_insights'])}

## Entities
{links(data['entities'])}

## Concepts
{links(data['concepts'])}

## Unfinished action items
{bullets(data['action_items'])}
"""
    (out_dir / f"{raw_path.stem} (distilled).md").write_text(body,
                                                             encoding="utf-8")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Distill raw chats into the wiki")
    ap.add_argument("--vault", required=True)
    ap.add_argument("--backend", default="cli", choices=["cli", "api"])
    ap.add_argument("--batch", type=int, default=10)
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    notes = find_undistilled(vault)
    print(f"→ {len(notes)} undistilled conversations found")
    if not notes:
        return

    if args.backend == "cli":
        run_cli(vault, args.batch)
    else:
        run_api(vault, notes, args.batch)


if __name__ == "__main__":
    main()
