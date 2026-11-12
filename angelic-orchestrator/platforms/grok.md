# Grok — install the angelic-orchestrator pack

**Mechanism (2026 guides; verify in UI on first use):** Custom Instructions (cap reduced 12,000 → **4,000 chars** in 2026) apply to every new chat; **Workspaces** isolate project context and can hold files; up to **4 Custom Agents** (rolled out March 2026), each with its own instructions; Grok has a **Memory** feature that accumulates context automatically.
**Confidence: Medium** — from 2026 third-party guides, not xAI's own docs; confirm current limits in Settings on first use.

## Steps

1. Settings → **Custom Instructions**: paste `platforms/_BOOTSTRAP.md` (fits the 4,000-char cap). Do NOT paste the full canonical pack here — it will not fit.
2. Create a **Workspace** named `angelic-orchestrator`; upload `CANONICAL_MEMORY.md` + `LEARNING_LOOP.md` as workspace files, and put one instruction line in the workspace: "The uploaded canonical pack is my source of truth; follow its rules 1-10."
3. Optionally dedicate one of the 4 **Custom Agent** slots to "orchestrator" with the bootstrap as its instructions.
4. Monthly: review Grok **Memory**; delete entries contradicting the canonical pack (watch for personality/instruction drift in long chats).

## Ask it to remember (one-shot)

> "Remember: my angelic-orchestrator canonical pack is in the angelic-orchestrator Workspace files; the repo is the source of truth; rules 1-10 apply to every answer; never save litigation or medical details."

## Privacy

The project you referenced (grok.com/project/ef2c7a89-...) already exists — put the workspace files there so the project itself carries the pack.
