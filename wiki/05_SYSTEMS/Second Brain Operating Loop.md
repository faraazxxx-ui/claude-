---
title: Second Brain Operating Loop
created: 2026-08-07
updated: 2026-08-07
domain: systems
tags: [second-brain, operating-loop, loss-function, capture, reconciliation]
status: developing
sources: [conversation-2026-08-07, Personal_Data_Embedding_Living_AI_Guide.md]
related: ["[[Claude Layers Model]]", "[[Why Wiki Pages Are the Second Brain]]", "[[Chat Archive Mining]]", "[[MOC — Claude and the Second Brain]]"]
---

# Second Brain Operating Loop

The second brain is not a thing you build once; it is a loop you run. Six stages — capture, triage, reconcile, index, retrieve, act — where each cycle measurably narrows the gap between what the system supplies and what you actually need. This page defines the loop, maps it onto the loss-function intuition (which is correct, just relocated), and gives the build order: retrospective arm first to seed the wiki, prospective arm forever after.

## The loop

| Stage | What happens | Where it lives |
|---|---|---|
| 1. Capture | Everything durable gets written down at the moment it exists: dictations, decisions, conversation outputs, documents | `99_INBOX/`, or straight to a page when the target is obvious |
| 2. Triage | Captures get routed to their domain — clinical and legal always segregated | Folder taxonomy in the wiki protocol |
| 3. Reconcile | New material merges into existing pages; contradictions resolved explicitly; statuses promoted | The wiki itself — see [[Why Wiki Pages Are the Second Brain]] |
| 4. Index | New pages linked from their MOC; links made bidirectional; later, embeddings refreshed | `00_INDEX/`, eventually the vector pipeline |
| 5. Retrieve | Each new Claude session pulls the relevant pages into the context window — by Project knowledge, Drive connector, or paste | Layers 2, 4, 6 of [[Claude Layers Model]] |
| 6. Act | Claude works with your actual state loaded, via skills and connectors; the session's durable output becomes a new capture | Layers 5–7, then back to stage 1 |

The loop is closed: acting generates captures, captures become pages, pages improve the next retrieval. Skip stage 3 and the system silently degrades into the data pile it was meant to replace.

## The loss function, relocated

The original intuition — trim the p-value and confidence interval until the model is the closest real-time mirror of the situation — is the right shape. It just doesn't run inside the model (those weights froze at Anthropic); it runs on the wiki.

| Training a neural net | Running your second brain |
|---|---|
| Prediction vs. actual next token | What the wiki supplied to a session vs. what the session actually needed |
| Loss function measures the gap | You notice the gap: the re-explaining you had to do, the context that was missing, the stale position that got retrieved |
| Gradient step nudges the weights | Reconciliation pass edits the pages: fills the hole, corrects the stale claim, adds the missing link |
| Millions of iterations converge | Hundreds of cycles narrow the interval around "what Dr. Rahman means and needs" |

Two practical consequences. First, **gaps are the signal, not the failure**: every time a session forces re-explanation, that is a labeled training example — capture it before it evaporates. Second, **convergence is real but asymptotic**: the mirror sharpens for months and then plateaus; the plateau is when the embedding pipeline becomes worth its complexity.

## Retrospective arm — seeding from the existing pile

Run once, in this order. The goal is coverage of what already exists, not perfection.

1. **Chat archives first.** Highest signal per gigabyte — they encode intent, not just facts. Full method in [[Chat Archive Mining]]; output is seed pages plus the linkage map.
2. **Active documents second.** For each live domain (clinical, legal, foundation, systems), the ten or twenty documents actually in play become or feed pages. Do not attempt the whole drive.
3. **The long tail last, and lazily.** Everything else gets touched only when a live task needs it — capture-on-demand beats bulk migration, and bulk migration is the classic ADHD project-graveyard shape.
4. **The heavy pipeline** (`Personal_Data_Embedding_Living_AI_Guide.md` — extraction, BigQuery, embeddings) is phase 2, applied to the *consolidated* wiki plus selected raw corpora, not a substitute for steps 1–3.

## Prospective arm — the standing habit

- Every substantive Claude session ends with a wiki write of anything durable: decisions with reasoning, resolved problems, reusable frameworks, facts a future session would otherwise re-derive. Capture during the session, not after — sessions end without warning.
- The axiom skill already carries this obligation automatically; the habit to build personally is *dictating captures the moment they occur* rather than trusting recall.
- A recurring reconciliation session (weekly or biweekly, scheduled — layer 7 of [[Claude Layers Model]] can run it as a routine) drains `99_INBOX/`, promotes statuses, and repairs orphan pages. This is the gradient step; protect it like a clinic slot.

## Failure modes and their pre-installed counters

| Failure mode | Counter already built in |
|---|---|
| Capture stops after two weeks (novelty decay) | Captures are one dictation long; the loop survives on 5-minute units; scheduled routine does the heavy lifting |
| Wiki becomes a second landfill | Search-before-write and merge-don't-append rules; MOC requirement makes orphans visible |
| Bulk-migration project stalls and poisons motivation | Retrospective arm is explicitly capped: archives + active documents only; long tail is lazy |
| Tool-building displaces tool-using (meta-work trap) | The loop runs on plain markdown from day one; embeddings and pipelines are gated behind the plateau, not prerequisites |

## Open questions

- Cadence: is weekly reconciliation sustainable, or should it ride an existing anchor habit?
- Which gap types recur most in the first month — that distribution decides where to invest next (more capture vs. better retrieval vs. more connectors).
- Trigger criteria for phase 2 (embeddings): page count, retrieval-miss rate, or wiki size?

## Provenance

Loop structure: adaptation of the standing 2_WIKI protocol's capture/reconciliation rules into an explicit cycle. Loss-function mapping: original synthesis from the conversation of 2026-08-07, validating and relocating the user's own analogy. Phase-2 pipeline reference: `Personal_Data_Embedding_Living_AI_Guide.md` in this repo.
