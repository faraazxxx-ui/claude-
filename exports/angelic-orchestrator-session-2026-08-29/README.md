# Export: Angelic-Orchestrator Voice-Capture Session

**Session span:** 2026-08-29 → 2026-11-12 · **Generated:** 2026-11-12/16 · **Repo:** faraazxxx-ui/claude- · **Branch:** claude/angelic-orch-db2nuf · **PR:** [#30](https://github.com/faraazxxx-ui/claude-/pull/30)

Full export of the conversation that verified a whisper.cpp dictation briefing, built `skills/voice-capture-setup/` and the `spine/` framework, ran an independent cross-model verifier pass, and then exported itself — at Dr. Rahman's request, in his own words:

> Export all the data including the thinking, my inputs and your outputs, the deltas, the artifacts, your thinking vs my thinking and everything which you can extract for the in a PDF, /artifact, json, markdown and SQL format and output it into a folder with the goal for it to be analyzed by others in order for it to be broken down in detail and re-created to its utmost accuracy.

## Files

| File | Format | What it holds |
|---|---|---|
| `transcript.md` | Markdown | The human-readable master. Every turn, the delta table, the thinking-vs-thinking comparison, gate grades, open items, commits, full source documents, and full current contents of every artifact file. |
| `transcript.json` | JSON | The same data, structured — `meta`, `commits`, `turns`, `deltas`, `thinking_comparison`, `gate_grades`, `open_items`, `source_documents`, `artifacts`. Machine-readable; this is what the Artifact viewer and the SQL dump are both generated from. |
| `transcript.sql` | SQL (SQLite-flavored) | `CREATE TABLE` + `INSERT` for 9 normalized tables mirroring the JSON. Loads cleanly in any standard SQL engine — validated against Python's `sqlite3` at build time. |
| `transcript.pdf` | PDF | `transcript.md` rendered via pandoc → styled HTML → headless Chromium print-to-PDF. ~46 pages. No external service touched — rendering stayed local, consistent with this session's own privacy stance. |
| `artifact_source.html` | HTML | Source of the published interactive viewer (see below). Fetches a sibling `transcript.json` at runtime — copy both files together to run it standalone. |
| `data.py` | Python | The actual single source of truth: the narrative content (turns, deltas, thinking-comparison, gate grades, open items, source documents) as a literal data structure. |
| `build.py` | Python | Reads `data.py`, reads the 10 artifact files **live from the repo** (not copied by hand), and renders `transcript.{md,json,sql}`. Re-run it after any future change to regenerate all three in lockstep — this is what keeps the formats from drifting apart. |

**Published Artifact (interactive viewer):** https://claude.ai/artifact/4vbLr9ktznCz4knMNARqjk — not re-fetchable from outside Claude; `artifact_source.html` + `transcript.json` is the durable copy of it.

## Why five formats stay in sync

`build.py` is the only thing that writes `transcript.md`, `transcript.json`, and `transcript.sql`. All three come from one in-memory dict (`data.py`'s content plus a live read of the repo's artifact files). The PDF is a straight render of `transcript.md`. The Artifact fetches `transcript.json` directly. Nothing downstream was hand-edited after generation — if something here looks wrong, the fix belongs in `data.py` or `build.py`, re-run, not in the output files.

## Privacy note — read before sharing this folder onward

This folder's own subject matter (dictation tooling, the spine framework) isn't sensitive. It does contain Dr. Rahman's work email in git commit co-author trailers and in reproduced session metadata, because that's how attribution actually looked during the session — removing it would make the export less accurate, not more private. Since the stated goal for this folder is to be analyzed by others, treat that email as PII to redact **before** handing this folder to anyone outside Dr. Rahman's own control. It was left in here because this export's job is accuracy, not redaction — those are two different, separable tasks.

## Known gaps, carried from `transcript.md` §5

- `spine/goal.md` is still `STATUS: UNSET` (2.5 months unfilled as of this export).
- `sony_sync.sh` / `com.faraaz.sonysync.plist` have never been read by any session — only the install commands around them were verified.
- Nothing in `skills/voice-capture-setup/` has been installed on an actual Mac yet.
- The `angelic-orchestrator/` canonical-memory pack (commit `fb3bb92`, a separate session) has no independent-verifier pass yet — the same Gate-4 gap this session's turn 5 closed for `SKILL.md` is open for that pack.

## Regenerating

```bash
cd exports/angelic-orchestrator-session-2026-08-29
python3 build.py        # rewrites transcript.md / .json / .sql from data.py + live repo files
```

PDF and Artifact regeneration are manual follow-ups (pandoc + headless Chromium; Artifact tool publish) — not wired into `build.py`, since both need tools outside plain Python.
