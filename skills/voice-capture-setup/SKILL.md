---
name: voice-capture-setup
description: Install, repair, and tune Dr. Rahman's local voice-dictation stack — the voice-to-claude push-to-talk plugin for Claude Code, and the Sony recorder batch-transcription pipeline, both running whisper.cpp on-device. Use this skill whenever he mentions dictation, voice input, push-to-talk, whisper, whisper.cpp, Wispr Flow, transcription, the Sony recorder, Voice-Inbox, a hotkey that stopped working, text not appearing at the cursor, or asks how to talk to Claude Code / Cursor / a terminal instead of typing. Also use when he asks whether voice input saves tokens, and use it any time a session is about to hand him install commands for a dictation tool — this skill carries the verified commands and exists precisely because unverified ones have already cost him an afternoon. He does not write code: every instruction he receives must be copy-paste exact and must not assume he can debug it.
---

# Voice Capture Setup

The capture layer beneath `voice-first-verbal-thinker`. That skill structures speech once it is text; this one gets speech *into* text correctly.

## Standing rule for whoever is reading this

Dr. Rahman cannot code. He cannot tell a working command from a broken one until it fails, and when it fails he cannot repair it. That asymmetry is the whole reason this file exists.

So: **do not give him an install command that is not in this file.** If a task needs a command that is not here, fetch the project's own README or docs page and read the current instructions before answering. Recall is not verification. The last time a session answered this from memory it produced a wrong install method, a wrong hotkey, a wrong prerequisite, and a caveat imported from a different tool — all of which read as confident and none of which worked.

When you do verify something new, add it to `references/verified_facts.md` with the date and the source, so the next session inherits the check instead of repeating it.

## Answer this correctly when he asks: does voice input save tokens?

No. It cannot, and the framing hides a real cost.

Claude Code's prompt has always been text — there was never an audio token charge to avoid. The built-in `/voice` command bills *transcription*, which is a separate service, not model context. So "local whisper saves tokens" compares against a charge that never existed.

What local whisper.cpp actually buys is **privacy** (audio never leaves the Mac) and **no per-hour transcription fee**. Both are real. Neither is tokens.

The part that matters for him: dictated prompts run materially longer than typed ones, so voice input tends to **raise** token use per turn. If token economy is the actual goal, the lever is prompt discipline and batching long thinking through Part B below — not the input method. Say this plainly rather than letting him optimize the wrong variable.

## Which path for which job

| Situation | Path |
|---|---|
| Short-to-medium prompt typed into Claude Code | **Part A** — push-to-talk |
| A five-minute design ramble, a drive, a walk | **Part B** — Sony recorder, batch transcribe, paste the cleaned text |
| Needs to stay on-device (patient material, litigation, journal) | Either — both are local. Never `/voice`, never a cloud transcriber. |
| He already has Wispr Flow running and it works | Leave it. Part A and Wispr Flow do the same job; running both is redundant, not additive. |

