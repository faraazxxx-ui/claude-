# Second brain

**State: spine built, automation missing. The corpus can now be read and written by every session.
Nothing yet reads it without being asked — that is the next step and it is the one that matters.**

Owner: Dr. Rahman · Started: 2026-07-26 · Supersedes:
`analysis-output/perfected/SECOND_BRAIN_ARCHITECTURE.md` (retained as history; its entity registry
and 13-domain taxonomy are still the best in the corpus and should be promoted, not rewritten)

---

## What this is

A durable corpus that every Claude session reads before working and writes to before finishing, so
that work compounds instead of restarting. The reasoning is in [[wiki-method]]; the stack position
is Layer 8 in [[claude-layers]].

## Done

- `CLAUDE.md` at the repository root. Every Claude Code session now loads it automatically, before
  the first instruction. This is the piece that was missing — its absence is why twelve sessions in
  a row each opened a new top-level directory.
- `brain/` with hub, concepts, templates, and the session protocol.
- `tools/corpus_forensics.py` — measures the specification gap from chat exports, and version churn
  from a file corpus. Both modes tested.
- `tools/wiki_lint.py` — broken links, orphans, hubs, staleness, Mermaid graph. Non-zero exit on
  broken links, so it can gate a commit.
- Baseline measurement of this repository in `brain/_forensics/`.

## Next — in order

### 0. Repository visibility — do this before anything else

**Confirmed 2026-07-26: `faraazxxx-ui/claude-` is public.** It has been since 2026-02-08.

18 tracked files contain third-party names or active-case references, including litigation strategy
under `legal-endeavors/references/`. A further 14 files hold personal clinical data under
`health_analysis_v2/`, `autonomic_intelligence_v3/` and `clinical_report_v4/`. No credentials or API
keys are present — that was checked separately and is clean.

Exposure appears low: 0 forks, 0 stars, 0 watchers.

Remediation, in order:

1. **Flip to private.** Settings → General → Danger Zone → Change visibility. Thirty seconds, and it
   stops any further exposure immediately.
2. **Understand what that does not fix.** Anything already cloned stays cloned, and public forks
   survive — there are none here, which is the good news. Cached copies may persist for a while.
3. **Deleting the files later will not remove them.** Git retains full history; a later `rm` leaves
   the content in every prior commit. Purging genuinely requires history rewriting
   (`git filter-repo`) and a force push, which breaks every existing clone. Decide whether that is
   warranted *after* step 1, not under time pressure.
4. **Then decide the split.** Method and tooling can stay in a public repository. Case material and
   clinical data should live in a private one. That separation is worth making deliberately rather
   than by default.

This outranks every other item on this page. Nothing below matters if it is skipped.

### 1. The Monday routine (~15 min, highest leverage)

The proactive layer. Without it, everything here still waits on you to initiate, which is the exact
step [[adhd-operating-system]] says not to depend on.

In Claude Code, ask for a scheduled Routine, Mondays 07:00 America/New_York, that reads
`brain/index.md`, `brain/sessions/` and open decisions, then produces **three sentences**: what was
left unfinished, what has become urgent, and the single thing to do today. It should append its
output to `brain/sessions/` so the briefings themselves accumulate into a record.

Three sentences. Not a dashboard. A dashboard is a menu, and a menu is a decision.

### 2. Write down the loss function (~10 min, blocks everything downstream)

One line in `brain/decisions/`: what "good" means for this system. The candidates and the reasoning
are in [[ai-medicine-rosetta]]. The recommended answer is *surface the one thing that unblocks the
next ninety minutes* — a precision objective, which means the system's job is to discard nearly
everything.

Retrieval threshold, briefing length, and what earns a page are all consequences of this line. It
cannot be delegated.

### 3. Consolidate the skills (~1 hr)

Seven skills across two directories. `skill/` and `skills/` both exist; `skill/references/` and
`skill/health-data-analyst/references/` hold byte-identical copies of the same two files.

Merge into `.claude/skills/`, one folder per skill, and point every reference at `brain/` instead of
at a private copy. Seven instruments become one system. Nothing needs rewriting — only moving and
re-pointing.

### 4. Run the chat forensics (~20 min, mostly waiting on exports)

Export from claude.ai (Settings → Privacy → Export data) and ChatGPT (Settings → Data controls →
Export data). Both arrive by email as a zip containing `conversations.json`. Unzip into `ingest/`
and run:

```bash
python3 tools/corpus_forensics.py chats ingest/ -o brain/_forensics --tz-offset -5
```

This produces the analysis you actually asked for: correction rate as a measure of the gap between
what you requested and what you wanted, restart families, abandonment, and your circadian
engagement curve. It also seeds a stub page for every topic you have raised across many separate
conversations without ever writing down once.

Treat the output as **diagnosis only** — see the derivation/validation warning in
[[ai-medicine-rosetta]].

### 5. Promotion queue (ongoing, one per session)

Each version family below is one idea currently stored in several competing files. Promote the best
copy to a plain-noun page in `brain/`, state what it supersedes, link the originals, leave them in
place. One per session — this is background work, not a project.

| Idea | Copies | Where |
|---|---:|---|
| `red-team-review` | 4 | `daily-note-ai-integration/`, `health_analysis_v2/`, `optimized-prompts/`, `prompts/` |
| `health-analysis` | 4 | `health_analysis/`, `health_analysis_v2/`, `autonomic_intelligence_v3/`, `clinical_report_v4/` |
| `prompts` | 3 | `daily-workflow-optimizer/`, `prompts/` ×2 |
| `master-report` | 3 | `analysis-output/` ×2, `health_analysis_v2/` |
| `ghusoon-prompts` | 2 | `optimized-prompts/` |
| `entity-registry` | 1 | `analysis-output/perfected/` — promote first, everything else references it |

## How we will know it worked

Re-run both forensics modes monthly. Falling numbers mean the corpus is being read:

- Version families and finality-claim rate (currently 5 families, 12.0%) → down
- Restart rate and correction rate from chats → down
- Orphan pages from `wiki_lint.py` → down

If they do not move, the write-back step is being skipped. That is a `CLAUDE.md` problem, not a
concept problem.

## Open question

Whether to split this into two repositories — a public one for method and tooling, a private one
for case and clinical material — or make the whole thing private. Resolve it as part of item 0.

## Links

- [[index]] · [[claude-layers]] · [[wiki-method]] · [[ai-medicine-rosetta]] · [[adhd-operating-system]] · [[anti-versioning]]
