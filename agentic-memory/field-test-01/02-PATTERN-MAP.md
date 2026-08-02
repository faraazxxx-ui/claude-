# Phase R — Pattern Map (Field Test #1)

**What this is:** a behavioral map — a symptom diary of *how he works with AI*, built only from the atomic notes. **Hypothesis-generating, not diagnostic.** Every pattern lists the notes it rests on; nothing here is un-sourced.
**What this is NOT:** a claim about his health, his neurology, or the 45 conversations not in this batch.

## The five recurring patterns

| # | Pattern | Evidence (notes) | Where it stalls |
|---|---------|------------------|-----------------|
| P1 | **The "perfect output" recursion** — corrections demand an un-testable ideal ("perfect," "cognitive wish") and loop with no exit | N01, N07 | Loop can't terminate because "done" was never defined observably |
| P2 | **Shorthand that the AI must decode over rounds** — "audiovisuals," "cognitive wish" carry stable intent but lag interpretation | N02, N08 | 2–3 wasted rounds until the AI guesses "interactive dashboard" |
| P3 | **The predictable second step** — analysis is always followed by "Help me visualize this data" | N03 | An entire round spent asking for something foreseeable |
| P4 | **Heavy front-loaded scaffolding, versioned** — exact schemas/formulas/guardrails, maintained as v1→v2 | N04, N05, N12 | High authoring effort; brittle to missing inputs (see P5) |
| P5 | **Answer fragility on incomplete data** — headline metric swings ~1 point on same-day data gaps | N09, N10 | Trust risk: same question, two numbers, no completeness flag |

## Ask → Intent → Outcome deltas (where the ask and the real need diverge)

| Conversation | The literal ask | The inferred intent | The delta (the gap the loop paid for) |
|--------------|-----------------|----------------------|----------------------------------------|
| C1 | "Redo to the perfect output, red-team it, add audiovisuals" (×3) | "Give me a living, visual dashboard grounded in *my* real data" | Intent was stable at turn 1; 3 rebuild rounds spent because neither "perfect" nor "audiovisual" was operationalized. **N01, N02** |
| C2 / C4 | "Produce the 9-section report" | "Give me one trustworthy number + the top lever to pull" | Two runs, two Loop Scores; the durable signal (adherence) was the same both times but the score wasn't. **N09, N10** |
| C3 | "Recommend the correct wraps" (after delegating the specifics) | "Decide for me from the evidence; don't make me choose" | He *removed* constraints and handed the decision back — clarifying questions were friction, not help. **N06** |
| C5 | "Build a citation-rich synthesis" → "visualize this" | "Give me the map, then let me see it" | Cleanly scoped; the only delta was the foreseeable visualize-second step. **N03** |

## Correction pattern

He corrects **form and depth, never facts** (N07). Dissatisfaction reads as "make it better / deeper / more visual," not "that's wrong." Two consequences:
- **Strength:** he trusts the AI's substance and iterates on rendering — fast to a usable artifact.
- **Latent risk:** the content notes N15–N18 are all AI-synthesized and **unverified**; his correction budget currently never lands on fact-checking, so errors would survive his review.

## Stall points (the map's payload — where his approach breaks)

1. **No externalized "done."** P1's recursion is the headline stall. Fix already in hand: LOOP OS "Done-when" test on every task. *This is the single highest-leverage change.*
2. **Un-glossed shorthand.** P2 — "audiovisual," "cognitive wish," "red-team" mean specific things to him; unstated, they cost rounds. Fix: a 6-line glossary in his standing instructions.
3. **Un-pre-empted next step.** P3 — visualization is so reliably the next ask that not bundling it is pure waste. Fix: default clinical/research outputs to "report **+** dashboard" in one pass.
4. **Completeness-blind metrics.** P5 — a headline score with no data-completeness flag flips between runs. Fix: print "inputs present: X/Y" next to any composite score.
5. **Verification never enters the loop.** N07 — form gets iterated, facts don't. Fix: a one-line "flagged-for-verification" list appended to any citation-bearing output.

## The meta-observation

Across all five, the through-line is **N11**: he keeps hand-running an n-of-1 analysis (decode my data → score it → tell me what to do → now show me) and is simultaneously trying to *build the machine that does it automatically* (CNN→RNN→RL "second brain"). The LOOP OS he operates under, and this Agentic-Memory field test, are the same project from a different angle: **externalize the loop so it stops living in a saturating chat thread and starts living in a retrievable system.** Every stall above is a place where that externalization hasn't happened yet.

## Confidence on the map as a whole

**Medium.** *Why:* the five patterns are each multiply-sourced and internally consistent, but the sample is 5/50 conversations, all from one ~2-week window, all health-topic. P1–P3 are High individually (verbatim repetition); P4–P5 are Medium; the generalization to "how he thinks overall" is **Low** until non-health, older conversations are added (see `03-GAP-LIST.md`).
