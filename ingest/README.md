# Drop zone

Raw exports land here. Contents are gitignored — this directory is a staging area, not part of the
corpus. Conclusions go in `brain/`; raw material stays here.

## Getting your chat exports

**Claude** — Settings → Privacy → Export data. Arrives by email as a zip. Unzip; you want
`conversations.json`.

**ChatGPT** — Settings → Data controls → Export data. Same idea, also `conversations.json`, a
different internal format. `corpus_forensics.py` detects and handles both, and will read several
files in one run, so you can analyse them together.

Rename them so you can tell them apart, e.g. `claude_conversations.json` and
`chatgpt_conversations.json`, then:

```bash
python3 tools/corpus_forensics.py chats ingest/ -o brain/_forensics --tz-offset -5
```

`--tz-offset -5` puts the circadian histogram in Eastern time. Use -4 during daylight saving.

## What comes out

- `brain/_forensics/chats_report.md` — correction rate (your specification gap), restart families,
  abandonment, depth, and the hour-by-hour map of when you actually engage.
- `brain/_forensics/metrics.json` — the same numbers, machine-readable.
- `brain/_forensics/seeds/` — a stub page per topic you have raised across many conversations
  without ever writing it down once. These are the pages your corpus is missing.

Read the derivation/validation warning in `brain/concepts/ai-medicine-rosetta.md` before drawing
conclusions. This output is diagnosis, not prescription.
