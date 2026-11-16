# Verified facts ledger

Every line here was checked against a primary source on the date shown. Anything not on this list is unverified — go read the source before repeating it to Dr. Rahman.

Add to this file whenever you verify something new. The point is that the next session inherits the check instead of re-running it, and that nobody has to trust recall.

## Confirmed — 2026-08-29

| Fact | Source |
|---|---|
| `enesbasbug/voice-to-claude` exists; Claude Code plugin, whisper.cpp + Metal, macOS | repo README |
| Install is via plugin marketplace, not `git clone` | repo README quick start |
| Default hotkey is **Ctrl+Alt** (Ctrl+Option on macOS) | repo README |
| Setup **builds its own** whisper.cpp; takes 3–5 min | repo README |
| Prerequisites: `brew install cmake && xcode-select --install` | repo README |
| Commands: `:setup` `:start` `:stop` `:status` `:config` | repo README |
| Runs as a **daemon** — must be started before the hotkey does anything | repo README |
| Permissions: Microphone **and** Accessibility | repo README troubleshooting |
| Models: tiny ~75MB · base ~142MB (default) · medium ~1.5GB · large-v3 ~3GB | repo README |
| Latency: tiny ~0.5s · base ~1s · medium ~2s · large-v3 ~3s | repo README table |
| Log path `~/.config/voice-to-claude/daemon.log` | repo README |
| Claude Code has built-in `/voice`; streams audio to Anthropic; needs Claude.ai auth | shipped 2026-03-03 |
| `brew install whisper-cpp` is a real Homebrew formula | formulae.brew.sh |
| `ggml-large-v3-turbo.bin` = 1,624,555,275 bytes (1.62 GB) | HTTP HEAD, huggingface.co |
| `ggml-medium.bin` = 1,533,763,059 bytes (1.53 GB) | HTTP HEAD, huggingface.co |

## Corrected — claims that were wrong in the 2026-08-29 briefing doc

These were stated confidently and were false. They are recorded so the same errors are not reintroduced.

| Was claimed | Actually |
|---|---|
| `git clone` + `pip install -r requirements.txt` | Plugin marketplace install — the clone method does not install it |
| Hotkey "Right-Option or similar" | Ctrl+Alt |
| Requires the whisper.cpp already installed for the Sony pipeline | Builds its own; the Homebrew one is separate and unused by it |
| "Works in Claude Code, Cursor, grok CLI identically" | README documents Claude Code / macOS only. Untested elsewhere. |
| Uses large-v3-turbo | That model belongs to the Sony pipeline. Plugin offers tiny/base/medium/large-v3. |
| "Long rambles stitch awkwardly at 0.5s chunk boundaries" | Does not apply. That is `whisper-stream`'s example flag; this tool is push-to-talk — one file, no chunking. |
| Implied it works once installed | Daemon must be started with `/voice-to-claude:start` |
| "Token-free… saves tokens" | False frame. See SKILL.md — dictation cannot save tokens and tends to raise them. |

## Not verified — do not assert these

- Whether keyboard injection reliably reaches Cursor, grok CLI, or other apps. Plausible, undocumented, untested.
- The contents and correctness of `sony_sync.sh` and `com.faraaz.sonysync.plist`. Never inspected — they were produced in an earlier session and were not available for review.
- ElevenLabs Scribe pricing (~$0.22/hr was claimed). Not checked. Do not quote a price without checking it.
- Whether `launchd` `WatchPaths` on `/Volumes` fires reliably on every mount across current macOS versions.
