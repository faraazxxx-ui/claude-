# Telemetry

One line per session. Minimum one per day, even mid-task. Append only.

## Format

```
YYYY-MM-DD · task-slug · outcome:PASS/FAIL · rounds:n/2 · breakers:none/named · detours:n(what,why) · handoffs:n · note:one line
```

The value is the pattern across lines, not any single entry — repeated detours to the same cause, or a slug that keeps reappearing, is the signal. So keep entries terse and never retroactively tidy one.

## Log

```
2026-08-29 · verify-whisper-dictation-doc · outcome:PASS · rounds:1/2 · breakers:none · detours:1(spine-absent,Gate-0-found-no-hub/goal/verify-so-ran-ungated) · handoffs:0 · note:8 of 13 doc claims wrong incl. install method and hotkey; token-saving premise itself was false
2026-08-29 · build-voice-capture-skill-and-spine · outcome:PASS · rounds:1/2 · breakers:none · detours:0 · handoffs:0 · note:skill written from re-verified README not recall; goal.md left UNSET rather than guessed
2026-08-30 · independent-verify-voice-capture-skill · outcome:PASS · rounds:1/2 · breakers:none · detours:0 · handoffs:1(Opus5→Sonnet5) · note:fresh-model re-fetch of source confirms zero drift from SKILL.md; Gate 4 now satisfied for this artifact
```
