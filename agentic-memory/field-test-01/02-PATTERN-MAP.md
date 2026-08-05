# Phase R — Pattern Map (Field Test #1, Round 2)

**What this is:** a behavioural map — a symptom diary of *how he works with AI*, built only from the atomic notes. **Hypothesis-generating, not diagnostic.** Every pattern lists the notes it rests on; nothing here is un-sourced.
**What this is NOT:** a claim about his health, his neurology, the merits of his litigation, or the ~42 conversations not in this batch.

**What changed in Round 2:** three ChatGPT/legal conversations from Oct 2025 joined five Claude/health conversations from Feb–Mar 2026. Patterns that appear on both platforms and in both domains are now separable from one model's habits (N29). Two patterns were promoted, one was reframed, two are new.

## The seven patterns

| # | Pattern | Evidence | Cross-checked? | Confidence |
|---|---------|----------|----------------|-----------|
| **P6** | **Clarifying questions are the main stall** — ask-then-wait costs rounds and sometimes kills the thread; he has explicitly asked for initiative instead | N06, N25, N26, N27, N28 | Both platforms, both domains | **High** |
| **P1** | **Loops without a stop rule, in both directions** — he re-issues "make it perfect" with no exit test; the assistant re-asks one question with no default | N01, N07, N27 | Both platforms | High |
| **P3** | **The predictable second step: render it as a deliverable** — dashboard for data, court-ready PDF for law | N03, N24 | 6 of 8 conversations | High |
| **P4** | **Heavy front-loaded scaffolding, versioned, domain-independent** — schemas, formulas, guardrails, node/edge architecture maps, v1 → v2 → v3 | N04, N05, N12, N22, N23 | Both domains — *promoted from Medium* | **High** |
| **P7** | **Every map gets a score** — a structured map is immediately followed by a triage layer producing one priority verdict | N32, N12, N31 | Both domains | High |
| **P8** | **The instruction set is rebuilt every session** — re-priming in 3 of 3 ChatGPT threads; the RLN schema hand-maintained since Oct 2025 | N20, N30 | ChatGPT only *(Claude threads carry standing instructions instead)* | High |
| **P2** | **Shorthand the AI must decode over rounds** — "audiovisuals," "cognitive wish" carry stable intent, interpretation lags | N02, N08 | C1 only — *not testable in C6–C8 (his turns absent)* | Medium |
| **P5** | **Answer fragility on incomplete data** — headline metric swings ~1 point on same-day gaps | N09, N10 | Health only | Medium |

## The central finding of Round 2

**The stall is not his impatience — it is the missing stop rule, on either side of the exchange.**

| Direction | What happens | Cost observed |
|-----------|--------------|---------------|
| His loop has no exit test | "Redo to the perfect output" fires 3× in one thread; each firing rebuilds from scratch (N01) | 2 wasted rebuild rounds in C1 |
| The assistant's loop has no default | The same question asked 3× in a row; 5 confirmation turns before any output (N26, N27) | 4 documents never delivered in C8; 5 round-trips in C7 |

Both are the same defect. One is fixed by a Done-when test; the other by propose-then-confirm. Neither requires more effort — only a rule.

## Ask → Intent → Outcome deltas

| Conversation | The literal ask | The inferred intent | The delta the loop paid for |
|--------------|-----------------|---------------------|------------------------------|
| C1 | "Redo to the perfect output, red-team it, add audiovisuals" (×3) | A living, visual dashboard on his real data | Intent stable at turn 1; 3 rebuild rounds because neither "perfect" nor "audiovisual" was operationalised. **N01, N02** |
| C2 / C4 | "Produce the 9-section report" | One trustworthy number and the top lever | Two runs, two Loop Scores; the durable signal was identical, the score was not. **N09, N10** |
| C3 | "Recommend the correct wraps" | Decide for me from the evidence | He removed two constraints and handed the third back; clarifying questions were friction. Deliverable absent. **N06** |
| C5 | "Build a citation-rich synthesis" → "visualize this" | Give me the map, then let me see it | Cleanly scoped; only the foreseeable render-second step. **N03** |
| C6 | *(not captured)* → "take full initiative, stop pausing for confirmations" | Produce the filings; assume and proceed | The most productive thread in the corpus: 4 PDFs + 2 full maps. Only unfinished item is the last offered PDF. **N25, N28** |
| C7 | *(not captured)* — a legal packet suite | Five signed-and-ready documents | Five consecutive formatting questions first; the promised markdown mirror set never arrived. **N26, N28** |
| C8 | *(not captured)* — four companion documents | A complete causal-harm dossier | Deadlocked on one missing date, asked three times. Zero of four delivered. **N27** |

## Correction pattern

He corrects **form and depth, never facts** (N07) — unchanged in Round 2, and now with a boundary attached: he wants exact figures where they trace to a source, and bands where the AI is judging (N31). Consequences:

- **Strength:** fast to a usable artefact; he trusts substance and iterates on rendering.
- **Latent risk:** his correction budget still never lands on verification. The unverified content notes (N15–N18 health, N33 legal) would survive his review unchallenged.

## Stall points, ordered by observed cost

| # | Stall | Cost in this corpus | Fix |
|---|-------|--------------------|-----|
| 1 | **Ask-then-wait** (P6) | 4 documents undelivered (C8), 5 round-trips (C7), 1 deliverable lost (C3) | **Propose-then-confirm.** Produce the draft, state the assumption inline, invite correction. Never more than one question, never a question instead of a draft. |
| 2 | **No externalised "done"** (P1) | 2 rebuild rounds (C1) | A Done-when test on every task. Already in LOOP OS. |
| 3 | **Un-pre-empted render step** (P3) | 1 round in each of 6 conversations | Ship the artefact in the first pass — dashboard, PDF or both. |
| 4 | **Session re-priming tax** (P8) | 3 of 3 ChatGPT threads | Persist the instruction set in a file. This repository is that fix. |
| 5 | **Completeness-blind metrics** (P5) | 6.7 vs 5.7 on the same data | Print "inputs present: X/Y" beside any composite score. |
| 6 | **Un-glossed shorthand** (P2) | 2–3 rounds (C1) | A short glossary in standing instructions. |

## The meta-observation

Across all eight conversations the through-line is unchanged but now dated: **he keeps hand-running a loop while trying to build the machine that runs it for him.** Round 2 shows this is not new — the RLN Living Notebook, with ID codes, YAML front-matter, backlinks and triage horizons, was already operating in October 2025 (N30). The CNN→RNN→RL design of early 2026 is the automation attempt; this field test is the third iteration.

Every stall point above is a place where that automation has not happened yet. The most expensive of them — ask-then-wait — is the one the *responder* can fix unilaterally, without him changing anything.

## Confidence on the map as a whole

**Medium-High.** *Why:* five of seven patterns now replicate across two platforms, two domains and two time points, which is the right test and it passed (N29). What holds confidence down: 8 of ~50 conversations, a 5-month window rather than five years, and — for C6–C8 — his own messages are missing, so those claims are one inference-step removed (N21). Generalisation to "how he thinks overall" is now **Medium**, up from Low.
