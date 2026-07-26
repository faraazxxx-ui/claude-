# 2026-07-26 — Claude's layers, and why wiki pages

**Asked:** teach Claude in its layers, and explain the point of wiki pages in building a second
brain.

**Wanted:** something different, and worth recording precisely because the gap was the whole
finding. The request read as a knowledge gap — *I am a few clicks behind optimal use*. It was not.
This repository already contained seven skills, a 30k-word embedding guide, four generations of
health analysis, and a genuinely good entity registry. The gap was never knowledge. It was that
nothing persisted between sessions, so every session started cold and produced a new top-level
directory. The teaching was necessary but secondary; the missing `CLAUDE.md` was the actual answer.

**Produced:**

- `CLAUDE.md` — the spine. Loaded automatically by every future Claude Code session. Its absence
  is the single-line explanation for twelve sessions of divergent output.
- `brain/index.md` — the hub, and the one address that has to be remembered.
- `brain/concepts/` — `claude-layers`, `wiki-method`, `ai-medicine-rosetta`,
  `adhd-operating-system`, `anti-versioning`.
- `brain/projects/second-brain.md` — state, ordered next actions, promotion queue.
- `brain/_templates/` — concept, project, person, decision, session.
- `tools/corpus_forensics.py` — chats mode (specification gap, restart families, abandonment,
  circadian) and files mode (version families, finality claims, duplicates). Reads both Claude and
  ChatGPT export formats. Pure stdlib; tested against synthetic exports in both schemas.
- `tools/wiki_lint.py` — broken links, orphans, hubs, staleness, Mermaid graph. Non-zero exit on
  broken links.
- `.claude/skills/second-brain/SKILL.md` — makes the protocol self-operating.
- `brain/_forensics/` — baseline measurement of this repository.

**Measured, not asserted:** 12.0% of 242 files carry a finality or version token. 3 byte-identical
duplicate groups. 5 version families over 14 files. The health analysis exists in four generations.

**Found along the way:** the repository is public, and has been since 2026-02-08. 18 tracked files
contain third-party names or active-case references, including litigation strategy; 14 more hold
personal clinical data. No credentials. 0 forks, 0 stars, 0 watchers, so exposure is likely minimal.
This displaced everything else as the top priority — see item 0 in [[second-brain]].

**Next action:** make the repository private. Settings → General → Danger Zone.

## Links

- [[index]] · [[second-brain]] · [[claude-layers]] · [[wiki-method]]
