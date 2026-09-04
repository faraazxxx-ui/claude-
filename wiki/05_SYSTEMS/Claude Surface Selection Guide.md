---
title: Claude Surface Selection Guide
created: 2026-08-07
updated: 2026-08-07
domain: systems
tags: [claude, routing, triage, surfaces, workflow]
status: developing
sources: [conversation-2026-08-07, AI_Platform_Master_Reference_FULL.md]
related: ["[[Claude Layers Model]]", "[[Second Brain Operating Loop]]", "[[MOC — Claude and the Second Brain]]"]
---

# Claude Surface Selection Guide

"A few clicks behind optimal" is almost always a routing error, not a prompting error — the right question sent through the wrong door. This page is the triage algorithm: classify the task by two axes (how long it runs, how much of *your* context it needs) and the surface picks itself. Thirty seconds of triage before starting saves the restart that usually follows.

## The triage table

| The task in front of you | Surface | Why |
|---|---|---|
| Quick question, thinking partner, one-off draft | **claude.ai chat** | Zero setup; context dies with the session — fine, because nothing durable is at stake |
| Anything inside a standing domain — a case, the litigation, the foundation | **The domain's Project** | Project knowledge (wiki pages) pre-loads layer 4; no re-explaining |
| Task matching an encoded procedure — clinical narrative, legal strategy, prompt polishing | **The matching skill**, inside chat or Project | The procedure fires as a unit, like an order set; naming it beats hoping it triggers |
| Needs your live data — inbox, calendar, Drive, literature | **Connectors, invoked explicitly** | "Check my calendar" outperforms hoping the model volunteers; a lookup beats a recall every time |
| Long, multi-step, file-producing, or repo-touching | **Claude Code** | Holds a working directory, runs tools, survives the length; where this very page set was built |
| Recurring on a schedule — reconciliation pass, morning brief, monitoring | **Scheduled routine / agent** | The system holds the cadence so working memory doesn't have to |
| Big volume batch job — archive mining, corpus processing | **Claude Code with subagents** | Parallel workers over batches; a chat window cannot hold it |

## The two-question shortcut

When the table feels like too much, two questions route almost everything:

1. **Will anything from this need to exist tomorrow?** If yes → a Project or Claude Code, and the output gets captured to the wiki ([[Second Brain Operating Loop]]). If no → plain chat, guilt-free.
2. **Does it need my context or my tools?** If your context → Project (wiki-fed). If tools/files/time → Claude Code or a routine. If both → Claude Code with the wiki connected.

## Standing rules

- **Name the skill when you know it.** Skill triggers are good, not perfect; "use apex-legal-strategy" removes the ambiguity — several skills in the current roster have overlapping triggers.
- **One domain per Project, wiki as its knowledge.** The Project is the exam room; the wiki pages are the chart on the door.
- **Never let chat do an agent's job.** A task that will outlive your attention span belongs to a surface that outlives it too. Handing a long task to a chat window is self-defeating on ADHD terms — the surface should compensate for drift, not depend on its absence.
- **Model choice is dose, not identity** (layer 1 of [[Claude Layers Model]]): deepest model for strategy and synthesis, mid-tier for routine drafting, fast tier for mechanical batching.

## Open questions

- Which recurring routines to stand up first — weekly wiki reconciliation is the obvious lead candidate.
- Whether the skills roster needs a deduplication pass before routing rules can be reliable (flagged also in [[Claude Layers Model]]).

## Provenance

Surface capabilities: Anthropic product line as of early 2026; verify before load-bearing use. Routing heuristics and two-question shortcut: original synthesis, conversation of 2026-08-07, consistent with the routing card in `AI_Platform_Master_Reference_FULL.md`.
