#!/usr/bin/env python3
"""
corpus_forensics.py — measure the gap between what you asked for and what you wanted.

Two modes:

  chats  Parse AI chat exports (Claude and/or ChatGPT `conversations.json`) and compute
         behavioural metrics: specification gap, restart families, abandonment, depth,
         and circadian engagement.

  files  Parse a directory of files (a repo, a Drive dump, an Obsidian vault) and compute
         structural metrics: version families, finality claims, byte-identical duplicates.

Both modes emit metrics.json + report.md, and seed wiki stubs for recurring topics.

Pure standard library. No numpy, pandas, or sklearn required.

Usage:
    python3 tools/corpus_forensics.py chats ingest/ -o brain/_forensics --tz-offset -5
    python3 tools/corpus_forensics.py files . -o brain/_forensics --exclude .git brain
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --------------------------------------------------------------------------------------
# Signal dictionaries
# --------------------------------------------------------------------------------------

# Phrases that mark "the answer I got was not the answer I wanted". Each hit in a user turn
# after the opening turn is one observed specification gap.
CORRECTION_MARKERS = [
    r"\bno,? i meant\b", r"\bi meant\b", r"\bthat'?s not what\b", r"\bnot what i\b",
    r"\bactually,? i\b", r"\bactually no\b", r"\bnot quite\b", r"\byou misunderstood\b",
    r"\bmisunderstood\b", r"\blet me rephrase\b", r"\bto clarify\b", r"\bi should have said\b",
    r"\binstead of that\b", r"\brather than that\b", r"\bnot like that\b", r"\bwrong\b",
    r"\btry again\b", r"\bredo\b", r"\bstart over\b", r"\bthat'?s wrong\b",
    r"\bi wanted\b", r"\bwhat i want(ed)? (is|was)\b", r"\bmy point (is|was)\b",
]

# Phrases that mark scope expansion mid-thread — the ADHD tell where one task becomes five.
EXPANSION_MARKERS = [
    r"\balso\b", r"\band another thing\b", r"\bwhile you'?re at it\b", r"\bcan you also\b",
    r"\badditionally\b", r"\boh and\b", r"\bone more thing\b", r"\balso can you\b",
]

# Filename tokens that claim finality or encode a version bump.
FINALITY_TOKENS = [
    "final", "perfected", "perfect", "complete", "master", "ultimate", "definitive",
    "optimized", "red_team", "redteam", "revised", "new", "latest", "fixed",
]
VERSION_RE = re.compile(r"[_\-. ]?v\d+(\.\d+)*\b|[_\-. ]\d+$", re.IGNORECASE)

STOPWORDS = set("""
a about above after again against all am an and any are aren't as at be because been before being
below between both but by can cannot could couldn't did didn't do does doesn't doing don't down during
each few for from further had hadn't has hasn't have haven't having he her here hers herself him himself
his how i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself
no nor not of off on once only or other ought our ours ourselves out over own same shan't she should
shouldn't so some such than that the their theirs them themselves then there these they this those
through to too under until up very was wasn't we were weren't what when where which while who whom why
with won't would wouldn't you your yours yourself yourselves get make like just want need know think
use using used one two also please thanks thank ok okay yes really much many way ways thing things
something anything everything sure right good great help give take see look go going come came
""".split())

TOKEN_RE = re.compile(r"[a-z][a-z0-9'\-]{2,}")


# --------------------------------------------------------------------------------------
# Normalisation: every export format collapses to the same shape
# --------------------------------------------------------------------------------------

def _parse_ts(value):
    """Accept epoch seconds (ChatGPT) or ISO-8601 (Claude). Return aware UTC datetime or None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if isinstance(value, str):
        raw = value.strip().replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(raw)
        except ValueError:
            return None
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return None


