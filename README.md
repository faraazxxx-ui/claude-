# claude-

Dr. Rahman's working repository and second brain.

**Start at [`brain/index.md`](brain/index.md).** That is the hub — everything durable is reachable
from it. If you are an agent, [`CLAUDE.md`](CLAUDE.md) loads automatically and tells you the rules.

---

## What is here

| Path | What it is |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Operating instructions. Every Claude Code session reads this first. |
| [`brain/`](brain/) | The corpus. Concepts, projects, decisions, session logs. The part that persists. |
| [`tools/`](tools/) | Two measurement scripts. Pure standard library, no dependencies. |
| `ingest/` | Drop zone for chat exports. Gitignored. |
| everything else | Prior work — health analyses, legal strategy, prompt collections, seven skills. Real, useful, not organised. Cite it; don't duplicate it. |

## The idea

Most of the Claude stack has a half-life measured in hours. The context window forgets at the end of
the conversation, prompts are rewritten from scratch each time, connectors fetch but never file.
Only three layers compound: skills, automation, and a written corpus.

This repository is the corpus. `CLAUDE.md` is what makes every session read it before working and
write to it before finishing, so that work accumulates instead of restarting.

The full reasoning is in [`brain/concepts/claude-layers.md`](brain/concepts/claude-layers.md) and
[`brain/concepts/wiki-method.md`](brain/concepts/wiki-method.md).

## Tools

```bash
# Version churn, finality claims, byte-identical duplicates
python3 tools/corpus_forensics.py files . -o brain/_forensics

# Specification gap, restart families, abandonment, circadian pattern
# (put Claude and/or ChatGPT conversations.json in ingest/ first — see ingest/README.md)
python3 tools/corpus_forensics.py chats ingest/ -o brain/_forensics --tz-offset -5

# Broken links, orphans, hubs, staleness, link graph
python3 tools/wiki_lint.py brain --mermaid brain/_forensics/graph.md
```

`corpus_forensics.py` reads both Claude and ChatGPT export formats and detects which is which.
`wiki_lint.py` exits non-zero on broken links, so it works as a pre-commit hook.

Current measurements live in [`brain/_forensics/`](brain/_forensics/).
