# Loops, in Plain English

*For a verbal, iterative thinker. Every technical word is defined the moment it appears. Written 2 August 2026.*

**First, the label.** "Loop engineering" is an **informal practitioner term**, not Anthropic's. Practitioner write-ups credit developer Peter Steinberger with coining it in June 2026. Anthropic's own public materials say **"loops," "loop patterns," "the agentic loop,"** and **"evaluator-optimizer."** Anthropic's webinar [*Startup Builds: Getting Started with Loops*](https://www.anthropic.com/webinars/startup-builds-getting-started-with-loops) (24 July 2026) never uses the phrase "loop engineering." Use the term in conversation if you like; don't cite it as Anthropic's.

---

## 1. The idea in one sentence

Instead of writing one perfect instruction, you set up a short repeating cycle — do the work, check it, fix what failed — and the thing you actually design is **the check and the moment you stop**.

## 2. What a loop is

A loop is a cycle you run more than once, on purpose, with the output of one turn feeding the next.

Three parts, always:

1. **An attempt** — something gets produced.
2. **A check** — the attempt is compared against a standard.
3. **A decision** — good enough (stop), or not (fix and go again).

If any of those three is missing, it isn't a loop. Two attempts with no check between them is just doing it twice.

## 3. What is being engineered

Not the prompt. People assume "loop engineering" means engineering better instructions. It doesn't. You are designing four things:

1. **The standard** — what "done" means, written down before you start.
2. **The check** — how you find out whether the standard was met.
3. **The repair rule** — what gets changed when the check fails (ideally: only the failing part).
4. **The exit** — when you stop, including when you stop *without* success.

Anthropic's Claude Code documentation puts the point bluntly: *"Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal available, and you become the verification loop."* ([Best practices for Claude Code](https://code.claude.com/docs/en/best-practices), retrieved 2 Aug 2026.)

**Jargon translated:** an *agentic loop* just means the AI runs the cycle itself instead of waiting for you to say "again." *Ground truth* — Anthropic's phrase — means a real result from the outside world (a test that ran, a file that exists, a source you can open), as opposed to the model's own opinion of its work.

## 4. A simple everyday analogy

You're a physician, so use the one you already run every day: **a diagnostic workup.**

You don't write one perfect order set on admission and walk away. You order a test, read the result, narrow the differential, order the next test. And you have a rule that stops you: **you stop when the next test wouldn't change management.**

That's a loop, and you've been running it for years. The prompt is the order. The check is the result coming back. The stopping rule is "would this change management?" Everything else in this document is that idea moved onto a keyboard.

