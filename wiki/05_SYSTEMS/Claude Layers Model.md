---
title: Claude Layers Model
created: 2026-08-07
updated: 2026-08-07
domain: systems
tags: [claude, mental-model, layers, context-window, skills, mcp]
status: developing
sources: [conversation-2026-08-07, AI_Platform_Master_Reference_FULL.md]
related: ["[[Why Wiki Pages Are the Second Brain]]", "[[Second Brain Operating Loop]]", "[[Claude Surface Selection Guide]]", "[[MOC — Claude and the Second Brain]]"]
---

# Claude Layers Model

Claude is a seven-layer stack. The bottom layer — the trained model itself — is frozen and identical for every user on earth. Every layer above it is configurable, and the entire difference between "using AI indefinitely" and "using AI as a second brain" lives in layers 2 through 7. The correct mental model: you will never train the model on your data; you will engineer what the model *sees* at the moment it thinks. That reframe changes everything about where to invest effort.

## The seven layers

Bottom to top. Each layer wraps the one below it, the way an attending's judgment wraps their med-school knowledge.

| # | Layer | What it actually is | Clinical analogy | Yours to change? |
|---|---|---|---|---|
| 1 | **Weights** — the trained model | Billions of frozen parameters, set during training at Anthropic, identical for everyone | Everything consolidated in a physician's long-term memory through med school and residency. You cannot edit it by talking to them. | No. You only choose which model (Opus for depth, Sonnet for balance, Haiku for speed). |
| 2 | **Context window** — working memory | Everything visible in the current session: your words, pasted documents, retrieved files, tool results. Large but finite, and wiped when the session ends. | Working memory plus the whiteboard in the room. The model has no hippocampus — every new chat starts with anterograde amnesia. | Completely. This is the layer where your data actually meets the model. |
| 3 | **System prompt, preferences, styles** | Standing instructions silently prepended before your message | Standing orders and the unit protocol taped to the wall — shapes every encounter without being restated | Yes — settings, personal preferences, per-Project instructions. |
| 4 | **Memory and Projects** | Persistent notes and uploaded knowledge that claude.ai auto-loads into context across chats | The chart that follows the patient between visits, instead of re-taking the history every time | Yes — one Project per domain, curated project knowledge. |
| 5 | **Skills** | Packaged procedures loaded on demand when a task matches | Order sets and care pathways: the sepsis bundle fires as a unit instead of being reinvented per patient | Yes — you already run a roster of them (axiom, apex-legal-strategy, physician-clinical-narratives, skill-creator, and more). |
| 6 | **Connectors (MCP)** | Live interfaces to external systems — Drive, Gmail, Calendar, GitHub, PubMed-class sources | EMR and lab interfaces: real-time values pulled from the source instead of recalled from memory | Yes — each connector converts a guess into a lookup. |
| 7 | **Agents and scheduled work** | Claude operating over time with tools — Claude Code sessions, background agents, recurring routines | Delegating to a resident with standing orders who works the list and reports back | Yes — long tasks, repo work, recurring jobs. |

Layers 2–4 determine what Claude **knows** in a session. Layers 5–7 determine what Claude **can do**. Layer 1 is fixed talent; everything else is systems design — and systems design is the part you are already good at.

## The one correction to the training-based mental model

The hypothesis "feed it everything, train it on itself until it mirrors me" is directionally right and mechanically wrong, and the mechanical part matters because it redirects the build.

- **Training** (weights, loss function, gradient descent) happened once, in the past, at Anthropic. The loss function measured the gap between the model's prediction and the actual next word across an enormous corpus, and nudged billions of weights to shrink that gap, millions of times. That process is closed. Nothing typed into a chat updates a weight.
- **Inference** (what every conversation is) runs your context through those frozen weights. The model's *attention* mechanism decides which parts of the context matter for each word it generates — which is why context quality dominates outcome quality.
- Therefore the personal system is built on **retrieval, not retraining**: keep your knowledge outside the model in a form that can be found and loaded into the context window at the moment of need. The industry name is retrieval-augmented generation; the working name here is the second brain.

The p-value / confidence-interval intuition survives the correction — it just relocates. In training, loss minimization is exactly iterative error-reduction against ground truth, successive approximation toward the tightest interval. In *your* system, the same loop exists one level up: the error signal is the gap between what your wiki supplied to a session and what the session actually needed, and each reconciliation pass is the gradient step. That loop is specified in [[Second Brain Operating Loop]].

## Where each layer earns its keep for you

| Your recurring situation | Layer that solves it |
|---|---|
| "Claude doesn't know my history / I re-explain everything" | 4 (Projects, Memory) fed by the wiki — see [[Why Wiki Pages Are the Second Brain]] |
| "The answer is generic, not calibrated to me" | 3 (preferences) + 5 (skills like axiom that encode how you think) |
| "It's guessing about my calendar / inbox / files" | 6 (connectors) — never let it recall what it can look up |
| "The task is too big for one sitting" (ADHD drift risk) | 7 (agents, scheduled routines) — the system holds the thread so you don't have to |
| "Output quality varies wildly" | 2 — context curation; garbage in the window, garbage out |

## Open questions

- Which domains get dedicated Projects first — clinical, legal, foundation — and what is the minimum project-knowledge set per domain?
- Where is the crossover point at which wiki-page retrieval should be supplemented by the embedding pipeline in `Personal_Data_Embedding_Living_AI_Guide.md`?
- Should the skills roster be consolidated? Several skills overlap (two grok-apex-legal versions, multiple prompt optimizers) — overlapping triggers create routing ambiguity.

## Provenance

Layer taxonomy and training-vs-inference distinction: standard transformer architecture, stated from model knowledge, current as of early 2026. Claude product surfaces (Projects, Memory, Skills, MCP connectors, Claude Code): Anthropic product line as of early 2026 — recheck against current docs before load-bearing decisions, as surfaces evolve quickly. Clinical analogies and the personal-loss-function mapping: original synthesis for this wiki, conversation of 2026-08-07.
