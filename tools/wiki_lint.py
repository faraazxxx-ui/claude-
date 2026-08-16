#!/usr/bin/env python3
"""
wiki_lint.py — check the integrity of the brain, and draw its actual shape.

A second brain fails silently. Pages rot, links break, notes get written that nothing
ever points at. None of that throws an error, so it accumulates until the corpus is
untrustworthy and you go back to asking the model from scratch.

This makes the failure loud:

  broken links   a [[link]] whose target page does not exist
  orphans        a page nothing links to — written once, never found again
  dead ends      a page that links to nothing — a leaf that never got connected
  hubs           the pages with the most inbound links: your real centres of gravity
  stale          pages untouched longest, ranked by git history

Exits non-zero when broken links exist, so it works as a pre-commit hook or CI gate.

Usage:
    python3 tools/wiki_lint.py brain
    python3 tools/wiki_lint.py brain --mermaid brain/_forensics/graph.md
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def slug(name: str) -> str:
    """Normalise a link target or filename to a comparable key."""
    return re.sub(r"[^a-z0-9]+", "-", Path(name.strip()).stem.lower()).strip("-")


def git_last_modified(path: Path, repo_root: Path):
    """Last commit date touching this file. None if untracked or git is unavailable."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo_root), "log", "-1", "--format=%as", "--", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or None
    except (subprocess.SubprocessError, OSError):
        return None


def collect(root: Path):
    """Index every corpus page and the links between them.

    Underscore-prefixed directories (`_templates`, `_forensics`) are meta, not corpus: templates
    carry placeholder links by design and forensics output is generated. They are registered as
    link *targets* so real pages may point at them, but never linted as sources.
    """
    pages, links = {}, defaultdict(set)
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.parts):
            continue
        key = slug(path.name)
        is_meta = any(part.startswith("_") for part in path.relative_to(root).parts[:-1])
        text = path.read_text(encoding="utf-8", errors="replace")
        body = FRONTMATTER_RE.sub("", text)
        pages[key] = {
            "path": path,
            "title": path.stem,
            "words": len(body.split()),
            "is_template": is_meta,
        }
        if is_meta:
            continue
        # `[[link]]` inside backticks is prose about the syntax, not an actual link.
        linkable = INLINE_CODE_RE.sub(" ", FENCED_CODE_RE.sub(" ", body))
        for target in WIKILINK_RE.findall(linkable):
            tkey = slug(target)
            if tkey and tkey != key:
                links[key].add(tkey)
    return pages, links


def analyse(pages, links):
    inbound = defaultdict(set)
    broken = []
    for src, targets in links.items():
        for tgt in targets:
            if tgt in pages:
                inbound[tgt].add(src)
            else:
                broken.append((src, tgt))

    real = {k: v for k, v in pages.items() if not v["is_template"]}
    orphans = [k for k in real if not inbound.get(k) and k not in ("index", "readme")]
    dead_ends = [k for k in real if not links.get(k)]
    hubs = Counter({k: len(v) for k, v in inbound.items() if k in real})
    return inbound, broken, orphans, dead_ends, hubs


def mermaid(pages, links, inbound, limit=40):
    """Render the link graph, keeping the most-connected nodes so it stays legible."""
    degree = Counter()
    for src, targets in links.items():
        degree[src] += len(targets)
        for t in targets:
            degree[t] += 1
    keep = {k for k, _ in degree.most_common(limit)} & set(pages)
    if not keep:
        return "```mermaid\ngraph LR\n  empty[No links yet]\n```\n"

    lines = ["```mermaid", "graph LR"]
    for key in sorted(keep):
        label = pages[key]["title"].replace('"', "'")
        shape = f'(["{label}"])' if len(inbound.get(key, ())) >= 3 else f'["{label}"]'
        lines.append(f"  {key.replace('-', '_')}{shape}")
    for src, targets in sorted(links.items()):
        if src not in keep:
            continue
        for tgt in sorted(targets):
            if tgt in keep:
                lines.append(f"  {src.replace('-', '_')} --> {tgt.replace('-', '_')}")
    lines.append("```")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", type=Path, nargs="?", default=Path("brain"))
    ap.add_argument("--mermaid", type=Path, help="write a Mermaid graph of the link topology here")
    ap.add_argument("--quiet", action="store_true", help="only report problems")
    args = ap.parse_args()

    if not args.root.exists():
        sys.exit(f"error: {args.root} does not exist")

    pages, links = collect(args.root)
    if not pages:
        sys.exit(f"error: no markdown pages found under {args.root}")

    inbound, broken, orphans, dead_ends, hubs = analyse(pages, links)
    real_count = sum(1 for p in pages.values() if not p["is_template"])
    total_links = sum(len(v) for v in links.values())

    if not args.quiet:
        print(f"\n  {real_count} pages, {total_links} links, "
              f"{round(total_links / max(real_count, 1), 1)} links/page\n")
        if hubs:
            print("  Centres of gravity (most linked-to):")
            for key, n in hubs.most_common(8):
                print(f"    {n:>3} inbound  {pages[key]['title']}")
            print()

    problems = 0
    if broken:
        problems += len(broken)
        print(f"  BROKEN LINKS ({len(broken)}):")
        for src, tgt in sorted(broken)[:25]:
            print(f"    {pages[src]['path']} -> [[{tgt}]] (no such page)")
        print()

    if orphans:
        print(f"  ORPHANS ({len(orphans)}) — written once, nothing points here:")
        for key in sorted(orphans)[:25]:
            print(f"    {pages[key]['path']}")
        print()

    if dead_ends and not args.quiet:
        print(f"  DEAD ENDS ({len(dead_ends)}) — link out to nothing:")
        for key in sorted(dead_ends)[:15]:
            print(f"    {pages[key]['path']}")
        print()

    repo_root = Path.cwd()
    dated = [(git_last_modified(p["path"], repo_root), p["path"])
             for k, p in pages.items() if not p["is_template"]]
    dated = [(d, p) for d, p in dated if d]
    if dated and not args.quiet:
        dated.sort()
        print("  STALEST PAGES:")
        for date, path in dated[:5]:
            print(f"    {date}  {path}")
        print()

    if args.mermaid:
        args.mermaid.parent.mkdir(parents=True, exist_ok=True)
        args.mermaid.write_text(
            "# Brain link graph\n\n"
            "*Auto-generated by `tools/wiki_lint.py`. Rounded nodes have 3+ inbound links —\n"
            "those are the concepts everything else hangs off.*\n\n"
            + mermaid(pages, links, inbound), encoding="utf-8")
        print(f"  graph -> {args.mermaid}\n")

    if problems:
        print(f"  FAILED: {problems} broken link(s).\n")
        return 1
    if not args.quiet:
        print("  OK: no broken links.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
