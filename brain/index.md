# Index

**This is the hub. Every session starts here — human or agent. If something durable is not
reachable from this page, it does not exist.**

---

## Start here

New to this, or coming back after a gap? Read in this order:

1. **[[claude-layers]]** — the nine layers of Claude, ranked by what actually persists. Where you
   are strong, where the gap is.
2. **[[wiki-method]]** — why these are wiki pages and not documents, and what that buys.
3. **[[ai-medicine-rosetta]]** — p-values, loss functions, weights: your analogy made rigorous, plus
   the one flaw in the plan.
4. **[[adhd-operating-system]]** — the design rules, and why they remove remembering steps rather
   than asking for discipline.
5. **[[anti-versioning]]** — why no filename here says `FINAL`.
6. **[[handoff]]** — what a finished output looks like when it reaches him. Read this before
   writing anything back to him.

## Concepts

| Page | What it settles |
|---|---|
| [[claude-layers]] | What each layer of the stack does and how long it remembers |
| [[wiki-method]] | Why a page beats a transcript for retrieval |
| [[ai-medicine-rosetta]] | Medicine ↔ AI translations; the derivation/validation trap |
| [[adhd-operating-system]] | Initiation, single address, one-next-action, the scope valve |
| [[anti-versioning]] | Plain-noun filenames; how to promote existing work |
| [[handoff]] | Artifact or PDF, three lines beside it, diagrams over prose |

## Projects

| Page | State |
|---|---|
| [[second-brain]] | Active — this system. Spine built; automation not yet. |

Add a page here for each real effort, using `_templates/project.md`. A project page does not hold
the work; it points at wherever the work actually lives and says what state it is in.

## People

One page per recurring person, from `_templates/person.md`. Deliberately empty for now — the
existing entity registry in `analysis-output/perfected/SECOND_BRAIN_ARCHITECTURE.md` already holds
canonical names, aliases and relationships. Promote from there as each becomes relevant rather than
bulk-importing.

## Decisions

Append-only. One page per decision that would be expensive to revisit, using
`_templates/decision.md`. Record the date, what was chosen, what was rejected, and why.

**Still owed:** the loss function. What "good" means for this system, in one line. See
[[ai-medicine-rosetta]] — nearly every other setting is downstream of it.

## Sessions

`sessions/` — one short entry per working session, from `_templates/session.md`. What was asked,
what was actually produced, the single next action. This is what lets a future session pick up
mid-thought instead of restarting.

- [[2026-07-26-claude-layers-and-wiki-method]] — the session that built this.
- [[2026-08-08-handoff-contract]] — the output rules, and the layers redrawn as figures.

## Measurements

`_forensics/` — generated, never hand-edited.

| File | What it measures |
|---|---|
| `files_report.md` | Version families, finality claims, duplicates in this repository |
| `chats_report.md` | Specification gap, restarts, abandonment, circadian pattern — once exports are in `ingest/` |
| `graph.md` | The link topology of this brain |

Regenerate:

```bash
python3 tools/corpus_forensics.py files . -o brain/_forensics
python3 tools/corpus_forensics.py chats ingest/ -o brain/_forensics --tz-offset -5
python3 tools/wiki_lint.py brain --mermaid brain/_forensics/graph.md
```

## History

Everything at the repository root outside `brain/` and `tools/` is prior work: health analyses,
legal strategy, prompt collections, seven skills. It is real and much of it is good. It is not
canonical and it is not organised. Cite it, promote from it, do not duplicate it.

The promotion queue is in [[second-brain]].

---

## The one next action

**Make this repository private.** Confirmed public on 2026-07-26, with case material and clinical
data tracked in it. Thirty seconds in Settings → General → Danger Zone. Full context and the
follow-on decisions are item 0 in [[second-brain]].

Then, and only then: add the Monday routine. That is the highest-leverage build step remaining, and
it is about fifteen minutes.
