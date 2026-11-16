# Hermes Agent (Nous Research, self-hosted) — install the angelic-orchestrator pack

**Mechanism (verified 2026-11-12, official docs + repo):** Hermes has a **closed learning loop**: agent-curated persistent memory written to `MEMORY.md` / `USER.md` (with periodic nudges), autonomous **skill creation** (SKILL.md files it writes and self-improves after complex tasks), FTS5 cross-session search of past conversations, optional memory-provider plugins (RetainDB, ByteRover, Honcho, Supermemory, Mem0…) via `hermes plugins install <name>`, and consent-aware write gating (`/skills approval on`) so skill writes can be staged for review.
**Confidence: High** — Nous Research's own documentation.

## Steps

1. In `~/.hermes/` (or the profile dir), place the pack where Hermes reads memory: append a pointer section to `MEMORY.md`: "Canonical pack: the angelic-orchestrator repo (faraazxxx-ui/claude-, `angelic-orchestrator/CANONICAL_MEMORY.md`) is the source of truth; bootstrap rules 1-10 apply to every answer." If the repo is cloned locally (e.g. `~/claude-`), reference the local path so Hermes can read the file directly.
2. Have Hermes ingest the pack once: "Read `angelic-orchestrator/CANONICAL_MEMORY.md` and `LEARNING_LOOP.md` and save the standing rules to memory."
3. Turn on `/skills approval on` at least until the first skills are vetted — this is the write-back gate.
4. Hermes' own learning loop then does the perpetual part natively: it saves durable facts to MEMORY.md and writes reusable skills. Weekly, Dr. Rahman reviews new entries and files anything durable into `spine/learnings.md`.
5. Monthly: diff MEMORY.md against the canonical pack; drift gets corrected in the repo first, then re-ingested.

## Privacy

Hermes is self-hosted — the right home for Private work, but keep Confidential (litigation, medical) in local-only folders it must not sync anywhere; do not connect it to messaging platforms for those topics.
