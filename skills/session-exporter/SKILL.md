---
name: session-exporter
description: >
  Archives a Claude conversation into a complete, portable package for external audit or
  reconstruction: a structured JSON record, a readable Markdown narrative, an interactive
  HTML artifact, a paginated PDF report, and a SQL (SQLite) dump — all built from the same
  underlying data so every format tells the same story. Use whenever the user asks to
  export, archive, capture, or dump "everything" from a conversation or session — their
  inputs, Claude's outputs, the reasoning deltas between what they asked and what they
  meant, and the artifacts produced — especially when the stated goal is for someone else
  (a collaborator, a future session, an outside analyst) to review the work in detail or
  rebuild it faithfully. Also trigger on "export this session", "give me everything from
  this conversation", "package this up for someone to review", or a request for a session
  in multiple formats (PDF + JSON + Markdown + SQL, or "every format you can").
---

# Session Exporter

Most conversation exports are a raw transcript dump — useful to nobody, because the signal
(what was actually decided, and why) is buried in the noise (pleasantries, tool-call
plumbing, retries). This skill produces the opposite: a **reconstructed, structured**
record, built the same way a physician writes a discharge summary rather than pasting the
raw nursing notes — same underlying events, organized so a stranger can pick it up and
understand the case.

## The one rule that matters: don't fabricate, label reconstruction as reconstruction

You have real access to this conversation's turns — the user's actual words, the tool
calls you actually made, the files you actually wrote. You do **not** have access to your
own past hidden reasoning tokens from earlier turns (the harness does not replay them back
into context) — only to what you *exposed*, i.e. any Supporting Analysis table you produced,
plus the actions you took. When you write a "reasoning" or "thinking" field for a turn that
had no exposed analysis, write it as an honest reconstruction from the visible trail
(what you did, in what order, and why that's the likely reason) and say so. Never present
a reconstruction as if it were a verbatim internal log — that's the same discipline as
never presenting inference as retrieval.

Capture failures too. A tool call that errored, a permission that was denied, a scheduling
attempt that silently didn't fire — these are not embarrassments to omit, they are exactly
the "gap between what was asked and what the system delivered" that a second-brain method
(chat-archive mining) is built to find. Include them plainly.

## Workflow

### 1. Reconstruct the turn-by-turn record

Walk the conversation from its start (or from wherever the user says to start) and build one
entry per turn with:

- **user_input** — the user's message, verbatim if short, faithfully summarized if long (never
  paraphrase away specifics like numbers, names, or exact phrasing that carried intent)
- **assistant_actions** — what you actually did: skills loaded, files written, commands run,
  tools called (including ones that failed — record the error)
- **assistant_output** — the substance of what you handed back
- **intent_delta** — literal ask vs. true objective vs. what was delivered, one line each; skip
  this field entirely for trivial turns rather than padding it
- **artifacts_produced** — file paths, URLs, PR links, commit hashes — anything durable that
  came out of the turn
- **supporting_analysis** — if the turn produced a real Supporting Analysis table (or
  equivalent exposed reasoning), carry it over verbatim; if not, write a short reconstruction
  and label it `"reconstructed": true`

Write this as `session-data.json` first — it is the single source of truth. Every other
format is a rendering of it, not an independent retelling; if a fact needs to change, change
it in the JSON and regenerate.

### 2. Derive the other four formats from the JSON

- **Markdown narrative** (`session-narrative.md`) — one section per turn, in reading order.
  This is the fastest format for a human to skim top to bottom.
- **Interactive HTML artifact** — a single self-contained page, one turn per expandable
  section, with the intent-delta and any diagrams pulled inline. Load the `artifact-design`
  and, if the session produced diagrams worth re-showing, `artifact-diagramming` skills before
  building it — this is a deliverable in its own right, not a debug dump, and deserves the
  same typographic care as any other artifact. Match the visual language already established
  in the session if one exists (reuse the palette/type choices from artifacts already produced
  this session) rather than inventing a new one — continuity across a body of work reads as
  intentional. Publish it with the Artifact tool when the runtime supports that; otherwise save
  it as a plain file in the export folder.
- **PDF report** (`report.pdf`) — build a second, print-tuned HTML file (no JS interactivity,
  everything expanded, explicit page-break CSS, running header/footer) and render it with a
  headless browser rather than a text-to-PDF library — it gives real typography for free.
  Use `scripts/render_pdf.sh <input.html> <output.pdf>`, which shells out to the
  Playwright-bundled Chromium already present in this environment
  (`/opt/pw-browsers/chromium-*/chrome-linux/chrome --headless --print-to-pdf`). Check that
  path exists first; if this environment has no bundled Chromium, fall back to whatever HTML→PDF
  path the `pdf` skill documents rather than failing silently.
- **SQL dump** (`session-export.sql` + `session-export.db`) — run
  `scripts/build_sql.py session-data.json --out-dir <export-folder>`. It defines a normalized
  schema (`sessions`, `turns`, `analysis_rows`, `artifacts`, `tool_failures`) and emits both a
  portable `.sql` text dump (for version control / review) and a queryable SQLite `.db` file.
  Don't hand-roll a different schema per export — the point of the fixed schema is that two
  exports from two different sessions are diffable and joinable.

### 3. Package and place it

Everything lands in one folder, named `<date>-<short-slug>` (e.g.
`2026-09-04-claude-layers-second-brain`), containing the five artifacts above plus a short
`README.md` that tells an outside reader what each file is and where to start (usually: read
the Markdown narrative for the story, open the JSON if you need to reprocess the data
programmatically, use the interactive HTML if you're the original user, use the PDF if you're
handing this to someone who wants a static document, use the SQL if you're going to query
across many sessions later).

If the project has a wiki (per the standing wiki protocol), add one short pointer page in
`05_SYSTEMS/` noting that this export exists and what it covers — the export folder itself is
raw archival material, not a wiki page, so it does not go in the wiki taxonomy; only the
pointer does. Link it from the relevant Map of Content.

## What NOT to do

- Don't run this as a token-maximizing exercise — a five-turn session should not produce a
  50-page PDF. Density over length, same as any other deliverable to a time-pressed reader.
- Don't silently drop turns that look like plumbing (a failed tool call, a system-triggered
  check-in). If it happened in the session, it belongs in the record; compress it, don't erase
  it.
- Don't invent timestamps, model names, or hashes you don't actually have. Mark unknowns as
  unknown rather than filling them in plausibly.
