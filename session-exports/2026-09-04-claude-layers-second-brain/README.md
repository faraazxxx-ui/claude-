# Session Export — Claude Layers & Second Brain

Full archival record of the session that built `wiki/00_INDEX/` and `wiki/05_SYSTEMS/` in this repo (2026-08-07 through 2026-09-04). Produced by the `skills/session-exporter` skill; see that skill's `SKILL.md` for the general method.

## Files in this folder

| File | What it is | Read this if you... |
|---|---|---|
| `session-data.json` | The structured source of truth — every other file is rendered from this | ...need to reprocess the record programmatically, or verify a claim |
| `session-narrative.md` | Human-readable turn-by-turn account | ...want the story, fastest, top to bottom |
| `interactive-review.html` | Self-contained interactive artifact — expandable turn cards, the central-delta diagram | ...are the original user, or want to browse it in a browser |
| `print-report.html` | Print-tuned source for the PDF (everything expanded, paginated CSS) | ...want to see what the PDF was rendered from, or re-render it |
| `report.pdf` | Paginated PDF, rendered from `print-report.html` via headless Chromium | ...want a static document to hand to someone else |
| `session-export.sql` | Portable SQL text dump (schema + INSERTs), SQLite-compatible | ...want to review the data as version-controlled text, or load it into another database |
| `session-export.db` | The same data as a queryable SQLite database | ...want to query it directly, or join it against another session's export later |

## Schema (SQL / JSON, same shape)

Five tables, fixed on purpose so exports from different sessions are diffable and joinable:

- **sessions** — one row: repo, branch, PR, user, model
- **turns** — one row per turn: trigger, input, output, intent-delta fields
- **assistant_actions** — ordered list of what was actually done, per turn
- **analysis_rows** — the exposed Supporting Analysis tables (or, where none existed, a labeled reconstruction), per turn
- **artifacts** — every durable file, URL, commit, and PR produced, per turn
- **tool_failures** — every failed tool call, its error, and its resolution (or lack of one)

## The one fact worth reading even if nothing else in this folder gets opened

The session's central delta (full detail in `session-narrative.md` and the JSON's `cognitive_model_delta` key): personal-data retraining was the intuition; wiki-page retrieval into the context window is the actual mechanism, because the model's weights are frozen and nothing typed into a chat changes them. Every wiki page and diagram this session produced is that correction, built out.

## Provenance and honesty note

This is a reconstruction, not a raw transcript dump. The user's inputs and the assistant's actions are represented faithfully; anywhere reasoning is reported for a turn that produced no exposed Supporting Analysis table, it is marked as a reconstruction from the visible action trail — never presented as a verbatim internal log. Failed tool calls (a wrong tool name, a denied approval, a stalled scheduling attempt) are included rather than cleaned up, on the same principle the session's own Chat Archive Mining page argues for: the gaps are the signal.
