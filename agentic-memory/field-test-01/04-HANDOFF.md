# HANDOFF CARD — Agentic Memory, Field Test #1 (Round 2 complete)

**Goal:** Turn exported AI-conversation history into atomic notes + a pattern map + a gap list, every claim traceable, feeding a BigQuery/RAG second brain.

**Done-when:** A batch yields the three artefacts, zero orphan claims, all missing data named. → **Met for 8 conversations. Not met for the ~50-conversation target.**

**What Round 2 changed:** 3 ChatGPT/legal/Oct-2025 conversations joined 5 Claude/health/Mar-2026 ones. Cross-checking became possible for the first time — 5 of 7 patterns replicate across two platforms and two domains, which largely retires the "is this him or the model?" doubt (N29). Two patterns promoted, two new, one reframed.

**The finding worth acting on:** the stall is a **missing stop rule on either side**, not impatience. He loops because "perfect" has no exit test (N01); the assistant loops because one question has no default (N26, N27 — 4 documents never delivered in C8, 5 confirmation round-trips in C7). Same defect, opposite directions. Ask-then-wait is the most expensive stall in the corpus and the only one the responder can fix alone.

**Decisions:** scoped to what exists; Process/Content note split retained; legal content recorded as declared-not-adjudicated with no legal opinion attached; Phase P run **in-thread** on instruction ("automatically proceed"), flagged as Medium confidence for that reason.

**Open:** G10 (his messages absent from C6–C8) and G1 (42 conversations missing) are the blockers. G11 (deliverables promised, absent in 4 of 8) blocks confirming N28.

## Artefacts

| File | Contents |
|------|----------|
| `00-INVENTORY.md` | 8 conversations + 2 reference files, what is missing |
| `01-ATOMIC-NOTES.md` | 34 notes, N01–N34 |
| `02-PATTERN-MAP.md` | 7 patterns, deltas, stall points ordered by observed cost |
| `03-GAP-LIST.md` | G1–G12 + fixes |
| `05-PHASE-P.md` | 3 predicted next prompts, loop-shaped, paste-ready |
| `06-INGEST.md` | Note → `documents` field mapping, validation result, the credential handoff |
| `notes.jsonl` | 34 BigQuery-ready rows. Validation PASS, zero orphan claims |
| `schema.json` | The guide's Stage 2.2 field list, verbatim, for `bq load` |
| `build_jsonl.py` | Regenerates both from the markdown, so the notes stay the single source of truth |
| `field-test-01.html` | The interactive artefact — published, and the PDF source |
| `field-test-01.pdf` | Print version |

**Two of the three Phase P predictions were executed rather than left as forecasts:** the triage layer (counts, observed cost, band, fix) is built into the pattern cards, and the notes are queryable — the artefact carries a working search panel that answers "where does my approach stall?" from the 34 notes with sources attached. Prediction 1 is blocked on exports only he can produce.

## How these notes feed BigQuery (reference, not a rebuild)

Per `Personal_Data_Embedding_Living_AI_Guide.md`. Each atomic note maps to one `documents` row:

| Note field | BigQuery `documents` field |
|------------|----------------------------|
| N-id | `document_id` |
| note title | `title` |
| note body | `content` |
| — | `source_type` = `"chat"` |
| domain (health / legal / meta) | `life_domain` |
| source (C1–C8) | `metadata.source` |
| platform (Claude / ChatGPT) | `metadata.tags` += `platform:claude` / `platform:chatgpt` |
| confidence band | `metadata.tags` += `conf:high` / `conf:medium` |
| gap flag present | `metadata.tags` += `gap` |
| — | `metadata.triage_category` = `behavioral-map` |

No embeddings generated here — that is the pipeline's job. **Watson X stays deferred** (nothing in the stack supports it, per brief).

## Next session

Round 2 of 2 is spent. Do **not** re-open this thread to improve it (anti-resonation). Three clean starts, in this order of value:

0. **Load the JSONL** — `06-INGEST.md` lists the four steps that need your Google Cloud credentials: bucket + dataset, IAM, `gsutil cp` then `bq load`, then embeddings. Everything before that boundary is done and validated.

1. **Fix the corpus, then scale** — re-export C6–C8 with user turns (G10), then add the remaining ~42, oldest first (G1). Prompt is drafted in `05-PHASE-P.md`, Prediction 1.
2. **Fresh-context Phase P** — the honest version of the forecast, run from the notes alone:

> **Phase P — Prospective, fresh context.** Load only `04-HANDOFF.md`, `01-ATOMIC-NOTES.md` and `02-PATTERN-MAP.md` from `agentic-memory/field-test-01/`. Do not read the source conversations. From the notes and pattern map alone, predict my 3 most likely next prompts. Draft each loop-shaped (Outcome / Done-when / Rounds), ready to paste. Ground every prediction in a named pattern or note — no orphan predictions. Flag anything you are inferring. Then compare your three against `05-PHASE-P.md` and tell me where an in-thread run over-fitted. Stop with a handoff card.

## Self-grade (Exit protocol)

- **Vulnerability:** that C6–C8 tell us what *he* did. His turns are missing, so those claims rest on the assistant's readback of him. Named as G10 and carried on every affected note.
- **Ambiguity:** "pattern map" could read as clinical, and the legal notes could read as findings of fact. Both labelled at the top of every file — behavioural, hypothesis-generating; declared, not adjudicated.
- **Inefficiency:** the content notes (N15–N18, N33) remain lower-value than the process notes for this outcome. Kept, clearly marked unverified, so they cannot masquerade as findings.
- **Done-when:** **Partial pass.** Three artefacts plus Phase P, zero orphan claims, gaps named — on 8 conversations, not ~50, across 5 months, not 5 years.

**Verdict:** PASSES for "prove the pipeline and cross-check it on a second platform and domain." Does **not** pass the literal ~50-conversation done-when. The method is now validated; the corpus is the constraint.
