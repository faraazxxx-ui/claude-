#!/usr/bin/env python3
"""
resurface.py — The gravity loop. Pushes old notes back onto today's desk.

Karpathy's append-and-review note works because old items "sink under
gravity" and he periodically scrolls down to rescue what still matters.
ADHD breaks the "periodically scrolls down" part — out of sight is out of
existence. This script IS the scrolling: every day it picks a handful of
old notes (weighted toward things unseen the longest) and appends them to
today's daily note, where you'll actually look.

Usage:
    python3 resurface.py --vault ~/Vault            # 4 picks into today's note
    python3 resurface.py --vault ~/Vault --count 6

Schedule it (that's the whole point — it must not depend on you remembering):
  macOS/Linux crontab:   0 6 * * *  /usr/bin/python3 /path/to/resurface.py --vault "$HOME/Vault"
  Windows Task Scheduler: daily 06:00 → python resurface.py --vault C:\\Users\\you\\Vault

No third-party dependencies.
"""

import argparse
import random
import re
import sys
from datetime import date, datetime
from pathlib import Path

FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
RESURFACE_HEADER = "## 🔁 Resurfaced"


def note_weight(path: Path, text: str) -> float:
    """Higher weight = more overdue for another look."""
    fm = FM_RE.match(text)
    fm_text = fm.group(1) if fm else ""
    weight = 1.0

    m = re.search(r"last_resurfaced:\s*(\S+)", fm_text)
    if not m or m.group(1) == "never":
        weight *= 3.0                      # never resurfaced → strongly favored
    else:
        try:
            days = (date.today() - date.fromisoformat(m.group(1))).days
            weight *= min(days / 30.0, 3.0)  # grows for a month, then caps
        except ValueError:
            weight *= 1.5

    m = re.search(r"^date:\s*\"?(\d{4}-\d{2}-\d{2})", fm_text, re.M)
    if m:
        try:
            age_years = (date.today() - date.fromisoformat(m.group(1))).days / 365
            weight *= 1.0 + min(age_years, 4) * 0.4   # older thinking favored
        except ValueError:
            pass

    if "- [ ]" in text:
        weight *= 2.0                      # open checkboxes = open loops
    if re.search(r"type:\s*(project|self)", fm_text):
        weight *= 1.5
    return weight


def first_line(text: str) -> str:
    body = FM_RE.sub("", text, count=1)
    for line in body.splitlines():
        line = line.strip().lstrip("#>-* ").strip()
        if len(line) > 15:
            return line[:140]
    return ""


def touch_last_resurfaced(path: Path, text: str):
    today = date.today().isoformat()
    if "last_resurfaced:" in text:
        new = re.sub(r"last_resurfaced:\s*\S+", f"last_resurfaced: {today}",
                     text, count=1)
    elif FM_RE.match(text):
        new = text.replace("---\n", f"---\nlast_resurfaced: {today}\n", 1)
    else:
        return
    path.write_text(new, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Resurface old notes into today")
    ap.add_argument("--vault", required=True)
    ap.add_argument("--count", type=int, default=4)
    ap.add_argument("--folders", nargs="*",
                    default=["raw/conversations", "wiki"],
                    help="Folders to draw from")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    pool = []
    for folder in args.folders:
        root = vault / folder
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if p.name in ("index.md", "log.md"):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            pool.append((p, text, note_weight(p, text)))

    if not pool:
        sys.exit("Nothing to resurface — is the vault path right?")

    k = min(args.count, len(pool))
    picks, chosen = [], set()
    paths, texts, weights = zip(*pool)
    while len(picks) < k:
        (p, t), = random.choices(list(zip(paths, texts)), weights=weights, k=1)
        if p in chosen:
            continue
        chosen.add(p)
        picks.append((p, t))

    # write into today's daily note
    daily_dir = vault / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    daily = daily_dir / f"{today}.md"
    if daily.exists():
        content = daily.read_text(encoding="utf-8")
    else:
        content = (f"---\ndate: \"{today}\"\ntype: daily\ntags: [daily]\n---\n\n"
                   f"# {datetime.now().strftime('%A, %B %-d') if sys.platform != 'win32' else datetime.now().strftime('%A, %B %d')}\n")

    stamp = datetime.now().strftime("%H:%M")
    lines = [f"\n{RESURFACE_HEADER}" if RESURFACE_HEADER not in content else "",
             f"\n> resurfaced {stamp}:"]
    for p, t in picks:
        teaser = first_line(t)
        lines.append(f"- [[{p.stem}]] — {teaser}")
        touch_last_resurfaced(p, t)

    daily.write_text(content.rstrip() + "\n" + "\n".join(l for l in lines if l)
                     + "\n", encoding="utf-8")
    print(f"✓ resurfaced {len(picks)} notes into daily/{today}.md")
    for p, _ in picks:
        print(f"  ↺ {p.stem}")


if __name__ == "__main__":
    main()
