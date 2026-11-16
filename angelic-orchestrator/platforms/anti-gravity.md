# Google Anti Gravity (IDE) — install the angelic-orchestrator pack

**Mechanism (verified 2026-11-12, antigravity.google/docs, reviewed 2026-10):** Anti Gravity reads **rules** from `AGENTS.md` / `GEMINI.md` / `.agents/rules/*.md` in the workspace **and any parent folder up to the repo root**, plus global rules at `~/.gemini/AGENTS.md`, `~/.gemini/config/AGENTS.md`, `~/.gemini/config/rules/*.md`. Rules are cumulative. Repeatable procedures live in **skills**: workspace `.agents/skills/<name>/SKILL.md`, global `~/.gemini/config/skills/` and `~/.gemini/antigravity-cli/skills/`. Legacy `.agents/workflows/` stop working **2026-10-19** — use skills. Agents require a **trusted workspace**; every run produces reviewable **artifacts**; non-workspace file access is off by default.
**Confidence: High** — Google's own docs.

## Steps

1. In the `faraazxxx-ui/claude-` clone opened as a workspace, add `AGENTS.md` at the repo root (if absent) containing `platforms/_BOOTSTRAP.md`, plus one line: "Canonical memory: `angelic-orchestrator/CANONICAL_MEMORY.md` — read it at session start; it is the source of truth; follow its standing rules 1-10."
2. Global layer: put the same one-liner + pointer in `~/.gemini/AGENTS.md` so every Anti Gravity workspace gets the rule.
3. Add a workspace skill `.agents/skills/angelic-orchestrator/SKILL.md` whose body points at `angelic-orchestrator/LEARNING_LOOP.md` for the write-back protocol, so the agent emits WRITE-BACK blocks at task end.
4. Keep the canonical pack itself in the repo (Anti Gravity reads repo files directly — this is the one platform where "attach the file" is native). Version-stamp check at session start is a rule in the bootstrap.
5. Monthly: no platform memory to audit — the repo is the memory. Just keep the branch pulled.

## Privacy

Trusted-workspace model means anything in the workspace can be read by the agent — keep Confidential folders out of the Anti Gravity workspace, or gate them with a rule line: "Never read or quote `skills/apex-legal-strategy/`, `legal-endeavors/`, `health_analysis*/`, `analysis-output/`."