`/voice` (Claude Code's built-in) streams audio to Anthropic's servers and requires Claude.ai authentication. It works, it is free with his plan, and it is genuinely zero-setup — but it breaks the on-device rule, so it is not the default here. Mention it as an option only when he explicitly relaxes that constraint.

---

## Part A — Push-to-talk in Claude Code

macOS only. Apple Silicon strongly preferred (Metal GPU acceleration).

### A1. Prerequisites — paste these first

```bash
brew install cmake && xcode-select --install
```

`xcode-select --install` opens a system dialog. Click **Install** and wait for it to finish before continuing. If it says the tools are already installed, that is fine — carry on.

### A2. Install the plugin — type these inside Claude Code, not in Terminal

These are Claude Code slash commands. They go in the Claude Code prompt itself.

```
/plugin marketplace add enesbasbug/voice-to-claude
/plugin install voice-to-claude@voice-to-claude-marketplace
/voice-to-claude:setup
```

Setup downloads dependencies and builds whisper.cpp from source. Budget **3–5 minutes**. It is not frozen — leave it alone.

Note this builds its *own* copy of whisper.cpp. It does not reuse the Homebrew `whisper-cpp` from Part B, and it does not need it. Having both on the machine is expected and harmless.

### A3. Choose the model at setup

| Model | Size | Transcribe time | Use when |
|---|---|---|---|
| tiny | ~75 MB | ~0.5 s | Never — accuracy too low for his vocabulary |
| base | ~142 MB | ~1 s | Default. English-only prompts, speed matters |
| **medium** | ~1.5 GB | ~2 s | **Recommended.** Holds up on Hindi/Urdu code-switching |
| large-v3 | ~3 GB | ~3 s | Maximum accuracy, noticeably slower per prompt |

Pick **medium**. His dictation code-switches, and `base` degrades on that in a way he will read as "the tool is bad" rather than "the model is small." The extra second is a fair trade; three seconds per prompt (large-v3) is not, when the interaction is conversational.

Change it later with `/voice-to-claude:config`.

### A4. Grant two macOS permissions

macOS will prompt. If it does not, set them by hand:

- **System Settings → Privacy & Security → Microphone** → enable your terminal app
- **System Settings → Privacy & Security → Accessibility** → enable your terminal app

Accessibility is the one that lets the plugin type text at the cursor. Without it, recording appears to work and no text ever lands — a failure that looks like a broken microphone but is not.

### A5. Start the daemon

This is the step most write-ups omit, including the one he was given. The plugin runs as a background service and does nothing until it is started.

```
/voice-to-claude:start
```

| Command | Does |
|---|---|
| `/voice-to-claude:start` | Turn dictation on |
| `/voice-to-claude:stop` | Turn it off |
| `/voice-to-claude:status` | Is it running, and on which model |
| `/voice-to-claude:config` | Change model, hotkey, output mode |

### A6. Daily use

Hold **Ctrl+Alt** (Ctrl+Option on a Mac keyboard) → speak → release. Text appears at the cursor. Edit, then Enter.

### A7. Scope — do not overstate this

The project documents **Claude Code on macOS**. It is installed through Claude Code's plugin system and driven by Claude Code slash commands.

It types via keyboard injection, so text may well land in Cursor's terminal or another CLI — but the project does not claim that and it is not tested. If he needs dictation across every app, that is Wispr Flow's job, and Wispr Flow already does it. Do not promise him system-wide coverage this tool does not advertise.

### A8. When it breaks

```bash
tail -50 ~/.config/voice-to-claude/daemon.log
```

| Symptom | Cause to check first |
|---|---|
| Recording works, no text appears | Accessibility permission (A4) |
| Nothing happens on the hotkey | Daemon not started — `/voice-to-claude:status` |
| Setup fails partway | `cmake` or Xcode tools missing — rerun A1 |
| Transcription is wrong or garbled | Model too small — `/voice-to-claude:config` → medium |

Have him paste the last 50 log lines rather than describing the symptom. He will describe it in clinical terms; the log will say what actually happened.

---

## Part B — Sony recorder batch pipeline

For long-form speech. Read `references/sony_batch_pipeline.md` before touching this — it carries the corrected install steps and an explicit note about which parts have never been verified.

The short version: plug the recorder in, a `launchd` watcher fires, new audio is mirrored into `~/Voice-Inbox/`, whisper.cpp transcribes it locally, and `.txt` / `.srt` / `.vtt` land in a transcripts folder. Recorder folder names become the routing key.

**Privacy hard stop:** never route a folder that may contain patient identifiers to any cloud transcription service. Local whisper.cpp only. This is not a preference — it is the constraint that keeps the pipeline usable for clinical material at all.

---

## Handing work back to him

Follow the orchestrator's output contract in `spine/verify.md`: answer first, structure shown rather than described, a clinical analogy before any technical term, confidence stated High/Medium/Low with one line of why, and exactly one named next step — never a menu of options for him to choose between.

When a step is one he must perform on the Mac, say so explicitly and say where — Terminal or the Claude Code prompt. Those are different places and the commands are not interchangeable. Every install failure he has hit so far traces back to that distinction being left implicit.