def _text_from_claude_message(msg):
    """Claude exports carry `text`, and newer ones a structured `content` list."""
    if isinstance(msg.get("content"), list):
        parts = [
            block.get("text", "")
            for block in msg["content"]
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        joined = "\n".join(p for p in parts if p)
        if joined.strip():
            return joined
    return msg.get("text") or ""


def normalize_claude(raw):
    """Claude.ai export: [{uuid, name, created_at, chat_messages:[{sender, text, created_at}]}]"""
    out = []
    for conv in raw:
        if not isinstance(conv, dict) or "chat_messages" not in conv:
            continue
        turns = []
        for msg in conv.get("chat_messages") or []:
            if not isinstance(msg, dict):
                continue
            sender = (msg.get("sender") or "").lower()
            role = "user" if sender in ("human", "user") else "assistant"
            text = _text_from_claude_message(msg)
            if not text.strip():
                continue
            turns.append({"role": role, "text": text, "ts": _parse_ts(msg.get("created_at"))})
        if turns:
            out.append({
                "id": conv.get("uuid") or hashlib.md5(str(conv).encode()).hexdigest()[:12],
                "title": conv.get("name") or "(untitled)",
                "created": _parse_ts(conv.get("created_at")),
                "source": "claude",
                "turns": turns,
            })
    return out


def normalize_chatgpt(raw):
    """ChatGPT export: [{title, create_time, mapping:{node:{message:{author,content,create_time}}}}]

    The mapping is a tree. We walk parent->child from the root so turns come out in
    conversation order rather than dict order, which is not guaranteed to be chronological.
    """
    out = []
    for conv in raw:
        if not isinstance(conv, dict) or "mapping" not in conv:
            continue
        mapping = conv.get("mapping") or {}
        if not isinstance(mapping, dict):
            continue

        children = {nid: (node or {}).get("children") or [] for nid, node in mapping.items()}
        parents = {nid: (node or {}).get("parent") for nid, node in mapping.items()}
        roots = [nid for nid, p in parents.items() if p is None or p not in mapping]

        ordered = []
        seen = set()

        def walk(nid):
            if nid in seen or nid not in mapping:
                return
            seen.add(nid)
            ordered.append(nid)
            # Follow the last child: on regenerated branches that is the surviving path.
            for child in children.get(nid, []):
                walk(child)

        for root in roots or list(mapping.keys())[:1]:
            walk(root)
        for nid in mapping:  # anything orphaned by a malformed tree
            walk(nid)

        turns = []
        for nid in ordered:
            msg = (mapping.get(nid) or {}).get("message")
            if not isinstance(msg, dict):
                continue
            role = ((msg.get("author") or {}).get("role") or "").lower()
            if role not in ("user", "assistant"):
                continue
            content = msg.get("content") or {}
            parts = content.get("parts") if isinstance(content, dict) else None
            text = ""
            if isinstance(parts, list):
                text = "\n".join(p for p in parts if isinstance(p, str))
            if not text.strip():
                continue
            turns.append({"role": role, "text": text, "ts": _parse_ts(msg.get("create_time"))})

        if turns:
            out.append({
                "id": conv.get("id") or conv.get("conversation_id")
                      or hashlib.md5(str(conv.get("title", "")).encode()).hexdigest()[:12],
                "title": conv.get("title") or "(untitled)",
                "created": _parse_ts(conv.get("create_time")),
                "source": "chatgpt",
                "turns": turns,
            })
    return out


def load_conversations(root: Path):
    """Find every *.json under root and normalise whichever export format it turns out to be."""
    conversations, files_read, skipped = [], [], []
    candidates = sorted(root.rglob("*.json")) if root.is_dir() else [root]

    for path in candidates:
        try:
            raw = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (json.JSONDecodeError, OSError) as exc:
            skipped.append(f"{path.name}: {type(exc).__name__}")
            continue
        if not isinstance(raw, list) or not raw:
            skipped.append(f"{path.name}: not a conversation list")
            continue

        probe = next((r for r in raw if isinstance(r, dict)), {})
        if "chat_messages" in probe:
            parsed = normalize_claude(raw)
        elif "mapping" in probe:
            parsed = normalize_chatgpt(raw)
        else:
            skipped.append(f"{path.name}: unrecognised schema")
            continue

        if parsed:
            conversations.extend(parsed)
            files_read.append(f"{path.name} ({len(parsed)} conversations)")

    return conversations, files_read, skipped


# --------------------------------------------------------------------------------------
# Text utilities
# --------------------------------------------------------------------------------------

def tokenize(text):
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


def shingles(text, size=4):
    """Overlapping n-gram set, used for near-duplicate detection between opening turns."""
    toks = tokenize(text)[:200]
    if len(toks) < size:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i:i + size]) for i in range(len(toks) - size + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def count_markers(text, patterns):
    low = text.lower()
    return sum(1 for p in patterns if re.search(p, low))


# --------------------------------------------------------------------------------------
# Metric: restart families (near-duplicate openings across separate conversations)
# --------------------------------------------------------------------------------------

def find_restart_families(conversations, threshold=0.45):
    """Cluster conversations whose opening user turn is near-identical.

    An inverted shingle index keeps this near-linear: only conversations sharing at least
    one 4-gram are ever compared, instead of all N^2 pairs.
    """
    openings = []
    for idx, conv in enumerate(conversations):
        first = next((t for t in conv["turns"] if t["role"] == "user"), None)
        if first and len(tokenize(first["text"])) >= 4:
            openings.append((idx, shingles(first["text"])))

    index = defaultdict(list)
    for idx, shs in openings:
        for sh in shs:
            index[sh].append(idx)

    shingle_by_idx = dict(openings)
    parent = {idx: idx for idx, _ in openings}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for idx, shs in openings:
        candidates = {c for sh in shs for c in index[sh] if c != idx}
        for cand in candidates:
            if find(idx) != find(cand) and jaccard(shingle_by_idx[idx], shingle_by_idx[cand]) >= threshold:
                union(idx, cand)

    groups = defaultdict(list)
    for idx, _ in openings:
        groups[find(idx)].append(idx)

    families = []
    for members in groups.values():
        if len(members) < 2:
            continue
        members.sort(key=lambda i: conversations[i]["created"] or datetime.min.replace(tzinfo=timezone.utc))
        span_days = None
        stamps = [conversations[i]["created"] for i in members if conversations[i]["created"]]
        if len(stamps) >= 2:
            span_days = round((max(stamps) - min(stamps)).total_seconds() / 86400, 1)
        families.append({
            "size": len(members),
            "span_days": span_days,
            "titles": [conversations[i]["title"][:90] for i in members],
            "resolved": any(len(conversations[i]["turns"]) >= 8 for i in members),
        })
    families.sort(key=lambda f: -f["size"])
    return families


# --------------------------------------------------------------------------------------
# Metric: salient topics (TF-IDF without sklearn)
# --------------------------------------------------------------------------------------

def salient_topics(conversations, top_n=25):
    doc_freq = Counter()
    term_freq = Counter()
    for conv in conversations:
        user_text = " ".join(t["text"] for t in conv["turns"] if t["role"] == "user")
        toks = tokenize(user_text)
        term_freq.update(toks)
        doc_freq.update(set(toks))

    n_docs = max(len(conversations), 1)
    scored = []
    for term, tf in term_freq.items():
        df = doc_freq[term]
        if df < 2 or tf < 3:
            continue
        # Sub-linear TF damps a term that is merely repeated inside one long rant.
        score = (1 + math.log(tf)) * math.log(n_docs / df)
        scored.append((score, term, tf, df))
    scored.sort(reverse=True)
    return [
        {"term": t, "score": round(s, 2), "mentions": tf, "conversations": df}
        for s, t, tf, df in scored[:top_n]
    ]


# --------------------------------------------------------------------------------------
# Mode: chats
# --------------------------------------------------------------------------------------

def analyse_chats(conversations, tz_offset=0):
    total = len(conversations)
    if not total:
        return {"error": "no conversations parsed"}

    depths, corrections, expansions = [], 0, 0
    correction_latencies, single_turn, ends_on_user = [], 0, 0
    hour_hist, weekday_hist = Counter(), Counter()
    per_source = Counter()
    corrected_titles = []

    for conv in conversations:
        turns = conv["turns"]
        depths.append(len(turns))
        per_source[conv["source"]] += 1

        user_turns = [t for t in turns if t["role"] == "user"]
        if len(turns) == 1:
            single_turn += 1
        if turns[-1]["role"] == "user":
            ends_on_user += 1

        # Corrections only count after the opening turn: turn 1 cannot correct anything.
        first_correction = None
        for pos, turn in enumerate(turns):
            if turn["role"] != "user" or pos == 0:
                continue
            if count_markers(turn["text"], CORRECTION_MARKERS):
                if first_correction is None:
                    first_correction = pos
            if count_markers(turn["text"], EXPANSION_MARKERS):
                expansions += 1
        if first_correction is not None:
            corrections += 1
            correction_latencies.append(first_correction)
            corrected_titles.append(conv["title"][:80])

        for turn in user_turns:
            if turn["ts"]:
                local = turn["ts"] + timedelta(hours=tz_offset)
                hour_hist[local.hour] += 1
                weekday_hist[local.strftime("%a")] += 1

    families = find_restart_families(conversations)
    restart_convs = sum(f["size"] for f in families)

    stamps = [c["created"] for c in conversations if c["created"]]
    date_range = None
    if stamps:
        date_range = [min(stamps).date().isoformat(), max(stamps).date().isoformat()]

    return {
        "mode": "chats",
        "total_conversations": total,
        "by_source": dict(per_source),
        "date_range": date_range,
        "depth": {
            "mean": round(statistics.mean(depths), 1),
            "median": statistics.median(depths),
            "max": max(depths),
            "single_turn_pct": round(100 * single_turn / total, 1),
        },
        "specification_gap": {
            "corrected_conversations": corrections,
            "correction_rate_pct": round(100 * corrections / total, 1),
            "median_turns_before_first_correction":
                statistics.median(correction_latencies) if correction_latencies else None,
            "examples": corrected_titles[:10],
        },
        "scope_expansion": {
            "total_expansion_markers": expansions,
            "per_conversation": round(expansions / total, 2),
        },
        "abandonment": {
            "ends_on_user_turn": ends_on_user,
            "ends_on_user_pct": round(100 * ends_on_user / total, 1),
        },
        "restarts": {
            "families": len(families),
            "conversations_in_families": restart_convs,
            "restart_rate_pct": round(100 * restart_convs / total, 1),
            "unresolved_families": sum(1 for f in families if not f["resolved"]),
            "top": families[:15],
        },
        "circadian": {
            "by_hour": {str(h): hour_hist.get(h, 0) for h in range(24)},
            "by_weekday": dict(weekday_hist),
            "tz_offset_applied": tz_offset,
        },
        "topics": salient_topics(conversations),
    }


# --------------------------------------------------------------------------------------
# Mode: files
# --------------------------------------------------------------------------------------

def canonical_stem(name: str) -> str:
    """Strip version and finality tokens so `FINAL_report_v3.md` and `report.md` collide."""
    stem = Path(name).stem.lower()
    stem = VERSION_RE.sub("", stem)
    parts = re.split(r"[_\-. ]+", stem)
    kept = [p for p in parts if p and p not in FINALITY_TOKENS and not re.fullmatch(r"v?\d+", p)]
    return "_".join(kept) or stem


def analyse_files(root: Path, excludes):
    by_hash, by_stem = defaultdict(list), defaultdict(list)
    finality_hits, all_files = [], []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in excludes for part in rel.parts):
            continue
        if path.stat().st_size > 20_000_000:
            continue
        all_files.append(str(rel))

        low = path.name.lower()
        if any(tok in low for tok in FINALITY_TOKENS) or VERSION_RE.search(Path(low).stem):
            finality_hits.append(str(rel))

        if path.suffix.lower() in {".md", ".py", ".json", ".csv", ".txt", ".yaml", ".yml"}:
            try:
                digest = hashlib.md5(path.read_bytes()).hexdigest()
            except OSError:
                continue
            by_hash[digest].append(str(rel))
            # Key on extension too: `data.csv` and `data.json` are two formats of one export,
            # not two competing versions of one idea. Same for `export.md` next to `export.py`.
            by_stem[(canonical_stem(path.name), path.suffix.lower())].append(str(rel))

    duplicates = [{"paths": p} for p in by_hash.values() if len(p) > 1]

    # A family is only pathological if at least one member *claims* to supersede the others.
    # Two plain `SKILL.md` files in different skill folders is a naming convention, not churn.
    versioned = set(finality_hits)
    families = []
    for (stem, suffix), paths in by_stem.items():
        if len(paths) < 2 or not any(p in versioned for p in paths):
            continue
        families.append({"canonical": f"{stem}{suffix}", "count": len(paths), "paths": sorted(paths)})
    families.sort(key=lambda f: -f["count"])

    total = max(len(all_files), 1)
    return {
        "mode": "files",
        "root": str(root),
        "total_files": len(all_files),
        "finality_claims": {
            "count": len(finality_hits),
            "pct_of_corpus": round(100 * len(finality_hits) / total, 1),
            "paths": sorted(finality_hits)[:60],
        },
        "byte_identical_duplicates": {"groups": len(duplicates), "detail": duplicates[:25]},
        "version_families": {
            "count": len(families),
            "files_involved": sum(f["count"] for f in families),
            "top": families[:25],
        },
    }


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------

