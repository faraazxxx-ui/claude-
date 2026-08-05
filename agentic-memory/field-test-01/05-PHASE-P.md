# Phase P — Prospective (Field Test #1, Round 2)

**What this is:** the three prompts you are most likely to need next, each drafted loop-shaped and ready to paste. Every prediction is grounded in a named pattern or note — no orphan predictions.

**Honesty flag on method:** the mission specified Phase P should run in fresh context from the handoff card and notes only. You instructed "automatically proceed to next step," so it ran **in-thread**, with the raw conversations still in view. That raises the risk of over-fitting to specifics I have just read rather than to durable patterns. Treated as a **Medium**-confidence forecast for that reason — a fresh-context run would be the cleaner test.

**Pre-empted rather than predicted:** the highest-probability next ask in the whole corpus is *"now render this as a PDF / an artefact"* (P3, N24 — the reflexive second move in 6 of 8 conversations). Per P3's own fix, it ships in this pass instead of being predicted. That is the loop closing on itself.

---

## Prediction 1 — Scale the pipeline to the full corpus

**Why:** G1 is the named blocker and you already know it. P4 shows you scale a proven scaffold rather than re-designing it, and N30 shows this project has been running since October 2025 in one form or another. The natural next move after "the method works on 8" is "run it on everything."
**Confidence:** High.

```
Agentic Memory — Field Test #2. Run the Phase R pipeline over my full conversation export,
not a sample.

Outcome: every conversation in the export becomes atomic notes in the same schema as
agentic-memory/field-test-01/01-ATOMIC-NOTES.md, rolled into one pattern map and one gap list.

Done-when: (a) every conversation is either processed or listed as unprocessable with a reason;
(b) zero orphan claims — every claim names its source conversation; (c) each pattern states how
many conversations, platforms, domains and months it spans; (d) any pattern found in only one
domain is labelled as such.

Rounds: 2.

Before starting, inventory what is actually present and tell me what is missing. Do not fill gaps
to look complete. Prioritise conversations dated before October 2025 — that is the thinnest part
of the corpus. Output an artefact.
```

---

## Prediction 2 — Score and triage the pattern map

**Why:** P7 / N32 — every structured map you build gets a triage layer immediately afterwards: Loop Score with four bands (C2, C4), severity 90/100 (C8), Danger Radar (C6), Now / Next 2 / Later (C7). Four conversations, two domains, two platforms. A map without a score is, in your corpus, an unfinished map.
**Confidence:** High for the shape of the ask; Medium for the exact instrument you would want.
**Constraint carried from N31:** figures you computed from data are wanted; decimals invented by me are not. So this asks for counts and bands, not a composite score with a decimal point.

```
Take the Round 2 pattern map in agentic-memory/field-test-01/02-PATTERN-MAP.md and add a triage
layer.

Outcome: each pattern carries (a) how many conversations, platforms and domains it appears in —
counts, not estimates; (b) the observed cost in rounds or undelivered deliverables; (c) a band —
Act now / Monitor / Note only; (d) the single fix, in one line.

Done-when: the patterns are ordered by observed cost rather than by how interesting they are, and
every count traces to named conversations. No composite score, no decimals — bands and counts only.

Rounds: 1.

Then tell me which one fix I should make this week and what changes if I make it.
```

---

## Prediction 3 — Make the notes queryable

**Why:** N11 and N30 — the whole point of the second brain is retrieval, not note-taking. The BigQuery guide is already attached, the note-to-`documents` field mapping is already written in the handoff card, and the notes were built atomic specifically so they would load. The step after "notes exist" is "notes answer questions."
**Confidence:** Medium — this is the logical next step and the infrastructure is in place, but nothing in the corpus shows you actually running an ingest, so this is inference about intent rather than an observed pattern.

```
Turn the field-test-01 atomic notes into a working retrieval layer using the pipeline in
Personal_Data_Embedding_Living_AI_Guide.md.

Outcome: the notes exist as newline-delimited JSONL matching the guide's documents schema, ready
to load, with source, confidence and gap carried as metadata tags.

Done-when: (a) one JSONL row per note, validated against the guide's field list; (b) I can ask
"where does my approach stall?" and get back the specific notes with their source conversations;
(c) any step that needs my credentials or a manual console action is listed separately as a
handoff, not silently skipped.

Rounds: 2.

Flag every manual step and propose the automated route. Watson X stays deferred. No code in your
explanation to me unless I say "show code."
```

---

## What would make these predictions better

| Missing | Effect on the forecast |
|---------|------------------------|
| Your actual messages in C6–C8 (G10) | Three of eight conversations are inference-only; your *phrasing* — the best signal for predicting a prompt — is invisible in them |
| A fresh-context run | This forecast saw the raw material; a clean run from notes only would test whether the patterns predict or the specifics do |
| Any pre-2025 conversation | The one longitudinal data point (N30) came from a 5-month gap. Prediction quality scales with time span, not just volume |

**Self-check:** all three predictions cite named notes or patterns. None assumes a conversation, tool or intention not present in the corpus. Prediction 3 is explicitly labelled as inference about intent rather than an observed behaviour.
