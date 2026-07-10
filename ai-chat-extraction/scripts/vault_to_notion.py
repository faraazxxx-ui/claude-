#!/usr/bin/env python3
"""
vault_to_notion.py — Mirror vault notes into a Notion database.

Obsidian stays your primary surface; Notion becomes the invisible, queryable
mirror (per your SYSTEM.md: "you never open Notion"). This script walks the
vault, pushes every note with `notion_synced: false` in its frontmatter to a
Notion database, then flips the flag so re-runs are incremental.

Setup (once):
  1. notion.so/my-integrations → New integration → copy the secret
  2. Create a database with properties:
       Name (title), Type (select), Platform (select), Date (date),
       Tags (multi-select), VaultPath (rich text)
  3. Share the database with your integration (••• → Connections)
  4. export NOTION_API_KEY=secret_xxx  NOTION_DB_ID=xxxx

Usage:
    python3 vault_to_notion.py --vault ~/Vault
    python3 vault_to_notion.py --vault ~/Vault --include raw wiki --limit 200

No third-party dependencies (urllib only).
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"
FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
MAX_BLOCKS_PER_REQUEST = 100  # Notion API limit
MAX_CHARS_PER_BLOCK = 1990    # Notion rich_text limit is 2000


def notion_request(method: str, url: str, payload=None):
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        sys.exit("ERROR: set NOTION_API_KEY")
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limited — honor Retry-After
                wait = float(e.headers.get("Retry-After", "2"))
                time.sleep(wait)
                continue
            body = e.read().decode(errors="replace")[:300]
            raise RuntimeError(f"Notion {e.code}: {body}") from e
    raise RuntimeError("Notion: rate-limited after retries")


def parse_frontmatter(text: str) -> dict:
    """Minimal YAML-ish frontmatter parser (flat key: value + [a, b] lists)."""
    m = FM_RE.match(text)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "-")):
            continue
        key, _, val = line.partition(":")
        val = val.strip().strip('"')
        if val.startswith("[") and val.endswith("]"):
            fm[key.strip()] = [v.strip().strip('"') for v in
                               val[1:-1].split(",") if v.strip()]
        else:
            fm[key.strip()] = val
    return fm


def chunk_blocks(body: str):
    """Markdown body → Notion paragraph blocks (dumb but lossless)."""
    blocks = []
    for para in body.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        for i in range(0, len(para), MAX_CHARS_PER_BLOCK):
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [
                    {"type": "text",
                     "text": {"content": para[i:i + MAX_CHARS_PER_BLOCK]}}
                ]},
            })
    return blocks


def build_properties(fm: dict, rel_path: str):
    title = fm.get("title") or Path(rel_path).stem
    props = {
        "Name": {"title": [{"text": {"content": title[:200]}}]},
        "VaultPath": {"rich_text": [{"text": {"content": rel_path[:200]}}]},
    }
    if fm.get("type"):
        props["Type"] = {"select": {"name": fm["type"][:100]}}
    if fm.get("platform"):
        props["Platform"] = {"select": {"name": fm["platform"][:100]}}
    date = fm.get("date") or fm.get("created")
    if date and re.match(r"\d{4}-\d{2}-\d{2}", str(date)):
        props["Date"] = {"date": {"start": str(date)[:10]}}
    tags = fm.get("tags") or []
    if isinstance(tags, list) and tags:
        props["Tags"] = {"multi_select": [{"name": t[:100]} for t in tags[:10]]}
    return props


def push_note(path: Path, vault: Path, db_id: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    if fm.get("notion_synced") == "true":
        return False
    body = FM_RE.sub("", text, count=1)
    blocks = chunk_blocks(body)
    rel = str(path.relative_to(vault))

    page = notion_request("POST", f"{API}/pages", {
        "parent": {"database_id": db_id},
        "properties": build_properties(fm, rel),
        "children": blocks[:MAX_BLOCKS_PER_REQUEST],
    })
    # append any overflow blocks in batches of 100
    remaining = blocks[MAX_BLOCKS_PER_REQUEST:]
    while remaining:
        notion_request("PATCH", f"{API}/blocks/{page['id']}/children",
                       {"children": remaining[:MAX_BLOCKS_PER_REQUEST]})
        remaining = remaining[MAX_BLOCKS_PER_REQUEST:]
        time.sleep(0.34)

    # flip the flag (add it if the note never had one)
    if "notion_synced: false" in text:
        new_text = text.replace("notion_synced: false", "notion_synced: true", 1)
    elif FM_RE.match(text):
        new_text = text.replace("---\n", "---\nnotion_synced: true\n", 1)
    else:
        new_text = f"---\nnotion_synced: true\n---\n{text}"
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Sync vault notes to Notion")
    ap.add_argument("--vault", required=True)
    ap.add_argument("--include", nargs="*", default=["raw", "wiki"],
                    help="Top-level vault folders to sync (default: raw wiki)")
    ap.add_argument("--limit", type=int, default=500,
                    help="Max pages to create this run (default 500)")
    args = ap.parse_args()

    db_id = os.environ.get("NOTION_DB_ID")
    if not db_id:
        sys.exit("ERROR: set NOTION_DB_ID")
    vault = Path(args.vault).expanduser()

    candidates = []
    for folder in args.include:
        root = vault / folder
        if root.exists():
            candidates.extend(sorted(root.rglob("*.md")))

    pushed = 0
    for path in candidates:
        if pushed >= args.limit:
            print(f"→ hit --limit {args.limit}; re-run to continue.")
            break
        try:
            if push_note(path, vault, db_id):
                pushed += 1
                print(f"  ✓ {path.relative_to(vault)}")
                time.sleep(0.34)  # ~3 req/s Notion rate limit
        except Exception as e:
            print(f"  ! {path.name}: {e}", file=sys.stderr)

    print(f"✓ synced {pushed} notes to Notion")


if __name__ == "__main__":
    main()
