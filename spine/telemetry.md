# Telemetry

One line per session, per the orchestrator contract:
`YYYY-MM-DD · task-slug · outcome · rounds · breakers · detours · handoffs · note`

2026-09-04 · session-export-mega-loop · outcome:PASS · rounds:1/2 · breakers:none · detours:2(container recycled — local branch sat behind origin, restored from remote; reasoning plaintext absent from transcript — export re-scoped to what is provable) · handoffs:0 · note:Full session exported to JSON/SQL/MD/PDF/artifact; round-trip verified; reasoning content unrecoverable and stated as such.

---

## Spine status — read before assuming this is wired up

`hub.md`, `goal.md`, `verify.md`, `progress.md`, `failure.md` and `learnings.md` **do not exist in this repository.** Gate 0 of the orchestrator says to read hub, goal and verify before dispatching anything; there was nothing to read, so that gate did not pass — it was skipped, and this note exists so nobody later assumes otherwise.

This file was created because gate 6 requires a telemetry line every session. The other five are **his to author** — writing them for him would be inventing a goal he never set, which is the failure mode the whole contract exists to prevent.

| File | Status | Who writes it |
|---|---|---|
| `telemetry.md` | Live | Appended every session |
| `hub.md` | Missing | Him |
| `goal.md` | Missing | Him — without it, no task can be checked for fit |
| `verify.md` | Missing | Him — the standing rubric a separate verifier grades against |
| `progress.md` | Missing | Him, or accumulated per task |
| `failure.md` | Missing | Him, or accumulated per task |
| `learnings.md` | Missing | Him, or accumulated per task |

Until `goal.md` and `verify.md` exist, two of the five gates are structurally unenforceable: nothing can be checked for fit against a live goal, and a separate verifier has no rubric to grade lines against. Gates 1 (mode select), 2 (privacy zone) and 5 (stop budget) work without them.
