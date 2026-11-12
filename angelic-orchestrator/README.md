# Angelic Orchestrator — Canonical Memory Pack

**Privacy zone: Private work.** Personal context. Never paste Confidential+ material (litigation, medical) into any platform — those live only in `skills/apex-legal-strategy/`, `legal-endeavors/`, `health_analysis*/`, `analysis-output/` and stay local.

## The question you asked

Restated precisely: *"One project (angelic-orchestrator), one set of instructions and memories, present and behaving the same in Le Chat, Mistral, Grok, ChatGPT, Gemini, Microsoft 365 Enterprise, Hermes Agent and Anti Gravity — plus a mechanism that keeps learning forever. What is that question really asking, and what is the answer?"*

## The answer

**No AI platform syncs its memory with another** (verified 2026-11-12 in ChatGPT's and Gemini's own docs — each says memory stays inside its product). So the mechanism cannot live in any one platform. It is:

1. **One canonical pack in this repo** = source of truth (`CANONICAL_MEMORY.md`, versioned).
2. **One bootstrap pasted into each platform** = that platform's cache (`platforms/`).
3. **One append-only learning loop** = new facts written back to `spine/` logs, consolidated into the canonical pack (`LEARNING_LOOP.md`).

Confidence: High for the architecture claim; per-platform mechanism details are tagged High/Medium in `platforms/` with the verification date.

## What's here

| File | Holds |
|---|---|
| `CANONICAL_MEMORY.md` | The instructions + memories every platform receives. Version-stamped. |
| `LEARNING_LOOP.md` | The perpetual learning mechanism: capture → tag → write-back → consolidate → re-emit. |
| `platforms/_BOOTSTRAP.md` | The short paste-able instruction block for any platform's custom-instructions field. |
| `platforms/*.md` | One install file per platform: Le Chat, Mistral, Grok, ChatGPT, Gemini, M365, Hermes, Anti Gravity. |

## Install map

| Platform | File | Where the memory lands | Confidence (why) |
|---|---|---|---|
| ChatGPT | `platforms/chatgpt.md` | Custom Instructions + Project files + Memory | High — OpenAI Help Center, 2026 |
| Gemini | `platforms/gemini.md` | Instructions for Gemini + Skills (Gems go read-only 2026-11-17) | High — Google support docs, 2026 |
| Grok | `platforms/grok.md` | Custom Instructions (4,000-char cap) + Workspace files | Medium — 2026 guides, verify in UI on first use |
| Le Chat | `platforms/le-chat.md` | Agent/system instructions | Medium — recalled, verify on first use |
| Mistral (La Plateforme / API) | `platforms/mistral.md` | Nothing persistent — prepend bootstrap every call | High — APIs are stateless by design |
| Microsoft 365 Copilot | `platforms/microsoft-365.md` | Copilot Memory + Custom Instructions (Enterprise) | High — Microsoft Learn, 2026 |
| Hermes Agent | `platforms/hermes-agent.md` | `MEMORY.md` / `USER.md` + self-written skills | High — official docs, 2026 |
| Anti Gravity | `platforms/anti-gravity.md` | `AGENTS.md` / `.agents/rules/` in the workspace + global rules | High — antigravity.google/docs, reviewed 2026-10 |

## Next step (one)

Paste `platforms/_BOOTSTRAP.md` + `CANONICAL_MEMORY.md` into **ChatGPT** first (Custom Instructions for the short block, a Project with the full file attached), then work down the install map. After that, fill `spine/goal.md` — it is still UNSET and Gate 0 is not fully loaded without it.
