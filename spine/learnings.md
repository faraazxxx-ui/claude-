# Learnings

What is now known that was not before. Append only, dated.

Distinct from `failure.md`: that file records what broke, this one records what is now true. Some entries here came from a failure; some came from simply checking something nobody had checked.

---

## 2026-08-29 — Voice dictation cannot save tokens, and the belief that it can is expensive

The premise behind the whole dictation push was that local transcription would save tokens. It cannot.

Claude Code's prompt has always been text — there was never an audio token charge to avoid. The built-in `/voice` bills transcription, a separate service, not model context. So local whisper.cpp was being compared against a cost that did not exist.

What it genuinely buys is privacy (audio never leaves the Mac) and no per-hour transcription fee. Both real, neither tokens.

The sharp edge: dictated prompts run materially longer than typed ones, so voice input **raises** token use per turn. Optimising capture to save tokens moves the number the wrong way. The lever is prompt discipline and batching long thinking through the Sony pipeline.

Generalises past voice: a stated goal ("save tokens") can be attached to a mechanism that does not serve it, and the mechanism can still be worth having for different reasons. Check that the lever moves the stated variable before optimising it — otherwise effort goes into something that looks like progress and is not.

---

## 2026-08-29 — Confident recall is more expensive for a non-coder than admitted uncertainty

Standard practice treats a hedge as a small cost — slightly less useful, slightly less crisp. For someone who cannot audit the output, the arithmetic inverts.

A hedged wrong answer costs a verification step. A confident wrong answer costs an afternoon, plus the trust that made the next answer usable.

So the reflex "sound authoritative, it's more helpful" is actively wrong here. Say which parts were verified and which were recalled, and the recalled parts get checked instead of pasted.

---

## 2026-08-29 — A gate that reads missing files does not fail, it silently vanishes

Gate 0 ran twice against files that did not exist and never announced it. Nothing errored. The gate simply was not there.

This is the failure mode of every check defined as "read X and consider it" — absence and satisfaction produce identical behaviour. A check needs a defined response to its own inputs being missing, or it is decorative under exactly the conditions where it matters most.

Hence `goal.md` now announces `STATUS: UNSET` in its own body rather than sitting empty. A file that declares its emptiness is a live gate; an absent file is not.

---

## 2026-11-12 — No AI platform syncs memory with another; "same memory everywhere" must be built, not found

Verified in ChatGPT's and Gemini's own 2026 documentation: each platform's memory stays inside that product. So the request "the same instructions and memories in Le Chat, Mistral, Grok, ChatGPT, Gemini, M365, Hermes and Anti Gravity" cannot be delegated to any single vendor's memory feature. The working architecture is: one canonical pack in a repo the user controls (source of truth) + a bootstrap pasted into each platform (its cache) + an append-only write-back loop into the repo (perpetual learning). This is now implemented in `angelic-orchestrator/`.

---

## 2026-11-12 — Platform memory boxes have hard limits and drift; durable context belongs in files you control

Checked 2026-11-12: Grok custom instructions capped ~4,000 chars; ChatGPT memory truncates/summarizes long entries and auto-curates (drift); Gemini Gems become read-only 2026-11-17 (replaced by Skills); Copilot memory/custom instructions don't apply to Agents; Anti Gravity and Hermes read files (AGENTS.md / MEMORY.md) natively; the Mistral API is stateless. Consequence baked into the pack: the full canonical memory lives in repo files, platform text boxes carry only the short bootstrap, and platform memories are audited monthly against the repo, which always wins on conflict.