def bar(value, peak, width=28):
    if not peak:
        return ""
    return "█" * max(1, round(width * value / peak)) if value else ""


def render_chat_report(m):
    L = ["# Chat Forensics", "", "*Behavioural metrics derived from your own AI conversation history.*",
         "", f"- Conversations analysed: **{m['total_conversations']}**",
         f"- Sources: {', '.join(f'{k} ({v})' for k, v in m['by_source'].items())}"]
    if m.get("date_range"):
        L.append(f"- Date range: {m['date_range'][0]} to {m['date_range'][1]}")

    sg = m["specification_gap"]
    L += ["", "## 1. Specification gap", "",
          "How often a conversation contained you telling the model it had got the wrong end of the stick.",
          "This is the measurable version of *what I asked for vs. what I wanted*.", "",
          f"- **Correction rate: {sg['correction_rate_pct']}%** "
          f"({sg['corrected_conversations']} of {m['total_conversations']} conversations)",
          f"- Median turns before you noticed the mismatch: **{sg['median_turns_before_first_correction']}**"]
    if sg["examples"]:
        L += ["", "Sample threads containing a correction:", ""]
        L += [f"- {t}" for t in sg["examples"]]

    r = m["restarts"]
    L += ["", "## 2. Restart families", "",
          "Separate conversations that opened with near-identical requests — you asked the same",
          "question again because the first answer never became a durable artifact.", "",
          f"- **Restart rate: {r['restart_rate_pct']}%** "
          f"({r['conversations_in_families']} conversations across {r['families']} families)",
          f"- Families that never reached depth (all attempts shallow): **{r['unresolved_families']}**"]
    if r["top"]:
        L += ["", "| Times asked | Span (days) | Ever resolved | Representative title |",
              "|---:|---:|:---:|---|"]
        for f in r["top"][:10]:
            L.append(f"| {f['size']} | {f['span_days'] if f['span_days'] is not None else '—'} "
                     f"| {'yes' if f['resolved'] else '**no**'} | {f['titles'][0]} |")

    d, a, x = m["depth"], m["abandonment"], m["scope_expansion"]
    L += ["", "## 3. Depth, abandonment, scope", "",
          f"- Median conversation depth: **{d['median']} turns** (mean {d['mean']}, max {d['max']})",
          f"- Single-turn conversations: **{d['single_turn_pct']}%**",
          f"- Conversations ending on your turn (no reply consumed): **{a['ends_on_user_pct']}%**",
          f"- Scope-expansion markers per conversation: **{x['per_conversation']}**"]

    hours = {int(k): v for k, v in m["circadian"]["by_hour"].items()}
    peak = max(hours.values()) if hours else 0
    if peak:
        L += ["", "## 4. When your brain actually engages", "",
              f"User turns by hour (UTC{m['circadian']['tz_offset_applied']:+d}):", "", "```"]
        for h in range(24):
            L.append(f"{h:02d}:00 {bar(hours.get(h, 0), peak)} {hours.get(h, 0)}")
        L += ["```"]
        best = sorted(hours.items(), key=lambda kv: -kv[1])[:3]
        L += ["", f"Peak engagement hours: **{', '.join(f'{h:02d}:00' for h, _ in best)}**.",
              "Protect these. Route deep work here and administrative work everywhere else."]

    if m["topics"]:
        L += ["", "## 5. What you actually keep returning to", "",
              "Ranked by TF-IDF salience across your own prompts — not raw frequency, so common",
              "filler is suppressed and genuine preoccupations surface.", "",
              "| Term | Salience | Mentions | Conversations |", "|---|---:|---:|---:|"]
        for t in m["topics"][:20]:
            L.append(f"| {t['term']} | {t['score']} | {t['mentions']} | {t['conversations']} |")
        L += ["", "**Each of these deserves one wiki page.** That is the whole method: a term that",
              "appears across many separate conversations is a concept you are re-deriving from",
              "scratch every time. Give it an address and you stop paying that cost."]
    return "\n".join(L) + "\n"


