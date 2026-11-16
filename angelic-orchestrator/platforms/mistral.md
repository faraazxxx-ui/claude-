# Mistral La Plateforme / API / Vibe — install the angelic-orchestrator pack

**Mechanism:** The Mistral API is **stateless** — no memory, no custom-instructions field, nothing persists between calls. Every request must carry its own context.
**Confidence: High** — statelessness is structural to any API, not a product setting.

## Steps

1. Keep `platforms/_BOOTSTRAP.md` + `CANONICAL_MEMORY.md` as files; prepend them to the `system` message of every API call (or the system prompt in Vibe / any Mistral-based client).
2. Minimal wrapper pattern:

```python
system = open("angelic-orchestrator/platforms/_BOOTSTRAP.md").read() + \
         open("angelic-orchestrator/CANONICAL_MEMORY.md").read()
client.chat.complete(model="mistral-large-latest",
                     messages=[{"role": "system", "content": system}, ...])
```

3. For long-running use, cache the combined system prompt (prompt caching) so the pack costs nothing per call after the first.
4. No monthly audit needed — there is no server-side memory to drift. The repo version stamp is still checked at wrapper startup.

## Privacy

API calls send the system prompt to Mistral's servers — the pack is Private work; never include Confidential attachments in the same call.
