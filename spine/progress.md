# Progress

Current state as of the last pass. The slow loop never reports itself done — only current.

Append a dated block per pass. Do not rewrite earlier blocks; a superseded state is evidence of direction, and direction is what this file is for.

---

## 2026-08-29 — Capture layer verified and written down; spine stood up

**State now.** The voice stack is documented accurately for the first time. The install instructions Dr. Rahman was previously given did not work; the corrected ones live in `skills/voice-capture-setup/` along with a dated ledger of what has actually been checked against a source.

The spine exists. Gate 0 has files to read.

**What moved.**

| | |
|---|---|
| Verified against primary sources | voice-to-claude install, hotkey, prerequisites, daemon, models, permissions, latency; Homebrew formula; both model file sizes by HTTP HEAD |
| Built | `skills/voice-capture-setup/` — SKILL.md, `verified_facts.md`, `sony_batch_pipeline.md` |
| Built | `spine/` — all seven files |
| Corrected | 8 wrong claims in the prior briefing doc; 3 broken shell commands in the Sony install |
| Recorded | Two failures, three learnings, two telemetry lines |

**Open — blocking.**

`goal.md` is UNSET. Until Dr. Rahman fills in the current push, done-condition, and out-of-scope, Gate 0 can confirm the file exists but cannot test whether a task belongs. The gate is standing but not yet loaded.

**Open — not blocking.**

- Nothing in `skills/voice-capture-setup/` has been executed. It was written from a README, on Linux, for a macOS machine. First real install is the test.
- `sony_sync.sh` and its plist remain uninspected. The install commands around them are fixed; the scripts themselves are unaudited.
- `verbal-thinker-stack-audit/voice-first-verbal-thinker-skill` was deliberately left untouched. Its routing card still points at Manus, Genspark, AudioPen and Wispr Flow — none re-verified, some possibly stale.
- Gate 4 was not satisfied for this pass. See below.

**Gate 4 note.** The separate-verifier gate could not be honoured: the same pass that built the skill and the spine also produced this summary, and no independent grader ran. That is a real gap, not a formality — the specific risk is that errors of the same *kind* the builder is prone to will not be visible to the builder. The next session should grade `skills/voice-capture-setup/SKILL.md` against the ten standing lines in `verify.md` with fresh eyes before the instructions are relied on.

**Next.** Dr. Rahman fills `goal.md`, then runs the Part A install on the Mac.