def render_file_report(m):
    fc, dup, vf = m["finality_claims"], m["byte_identical_duplicates"], m["version_families"]
    L = ["# Corpus Forensics", "",
         f"*Structural metrics for `{m['root']}` — {m['total_files']} files.*", "",
         "## 1. Finality claims", "",
         "Files whose names assert they are the last word: `FINAL`, `PERFECTED`, `MASTER`, `_v3`.",
         "A high rate means each session declared victory and the next session disagreed.", "",
         f"- **{fc['count']} files ({fc['pct_of_corpus']}% of corpus)** carry a finality or version token.",
         "", "## 2. Byte-identical duplicates", "",
         f"- **{dup['groups']} groups** of files with identical content at different paths."]
    for g in dup["detail"][:10]:
        L += ["", "```"] + [f"  {p}" for p in g["paths"]] + ["```"]

    L += ["", "## 3. Version families", "",
          "Files that collapse to the same name once version and finality tokens are stripped.",
          "Each family is one idea stored in N places, with no page saying which one is true.", "",
          f"- **{vf['count']} families** covering **{vf['files_involved']} files**.", ""]
    if vf["top"]:
        L += ["| Canonical idea | Copies | Paths |", "|---|---:|---|"]
        for f in vf["top"][:15]:
            L.append(f"| `{f['canonical']}` | {f['count']} | {'<br>'.join(f['paths'][:6])} |")
    L += ["", "> Every family above is a wiki page waiting to exist. Pick the best copy, promote it",
          "> to `brain/`, and leave the rest as history. The point is not tidiness — it is that the",
          "> next session can find the answer instead of regenerating it."]
    return "\n".join(L) + "\n"


