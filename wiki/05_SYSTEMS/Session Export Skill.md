---
title: Session Export Skill
created: 2026-09-04
updated: 2026-09-04
domain: systems
tags: [session-export, archival, skill-creator, second-brain-tooling]
status: stable
sources: [conversation-2026-09-04]
related: ["[[MOC — Claude and the Second Brain]]", "[[Second Brain Operating Loop]]", "[[Chat Archive Mining]]"]
---

# Session Export Skill

`skills/session-exporter` turns a conversation into a portable, five-format archive — JSON (source of truth), Markdown narrative, an interactive HTML artifact, a paginated PDF, and a SQL/SQLite dump — built for someone other than the participants to audit in detail and rebuild faithfully. It exists because a raw transcript dump is useless to a third party: the signal (what was decided, and why) is buried in tool-call plumbing and retries. The skill reconstructs the record the way a discharge summary reconstructs a chart — same events, organized for a stranger to pick up.

## First run

`session-exports/2026-09-04-claude-layers-second-brain/` — the export of the session that produced this wiki's `05_SYSTEMS` pages and the visual guide artifact. Its README explains the five files and the fixed schema (sessions / turns / assistant_actions / analysis_rows / artifacts / tool_failures) shared by JSON and SQL alike, so two exports from two different sessions stay diffable and joinable.

## The honesty rule that makes it trustworthy

The skill has no access to its own past hidden reasoning tokens — only to what a turn actually exposed (a Supporting Analysis table) or actually did (files written, tools called). Where a turn's reasoning has to be reconstructed rather than quoted, the export says so explicitly rather than presenting inference as a verbatim log. Failed tool calls are recorded, not cleaned up — a wrong tool name or a denied approval is exactly the kind of gap [[Chat Archive Mining]] exists to catch.

## When to use it again

Any time a session's output should survive being handed to someone who wasn't in the room — a collaborator, an auditor, or a future session rebuilding from scratch. Not for routine wiki capture; that's what the ordinary reconciliation loop in [[Second Brain Operating Loop]] already does.

## Open questions

- Whether session exports themselves should ever get mined the way `[[Chat Archive Mining]]` mines external chat archives — the `tool_failures` table across many exports would be a direct, structured gap ledger.
- Retention: exports live under `session-exports/` at the repo root (not in the wiki taxonomy — they're raw archival material, not consolidated knowledge). No pruning policy set yet.

## Provenance

Built and first run 2026-09-04, in response to a request to archive the layers/second-brain session itself — a direct instance of the second-brain method applied reflexively to its own construction.
