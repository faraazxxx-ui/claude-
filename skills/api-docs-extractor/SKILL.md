---
name: api-docs-extractor
description: >
  Recurrent skill that extracts the full content of any API documentation page
  (quickstarts, references, tutorials, SDK guides), normalizes it into a durable
  Markdown reference, and teaches the user how to functionally apply it through
  basic case practices. Use whenever the user shares a docs URL (docs.mistral.ai,
  platform.openai.com, any /docs/ path), asks to "extract everything from this
  page", wants a doc turned into a reusable reference, wants to learn an API
  workflow, or asks how to actually work with a tool given their preferences
  (verbal thinker, structured frameworks, conclusion-first output). Also
  trigger on requests for documentation digestion, API onboarding guides, or
  turning docs into practice exercises.
---

# API Docs Extractor

Extract any API documentation page into a permanent, structured reference, then convert it into a working practice loop so the knowledge compounds instead of evaporating.

## Output Protocol (every response)

1. **Final answer first** — conclusion or recommendation (2-3 sentences)
2. **Structured extraction** — complete, normalized Markdown (nothing dropped)
3. **Functional practice** — a minimal hands-on case the user can run immediately
4. **Next steps** — ordered, small, verifiable

## Workflow

### Phase 1 — Extraction (forensic, lossless)

1. Fetch the page (web_fetch or hidden connector tool if one exists for the platform).
2. Capture ALL of: title, URL, description, prerequisites, steps, code samples, parameter tables, notes/warnings, "what's next" links.
3. Distinguish **evidence** (verbatim from the page) from **inference** (anything you add). Mark inference explicitly.
4. Save the normalized extraction to `references/<source>-extract.md` in this skill folder (see `references/mistral-playground-extract.md` for the format).
5. Report dead links, JS-only content that failed to render, or paywalled sections honestly.

### Phase 2 — Reference card

Distill the extraction into a scannable card:

| Field | Value |
|---|---|
| **Tool** | e.g., Mistral Studio Playground |
| **Core action** | The one thing the page teaches |
| **Key parameters** | name → effect → typical values |
| **Prerequisites** | account/auth/keys |
| **Time to first result** | realistic estimate |

### Phase 3 — Basic case practice (learn by doing)

Build the smallest end-to-end exercise:

- One concrete goal (e.g., "compare temperature 0.1 vs 0.9 on the same prompt").
- Exact clicks or commands, numbered, no assumed knowledge.
- A **verify** step so success is observable.
- An **experiment grid**: vary one parameter at a time, record outputs, compare side by side. This mirrors the playground's own pedagogy — same prompt, different settings, diff the results.

### Phase 4 — Recurrence (make it a habit)

- Store each new extraction as its own reference file; the skill folder becomes a personal API library.
- On each new run, link back to prior extractions ("you learned X here; this page extends it with Y").
- End every run by proposing the next doc in the platform's learning path (the page's "What's next" section is the source of truth).

## Teaching Style (adapted to how this user works)

- **Conclusion before process.** State what to do and why first; steps second.
- **One variable at a time.** Never change model + temperature + prompt together; diff isolation is the whole point of parameter testing.
- **Frameworks over prose.** Tables, numbered steps, and grids; SCQH-style framing where applicable.
- **Say it, then do it.** Each concept pairs with a 2-minute hands-on case — reading docs without running the case is the shortfall this skill exists to fix.
- **Evidence vs. inference.** Quote docs verbatim for facts; clearly label anything interpreted, so trust in the reference never erodes.

## Example Run (Mistral playground page)

**Answer first:** The page teaches model/parameter evaluation before committing to an API integration — you test in the UI so you don't burn tokens or time in code.

**Extraction:** `references/mistral-playground-extract.md` (full page, lossless).

**Basic case:** Open Studio → Playground → pick `mistral-small-latest` → send "Explain the difference between supervised and unsupervised learning in three sentences." → set temperature 0.1, resend → set 0.9, resend → diff the two outputs → switch to `mistral-large-latest`, resend, diff again.

**Verify:** You can state, in one sentence each, what temperature did and how the two models differed on the identical prompt.

**Next:** "Create a reusable Prompt" → "Send your first API request" (per the page's What's next).

## Known Shortcomings This Skill Corrects

1. **Doc-skimming → doc-running.** The gap is never reading; it's executing. Every extraction MUST end in a runnable case.
2. **Parameter mystique.** Temperature/top-p/max-tokens stay abstract until diffed on identical prompts. The experiment grid makes effects visible.
3. **Knowledge evaporation.** Verbatim reference files + cross-links turn one-off reads into a compounding library.
4. **Choice paralysis (which model?).** The playground's compare-then-commit pattern is the decision procedure: same prompt, N models, pick on evidence.