def write_topic_seeds(metrics, outdir: Path):
    """Emit one wiki stub per salient topic so the corpus starts populating itself."""
    if metrics.get("mode") != "chats" or not metrics.get("topics"):
        return []
    seeds = outdir / "seeds"
    seeds.mkdir(parents=True, exist_ok=True)
    written = []
    for topic in metrics["topics"][:12]:
        term = topic["term"]
        slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
        path = seeds / f"{slug}.md"
        if path.exists():
            continue
        path.write_text(
            f"# {term.title()}\n\n"
            f"*Auto-seeded from chat forensics. You raised this across "
            f"{topic['conversations']} separate conversations "
            f"({topic['mentions']} mentions) without ever writing it down once.*\n\n"
            f"## What I actually believe\n\n_Replace this. One paragraph, in your own words._\n\n"
            f"## Open questions\n\n- \n\n## Links\n\n- [[index]]\n\n"
            f"---\nstatus: seed\n", encoding="utf-8")
        written.append(str(path))
    return written


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["chats", "files"])
    ap.add_argument("path", type=Path, help="export directory (chats) or corpus root (files)")
    ap.add_argument("-o", "--outdir", type=Path, default=Path("brain/_forensics"))
    ap.add_argument("--tz-offset", type=int, default=0, help="hours from UTC for circadian map (e.g. -5)")
    ap.add_argument("--exclude", nargs="*", default=[".git", "node_modules", ".venv", "__pycache__"])
    args = ap.parse_args()

    if not args.path.exists():
        sys.exit(f"error: {args.path} does not exist")
    args.outdir.mkdir(parents=True, exist_ok=True)

    if args.mode == "chats":
        conversations, files_read, skipped = load_conversations(args.path)
        if not conversations:
            print(f"No conversations found under {args.path}.", file=sys.stderr)
            if skipped:
                print("Skipped:", file=sys.stderr)
                for s in skipped[:10]:
                    print(f"  - {s}", file=sys.stderr)
            print("\nDrop your Claude/ChatGPT `conversations.json` in there and re-run.", file=sys.stderr)
            sys.exit(1)
        for f in files_read:
            print(f"  read {f}")
        metrics = analyse_chats(conversations, tz_offset=args.tz_offset)
        report = render_chat_report(metrics)
    else:
        metrics = analyse_files(args.path, set(args.exclude))
        report = render_file_report(metrics)

    (args.outdir / "metrics.json").write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    report_path = args.outdir / f"{args.mode}_report.md"
    report_path.write_text(report, encoding="utf-8")
    seeds = write_topic_seeds(metrics, args.outdir)

    print(f"\n  metrics -> {args.outdir / 'metrics.json'}")
    print(f"  report  -> {report_path}")
    if seeds:
        print(f"  seeds   -> {len(seeds)} topic stubs in {args.outdir / 'seeds'}")


if __name__ == "__main__":
    main()
