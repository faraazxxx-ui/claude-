---
name: second-brain
description: >
  Read, extend, and measure Dr. Rahman's second brain in `brain/`. Use whenever the request touches
  the knowledge corpus, the wiki, or continuity between sessions: looking something up that was
  worked on before, writing a conclusion down so it persists, promoting a scattered file into a
  canonical page, checking link integrity or orphans, running chat or corpus forensics, or asking
  what to work on next. Also use when the user asks about the second brain, the wiki method, how
  Claude's layers fit together, the specification gap, restart or version churn, or how to stop
  rebuilding the same work. Trigger on "second brain", "the wiki", "brain/", "what was I doing",
  "have I done this before", "write this down", "make this stick", "forensics", "what should I work
  on", or when a session is ending and something durable was produced.
---

# Second brain

The corpus in `brain/` is Layer 8 — the only layer of the stack that persists and compounds. This
skill is how you read and extend it. The reasoning behind it is in `brain/concepts/wiki-method.md`;
the stack model is in `brain/concepts/claude-layers.md`.

## Before anything else

Read `brain/index.md`. Then search `brain/` for the topic:

```bash
grep -ril "<topic>" brain/
```

If a page exists, **update it**. If not, create one. Never open a new top-level directory, and never
put `FINAL`, `PERFECTED`, `MASTER`, or `_v2` in a filename — see `brain/concepts/anti-versioning.md`
for why this repository already contains four generations of the same health report.

## Creating a page

Copy the matching template from `brain/_templates/` — `concept`, `project`, `person`, `decision`, or
`session`. Then:

- **Answer first.** Bold two or three sentences at the top that carry the whole point. A page that
  has to be read to the bottom will not be read.
- **One idea.** If the title needs "and", it is two pages.
- **Under a thousand words.** Longer means it is an index; split and link.
- **Separate evidence from inference.** He is a physician and will act on this. Mark what is
  measured, what is inferred, what is assumed.
- **Give it an inbound link in the same session.** Add it to `brain/index.md` or a parent page. An
  orphan page does not exist.
- **Plain-noun filename.** `health-analysis.md`, never `PERFECTED_HEALTH_REPORT_v4.md`.

## Promoting existing work

The repository root holds a lot of good work from prior sessions, scattered and duplicated. The
queue is in `brain/projects/second-brain.md`. One per session, as background work:

1. Pick the best copy in the family.
2. Create the canonical page in `brain/` with a plain-noun name.
3. State what it supersedes; link the originals.
4. **Leave the originals in place.** Promotion is reversible; deletion is not.

## Measuring

```bash
# Version churn, finality claims, duplicates in this repository
python3 tools/corpus_forensics.py files . -o brain/_forensics

# Specification gap, restarts, abandonment, circadian pattern (needs exports in ingest/)
python3 tools/corpus_forensics.py chats ingest/ -o brain/_forensics --tz-offset -5

# Broken links, orphans, hubs, staleness; non-zero exit on broken links
python3 tools/wiki_lint.py brain --mermaid brain/_forensics/graph.md
```

Chat forensics output is **diagnosis, not prescription**. It describes how he has worked, which
includes every abandoned thread and restart. Do not treat it as a target to imitate — the
derivation/validation reasoning is in `brain/concepts/ai-medicine-rosetta.md`.

## Ending a session

All three, before you finish:

1. Update or create the canonical page for what you worked on.
2. Append an entry to `brain/sessions/` from `brain/_templates/session.md`. Record **asked** vs
   **wanted** separately when they differed — that gap, logged one instance at a time, is the most
   useful signal in the corpus.
3. Run `python3 tools/wiki_lint.py brain` and fix any link you broke.

If nothing was written into `brain/`, the session did not happen.

## How to answer him

- Conclusion first, reasoning underneath.
- **One** next action, never a menu. A list of options is a decision, and decisions are the
  expensive currency here.
- Finish what you start. A half-built thing becomes another directory he has to remember.
- Say plainly when something is uncertain or when you did not do part of it.
