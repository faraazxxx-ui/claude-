# Learning Loop — the perpetual mechanism

**Privacy zone: Private work.** Version 1.0.0 · 2026-11-12

The pack stays alive because facts flow one way — out of conversations, into the repo — and the canonical file is re-emitted when enough has accumulated. Nothing is ever rewritten in the logs; the value is the pattern across entries.

## The loop

```
SESSION START                DURING                       SESSION END                 WEEKLY
─────────────                ──────                       ───────────                 ──────
Gate 0: read spine/hub,    Work under standing          Emit WRITE-BACK block:      Consolidate logs →
goal, verify + this        rules (10 lines).            new facts (use / weakness /  bump CANONICAL_MEMORY
canonical pack.                                          next action) + privacy tag   version → re-paste where
                                                         + one-line summary.          stamp changed → audit
                                                                      │                  platform memories, delete drift
                                                                      ▼
                                                         append to spine/learnings.md,
                                                         spine/progress.md,
                                                         spine/telemetry.md (one line min per day)
```

## Session-start protocol (Gate 0, extended)

1. Read `spine/hub.md`, `spine/goal.md`, `spine/verify.md`. If any is missing or `goal.md` says UNSET, say so out loud before dispatching work — a missing gate must announce itself, never silently proceed.
2. Read `CANONICAL_MEMORY.md` (or confirm the platform's cached copy matches the version stamp).
3. If a task does not fit `goal.md`, stop and say so. That is the gate working.

## Session-end WRITE-BACK format (paste into chat, Dr. Rahman files it)

```markdown
## WRITE-BACK · <date> · <platform> · privacy: <zone>
- Fact: ... | Use: ... | Weakness: ... | Next action: ...
- Fact: ... | Use: ... | Weakness: ... | Next action: ...
Summary: one line.
```

## Log map (append-only, never rewrite history)

| File | What goes in | Cadence |
|---|---|---|
| `spine/progress.md` | Current state as of the last pass | Every session |
| `spine/telemetry.md` | One line per session, minimum one per day | Every session |
| `spine/failure.md` | What broke, what it cost, what would have caught it | On failure |
| `spine/learnings.md` | What is now known that was not before | On learning |

`spine/hub.md`, `spine/goal.md`, `spine/verify.md` are Dr. Rahman only — read-only during a task.

## Cross-platform sync rules

1. **The repo is the truth; platform memory is a cache.** On any conflict, the repo wins.
2. **Version stamp check:** every platform session starts by comparing its cached pack version against this repo's. Mismatch → ask for the current file, do not improvise.
3. **Monthly audit:** open each platform's memory UI, delete entries that contradict the canonical pack or that drifted. Platform memories are auto-curated and will drift; that is expected, not a bug.
4. **Hard limits:** Grok custom instructions cap ~4,000 chars; ChatGPT memory truncates long entries; Gemini Gems go read-only 2026-11-17 (use Skills). So the full pack lives in files/attachments, never only in a text box — the bootstrap text box carries rules only.
5. **Privacy is non-negotiable in the loop:** Confidential+ facts never enter any platform memory. If a WRITE-BACK block contains one, tag it and file it locally only.

## Failure handling

- 3 consecutive fails on the same verify line → halt, surface to Dr. Rahman; the rubric line or approach is wrong, not the effort.
- Any platform that answers from its own stale memory against the canonical pack → correct it, note the drift in `spine/failure.md`.
- If the canonical pack and a platform memory genuinely disagree and the pack is older, bump the pack first — never patch the platform cache as the fix.
