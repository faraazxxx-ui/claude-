# Le Chat (Mistral) — install the angelic-orchestrator pack

**Mechanism:** Le Chat supports **Agents** with custom system instructions and per-agent context; account-level custom instructions have existed in different forms across releases. **No cross-platform memory sync exists.**
**Confidence: Medium** — recalled from Mistral's 2025-2026 product changes; verify the current Settings → Agents / instructions UI on first use. If no persistent instructions field exists, create one dedicated Agent named `angelic-orchestrator` and always start project chats there.

## Steps

1. Create an **Agent** named `angelic-orchestrator`; set its system instructions to `platforms/_BOOTSTRAP.md` + `CANONICAL_MEMORY.md` (agents can hold longer instructions than a settings text box).
2. Attach/upload `CANONICAL_MEMORY.md` and `LEARNING_LOOP.md` to the agent or keep them in a project folder Le Chat can read, and reference them by name in the instructions.
3. If Le Chat offers account-level custom instructions, put the one-line pointer there: "Project chats must use the angelic-orchestrator agent."
4. Monthly: re-read the agent instructions against the repo version stamp; update on bump.

## Ask it to remember (one-shot)

> "Remember: I work on the angelic-orchestrator project; my canonical memory is in this agent's files; rules 1-10 in the bootstrap apply to every answer; never store litigation or medical details."

## Privacy

Le Chat is a SaaS — Confidential material stays in local sessions only; do not upload apex-legal or health files.