*(The analogy is mine, not Anthropic's.)*

## 5. Three concrete AI examples

**A writing loop — draft, critique, revise**
> "Write a 200-word patient handout on POTS at an 8th-grade reading level. Then check it against three things: no word above 8th grade, every claim traceable to a named source, under 200 words. Fix only what fails. Show me what failed."

The check is mechanical: reading level, sourcing, length. You can tell whether it passed without re-reading the whole thing.

**A research loop — search, find gaps, search again, synthesize**
> "Find the current evidence on X. List what you found and, separately, list what you *couldn't* find. Then run a second round targeting only the gaps. Stop after the second round and tell me what's still missing."

The check here is coverage, and the crucial part is *"list what you couldn't find."* That's what turns a confident summary into an honest one.

**A work loop — do it, check against criteria, correct failures**
> "Draft the LLC formation checklist. Then verify: every step names the filing body, every step names the form number, no step needs my SSN in the document. Fix failures. Report the check results, not just the corrected version."

The last clause — *report the check results* — is what keeps you from having to redo the checking yourself. Anthropic's phrasing: *"Have Claude show evidence rather than asserting success."*

## 6. How your "prompting" folder method fits

Your folder is the memory the loop doesn't have. Every conversation starts from zero; the model forgets. Your folder doesn't.

That makes it genuinely valuable. But right now it stores the **wrong half** of each loop. It keeps the *attempts* — the prompt versions — and throws away the *checks*: what you were hoping for, what actually went wrong, why v2 exists.

Six months later, a folder of attempts tells you what you wrote. A folder with checks tells you what "good" meant, and whether you ever hit it.

**One-line fix:** every time you save a version, add two sentences — *what this was supposed to achieve* and *what the last version got wrong*. That's it. That single habit converts the folder from an archive into a record you can learn from.

## 7. Why this is different from writing one perfect prompt

A perfect prompt is a **prediction**: you're guessing every way the answer could go wrong, in advance, before you've seen a single output.

A loop is a **measurement**: you let it go wrong, then catch it.

Prediction is expensive and unreliable — that's why your prompts keep growing. Measurement is cheap, because you only fix what actually broke.

Anthropic recommends the measurement approach directly: *"It's best to start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples to improve performance based on failure modes found during initial testing."* ([Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 29 Sept 2025.)

There's also a hard ceiling on perfectionism. Anthropic warns that over-long instruction files backfire: *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"* Past a certain length, adding more instructions makes the model follow **fewer** of them. The perfect prompt doesn't just fail to arrive — chasing it actively degrades results.

## 8. Why AI self-critique is not the AI getting smarter

This is the most misunderstood part, so here it is plainly.

**During your conversation, the model does not change.** Its underlying settings — the weights, fixed during training months ago — are frozen. Nothing you say edits them.

So what improves? **The page, not the mind.** When the model critiques its own draft, it's re-reading text that's now sitting in front of it and writing a better draft *in light of that text*. It's a person re-reading their own paragraph with fresh eyes — the paragraph gets better, the person's vocabulary doesn't.

And it evaporates. Close the window and every "improvement" is gone. The model starts the next conversation exactly as capable, and exactly as ignorant of your preferences, as it started this one. **The only thing that carries over is what you saved** — which is precisely why your folder instinct is correct.

The thing people confuse this with has a proper name: **recursive self-improvement**, an AI autonomously designing and building its own successor. Anthropic addresses it directly in [*When AI builds itself*](https://www.anthropic.com/institute/recursive-self-improvement) (May 2026, Marina Favaro & Jack Clark), describing it as *"AI system capable of fully autonomously designing and developing its own successor"* and stating: **"We are not there yet, and recursive self-improvement is not inevitable."** Humans, the piece notes, still "set research directions and judge results."

So: self-critique in your chat window is a **draft getting better**. Recursive self-improvement is a **model getting better**. They are not on the same scale, and the first is not a small version of the second.

## 9. Where loops fail

**Repetition.** The loop keeps producing near-identical versions. *Tell:* the diff between rounds is mostly reordering and synonyms. Your Ghusoon v1→v2 changed 175 of 449 lines, and a good share of that was numbered-list-to-bullets and a retitle.

**Error amplification.** A mistake in round one gets treated as established fact in round two and defended by round three. Nothing re-checks the original premise, so a wrong assumption hardens with every pass.

**False confidence.** Each round *sounds* more authoritative because it's more polished. Polish is not accuracy. A file in your store carries `Confidence: 98.7` — a decimal-point confidence figure with no method behind it. It reads as rigor; it's decoration.

**Drift from the goal.** You started wanting a clear one-page brief; nine rounds later you have a 12-section framework nobody asked for. Anthropic observed the flip side in long agent runs: *"a later agent instance would look around, see that progress had been made, and declare the job done"* ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), 26 Nov 2025, Justin Young). Both are drift — the loop loses hold of the original target.

**Endless revision.** The structural one, and Anthropic names the mechanism: *"A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do. Chasing every finding leads to over-engineering."*

Read that twice. **If you ask for critique, you will always receive critique.** Criticism arriving is not evidence that something is wrong. So "the AI still found issues" can never be your reason to keep going — it's guaranteed regardless of quality.

## 10. A practical loop you can reuse

**Stage 1 — Define the outcome and the completion test.**
One sentence each. *Outcome:* what the finished thing must let someone do. *Done when:* the observable condition. Write both **before** the first prompt.

**Stage 2 — Produce the first attempt.**
Short and honest, not maximal. You're generating something to measure, not something to submit.

**Stage 3 — Evaluate against explicit criteria.**
Use your own three headings — **Vulnerability / Ambiguity / Inefficiency** — plus "does it pass the completion test?" Ask for the *list of failures*, not a rewrite.

**Stage 4 — Revise only the identified weaknesses.**
Name the defect, then fix that. Never "improve it" — that's a request for a full rewrite, and it's how versions balloon.

**Stage 5 — Stop.**
When the completion test passes, or the next change would only alter wording.

---

## A complete before-and-after

**Round 0 — the weak request**

> "Explain this better."

Nothing here is checkable. "Better" isn't defined, there's no reader, no length, no test. The model has to guess what you're unhappy about — so it does the only safe thing: makes it longer and adds headings. That's why "explain this better" so often returns something *bigger* rather than clearer.

**Round 1 — what the loop notices about the first response**

Graded against your own rubric:

- **Vulnerability:** the response added three claims with no sources. Can't tell which are load-bearing.
- **Ambiguity:** "better" was read as "more thorough." You meant "simpler."
- **Inefficiency:** grew from 300 to 900 words. Two paragraphs restate the intro.
- **Completion test:** none was set, so nothing can be judged. *This is the actual root failure.*

**Round 2 — the stronger revision**

> "Rewrite the explanation below for a smart friend with no medical training.
>
> **Done when:** under 250 words, no term left undefined on first use, and a nontechnical reader could restate the main idea in their own words.
>
> Don't add new claims. If something can't be simplified without becoming wrong, leave it and flag it in one line at the end.
>
> After drafting, list anything that fails the three conditions above. If nothing fails, say 'passes' and stop."

**What changed, and why each change matters:**

| Change | Why |
|---|---|
| "smart friend with no medical training" | Gives "better" a direction. Without a reader, the model defaults to longer. |
| "under 250 words" | Makes the anti-bloat instruction checkable instead of hopeful. |
| "restate in their own words" | Turns clarity into a test rather than a vibe. |
| "Don't add new claims" | Blocks scope creep — the main driver of round-over-round growth. |
| "flag it in one line" | Gives an honest exit for things that genuinely can't be simplified, instead of forcing a bad simplification. |
| "If nothing fails, say 'passes' and stop" | **The stopping rule, inside the prompt.** Without this, asking for a check guarantees findings. |

That last row is the whole lesson. The loop didn't get better because the wording got fancier. It got better because it now has a way to end.

---

## Comparison table

| Concept | Plain-English meaning | Example | Main risk |
|---|---|---|---|
| **Prompt engineering** | Writing the instruction well | "Write a 200-word handout at an 8th-grade level" | You can't predict every failure in advance |
| **Iterative prompting** *(informal term)* | Asking again after seeing the answer | "Shorter, and drop the jargon" | No stopping rule — runs until you're tired |
| **Agentic loop** *(Anthropic: "LLMs using tools… in a loop")* | The AI repeats the cycle itself | Writes code, runs tests, fixes failures, re-runs | Runs a long way in a wrong direction unattended |
| **Evaluator-optimizer** *(Anthropic's term)* | One pass writes, another grades, repeat | Draft → graded against a rubric → targeted fix | Only as good as the criteria; vague ones produce vague loops |
| **Reflection / self-critique** *(academic + practitioner term, not Anthropic's)* | Model grades its own output | "List three weaknesses in what you just wrote" | The grader shares the writer's blind spots |
| **Meta-prompting** *(informal; Anthropic ships "prompt generator" / "prompt improver")* | AI writes or fixes the prompt | Anthropic's Console prompt improver | Produces long, impressive prompts that bury your real ask |
| **Context engineering** *(Anthropic's term)* | Curating the smallest high-signal input | One `medical_context.md` all prompts reference | Stale context silently poisons every downstream answer |
| **"Loop engineering"** *(informal — not Anthropic's)* | Designing the cycle rather than the prompt | Setting outcome + check + stop rule up front | Overbuilding a system for a task that needed one good question |
| **Recursive self-improvement** *(Anthropic discusses it; says we're not there)* | AI autonomously builds its successor | Not currently possible | Confusing it with self-critique — a category error |

---

## Three rules for continuing or stopping

**Rule 1 — Continue only if you can name the defect.**
Say the specific thing that's wrong and which condition it fails. "It could be tighter" is not a defect; it's a mood. **No named defect → stop.**

**Rule 2 — Stop when the next change would only alter wording.**
Your version: *stop when the next revision won't change management.* If the reader could not do anything differently as a result of the edit, the edit is polish. Polish once, at the end, deliberately — not as a loop.

**Rule 3 — After two failed corrections on the same point, restart instead of revising.**
This is Anthropic's own rule: *"After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections."* A third attempt at the same fix is the loop failing, not working.

---

## The three most important takeaways

1. **A loop is attempt → check → decide.** Miss the check and you don't have a loop, you have repetition.
2. **What you engineer is the standard and the exit** — not the prompt. Without them, Anthropic's line applies to you literally: *"you become the verification loop."*
3. **Self-critique improves the draft, never the model.** The weights don't move while you talk. Only your folder remembers — so write down *why* a version changed, not just that it did.
