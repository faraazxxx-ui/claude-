# ChatGPT — install the angelic-orchestrator pack

**Mechanism (verified 2026-11-12, OpenAI Help Center / 2026 guides):** Custom Instructions (Settings → Personalization → Custom Instructions, two text boxes) apply to every chat; Memory (Settings → Personalization → Memory) auto-saves facts + can reference chat history; Projects hold files that persist per project. Memory does **not** leave ChatGPT.
**Confidence: High** — stated in OpenAI's own docs.

## Steps

1. Settings → Personalization → **Custom Instructions**: paste `platforms/_BOOTSTRAP.md` into "How would you like ChatGPT to respond?"; put one line in "What would you like ChatGPT to know about you?": "See my angelic-orchestrator canonical memory (attached in Projects); repo is source of truth."
2. Create a **Project** named `angelic-orchestrator`; upload `CANONICAL_MEMORY.md` and `LEARNING_LOOP.md` as project files. Pin the bootstrap in the project instructions too.
3. In Memory settings, leave **Saved memories ON**, decide on Reference chat history (recommend OFF for work chats — it drifts).
4. Monthly: Manage memories → delete anything contradicting `CANONICAL_MEMORY.md`.

## Ask it to remember (one-shot)

> "Remember: my angelic-orchestrator canonical pack is the project files in the angelic-orchestrator Project; the repo faraazxxx-ui/claude- is the source of truth; standing rules 1-10 in the bootstrap apply to every answer; Confidential material (litigation, medical) is never saved to memory."

## Privacy

Do not enable memory contribution from chats that touch litigation or medical material — use Temporary Chat for those.
