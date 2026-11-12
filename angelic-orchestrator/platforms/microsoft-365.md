# Microsoft 365 Copilot (Enterprise) — install the angelic-orchestrator pack

**Mechanism (verified 2026-11-12, Microsoft Learn + Microsoft Tech Community):** Copilot **Memory** (saved memories + inferences) and **Custom Instructions** (Settings and more → Chat settings → Personalization → Custom instructions) personalize Copilot Chat. Enterprise: available with a Copilot license; admin controls exist (Enhanced personalization, Custom instruction controls). Memory/custom instructions are **not available for Agents**; for agent-grade standing context use **Copilot Studio** (declarative agents with instructions + knowledge sources). Copilot Cowork has its own Customize → Preferences instructions (documented 20 KB limit).
**Confidence: High** — Microsoft's own documentation.

## Steps

1. Settings and more → Chat settings → Personalization → **Custom instructions**: paste `platforms/_BOOTSTRAP.md`.
2. Tell Copilot once: "Please remember: my angelic-orchestrator canonical pack governs how you answer — rules 1-10, answer-first, confidence stated, one next step; Confidential litigation/medical material is never remembered."
3. Store the full pack as files in **OneDrive** (`/angelic-orchestrator/`) so Copilot's work-content grounding can read `CANONICAL_MEMORY.md` when asked; reference it by name in custom instructions.
4. For scheduled/standing agent behavior, build a **Copilot Studio** agent with the bootstrap as its instructions and the OneDrive files as knowledge.
5. Monthly: Manage saved memories → delete drift vs the canonical pack.

## Privacy

Enterprise tenant: check with the admin whether Enhanced personalization is on. Treat work-graph data as Private work; litigation/medical = never in Copilot memory, never in OneDrive shared with the org.
