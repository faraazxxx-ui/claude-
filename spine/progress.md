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

---

## 2026-08-30 — Gate 4 satisfied: independent re-verification, zero drift

A fresh session (Sonnet 5, not the Opus 5 pass that built the artifact) re-fetched `enesbasbug/voice-to-claude`'s README directly — not the prior session's ledger — and checked it line-by-line against `skills/voice-capture-setup/SKILL.md`. Every fact matched: hotkey, install steps, prerequisites, daemon requirement, model sizes and speeds, permissions, platform scope. No corrections needed.

This is the separate-verifier pass `progress.md` flagged as missing on 2026-08-29. Gate 4 is now satisfied for this artifact's factual accuracy.

**Still open, unchanged.** `goal.md` remains UNSET. `sony_sync.sh` and its plist remain unread. PR #30 unchanged — clean, draft, no comments.

---

## 2026-11-12 — Canonical cross-platform memory pack built for the angelic-orchestrator push

**State now.** `angelic-orchestrator/` exists: `CANONICAL_MEMORY.md` (v1.0.0, the single source of truth), `LEARNING_LOOP.md` (perpetual write-back mechanism), `platforms/_BOOTSTRAP.md` plus one install file per platform — ChatGPT, Gemini, Grok, Le Chat, Mistral API, M365 Copilot, Hermes Agent, Anti Gravity. Platform mechanisms verified 2026-11-12 against each vendor's own docs where possible (ChatGPT, Gemini, Anti Gravity, Hermes, M365 = High); Grok, Le Chat, Mistral consumer UI tagged Medium, verify on first use.

**What moved.**

| | |
|---|---|
| Built | `angelic-orchestrator/` — README, CANONICAL_MEMORY, LEARNING_LOOP, _BOOTSTRAP, 8 platform files |
| Verified | No platform syncs memory with another (ChatGPT/Gemini docs state it); per-platform memory mechanisms + limits (Grok 4,000-char cap; Gemini Gems read-only 2026-11-17 → Skills; Anti Gravity AGENTS.md/.agents/rules; Hermes MEMORY.md + skills loop; Copilot Memory + Custom Instructions, not for Agents) |
| Seeded from | local repos only (`claude-`, `perplexity-chat-export`) + public vendor docs |
| Recorded | 1 telemetry line, 2 learnings |

**Open — blocking.**

`goal.md` is still UNSET. Gate 0 is standing but not loaded. Dr. Rahman fills it.

**Open — not blocking.**

- The grok.com project (ef2c7a89…) and claude.ai project (01a00d0e…) URLs, Google Drive, and "super memory" were **not reachable from this build environment**. The pack was seeded from the local repos; anything living only in those external projects must be pasted in manually (the platforms files say how).
- Gate 4 NOT satisfied for this pack: the same pass built it and wrote this summary; no independent verifier graded it against `verify.md` line-by-line. Next session should do that pass before the pack is relied on.
- Grok / Le Chat / Mistral consumer files are Medium confidence — first real paste is the test.
- `spine/hub.md` standing-skills table does not list `angelic-orchestrator/` yet — hub.md is Dr. Rahman only, so left untouched.

**Next.** Dr. Rahman pastes `_BOOTSTRAP.md` + `CANONICAL_MEMORY.md` into ChatGPT first (Custom Instructions + angelic-orchestrator Project), then works down the README install map, then fills `goal.md`.

---

## 2026-11-12/16 — Full session export built: MD, JSON, SQL, PDF, Artifact

**State now.** `exports/angelic-orchestrator-session-2026-08-29/` holds a complete turn-by-turn export of the 2026-08-29→11-12 session (doc verification, skill build, independent verifier pass) in five formats, generated from one source (`data.py` + a live read of the repo's own artifact files) so the formats can't drift apart. Published Artifact: https://claude.ai/artifact/4vbLr9ktznCz4knMNARqjk.

**What moved.**

| | |
|---|---|
| Built | `exports/angelic-orchestrator-session-2026-08-29/` — transcript.{md,json,sql,pdf}, artifact_source.html, data.py, build.py, README.md |
| Validated | JSON parses; SQL loads cleanly into a real sqlite3 database (not just well-formed text); PDF is a genuine multi-page %PDF-1.4 file; artifact's embedded JS passes `node -c` |
| Rendered locally | pandoc (MD→HTML) → pre-installed headless Chromium (HTML→PDF) — no external conversion service touched, consistent with this session's own local-only stance |
| Recorded | 1 telemetry line |

**Open — flagged in the export itself, not resolved by it.** Dr. Rahman's work email appears in commit trailers and session metadata reproduced in the export. Not sensitive on its own, but the export's stated destination is "to be analyzed by others" — redact before this folder leaves Dr. Rahman's own control. The export documents this; it doesn't decide it.

**Still open, unchanged.** `goal.md` still UNSET. `sony_sync.sh`/plist still unread. `angelic-orchestrator/` pack (fb3bb92) still has no independent-verifier pass.

**Next.** Dr. Rahman decides whether/how this export folder gets shared, and handles the email-redaction call first if so.
