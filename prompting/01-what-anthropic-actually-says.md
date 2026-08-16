# What Anthropic Is Actually Pointing Toward

*Prepared 2 August 2026. Every Anthropic claim below is tied to a named, dated, public Anthropic page. Where a claim is mine or a practitioner's, it is labelled.*

---

## The idea in one sentence

Anthropic is pointing at **a work cycle with a check in it** — the model does something, something else grades it against a stated standard, and the cycle repeats until the standard is met — and the part you design is **the check and the stopping condition**, not a perfect opening instruction.

---

## What Anthropic was actually pointing toward

Your description ("AI that iterates, critiques, revises, or prompts itself") maps onto **four separate Anthropic ideas**, not one. Mixing them is the reason the vocabulary feels slippery.

### 1. The evaluator-optimizer workflow — the closest match

From *Building Effective Agents* (19 Dec 2024, Erik S. and Barry Zhang):

> "In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop."

Anthropic says to use it when:

> "we have clear evaluation criteria, and when iterative refinement provides measurable value."

**Note the detail most people skip:** it is *two roles*, not one model grading itself. A maker and a marker. The value comes from the marker having criteria the maker didn't write.

### 2. The agent loop — how Anthropic defines agents at all

Same post:

> "They are typically just LLMs using tools based on environmental feedback in a loop."

And:

> "During execution, it's crucial for the agents to gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress."

**"Ground truth" is the load-bearing phrase.** A loop that only consults its own opinion has no ground truth. A loop that runs a test, reads an error, or compares against a fixture does.

### 3. "Give Claude a way to verify its work" — the operational instruction

From Anthropic's *Best practices for Claude Code* (undated living documentation, retrieved 2 Aug 2026):

> "Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal available, and you become the verification loop: every mistake waits for you to notice it. Give Claude something that produces a pass or fail, and the loop closes on its own."

That sentence — *you become the verification loop* — is the precise diagnosis of the habit you described.

The same page gives a hard correction rule:

> "If you've corrected Claude more than twice on the same issue in one session, the context is cluttered with failed approaches. Run `/clear` and start fresh with a more specific prompt that incorporates what you learned. A clean session with a better prompt almost always outperforms a long session with accumulated corrections."

And it names the trap that makes loops run forever:

> "A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do. Chasing every finding leads to over-engineering."

### 4. Context engineering — what your folder habit actually is

From *Effective context engineering for AI agents* (29 Sept 2025; Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield):

> "Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

> "At Anthropic, we view context engineering as the natural progression of prompt engineering."

> "Good context engineering means finding the *smallest possible* set of high-signal tokens that maximize the likelihood of some desired outcome."

And on how to start:

> "It's best to start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples to improve performance based on failure modes found during initial testing."

That last quote is Anthropic explicitly endorsing **start small, then patch observed failures** over **write one perfect prompt**.

### On "meta-prompting"

Anthropic does ship AI-that-writes-prompts, as product, not theory: the Console **prompt generator** ("Automatically generate first draft prompt templates") and the **prompt improver**, which Anthropic describes as helping you "quickly iterate and improve your prompts through automated analysis and enhancement." Anthropic's own documentation URL for the generator helper contains the string `helper-metaprompt-experimental` — *my observation, not an Anthropic definition.* Anthropic's user-facing pages call these tools "prompt generator" and "prompt improver," not "meta-prompting."

---

## Is "loop engineering" the right term? No.

**Verdict: informal practitioner term. Not Anthropic terminology.**

What I actually verified:

- Anthropic's public webinar page **"Startup Builds: Getting Started with Loops"** (24 July 2026, Mark Nowicki, Applied AI @ Anthropic) uses **"loops"** and **"the four loop patterns in Claude Code."** The phrase *"loop engineering" does not appear on that page.* The page also does not publicly name what the four patterns are.
- Practitioner write-ups attribute the coinage to developer **Peter Steinberger (June 2026)**, amplified by **Addy Osmani**.
- **A caution, and a live example of why you asked for source discipline:** at least one secondary summary claims Anthropic "published an official blog post titled 'Getting started with loops' which categorized loops into four types (turn-based, goal-based, time-based, proactive)." I checked the Anthropic page. It is a **webinar listing, not a blog post**, and it does **not** name those four types publicly. I could not verify those four labels as Anthropic's. Do not repeat them as Anthropic's.
- A widely circulated quote — *"You're not supposed to prompt Claude. You're supposed to build a system that prompts itself"* — is attributed to Boris Cherny (who leads Claude Code at Anthropic) in practitioner articles **with no linked source, date, or venue.** Treat it as unverified.

**Anthropic's own words for this territory are:** "loops," "loop patterns," "the agentic loop," "evaluator-optimizer," "context engineering," and "give Claude a way to verify its work."

---

## How it differs from trying to write a perfect prompt

Writing a perfect prompt is trying to **predict every failure in advance**. A loop is **letting the failures show up and catching them with a check**.

The difference is where the intelligence lives:

| | Perfect-prompt approach | Loop approach |
|---|---|---|
| Where effort goes | Into the wording, before you see any output | Into the standard the output must pass |
| How you know it worked | It feels thorough | It passed a test you wrote first |
| What happens when it fails | Rewrite the whole thing | Patch the one part that failed |
| When you stop | When you're tired of it | When the test passes |

Anthropic's advice points at the second column: *"Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short"* (*Building Effective Agents*, 19 Dec 2024).

---

## How your "prompting" folder method relates to it

Your instinct is right and it has an Anthropic-supported name: **context engineering**. Saving versions is curating "the optimal set of tokens" across time instead of within one message.

But there is a gap, and it's the whole ballgame:

- **Anthropic's loop stores the *check*.** A test file, a `/goal` condition, a screenshot to diff against.
- **Your folder stores the *outputs*.** Version after version of the prompt itself.

Storing outputs tells you *what you wrote*. Storing checks tells you *what "good" meant*. Without the second, a folder of versions can't tell you whether v2 beat v1 — only that v2 came later.

*(My synthesis, not Anthropic's claim.)*

---

## What you are already doing correctly

1. **You refuse the one-shot.** Anthropic agrees: "Though Claude occasionally solves problems perfectly on the first attempt, correcting it quickly generally produces better solutions faster."
2. **You externalise shared context.** Your health prompts reference a single `medical_context.md`, which you justified in your own words: *"This makes the prompts shorter and ensures consistency."* That is the "smallest possible set of high-signal tokens" principle, arrived at independently.
3. **You built an evaluator before anyone told you to.** `prompts/red_team_analysis.md` grades every prompt under three fixed headings: **Vulnerability / Ambiguity / Inefficiency.** That's a rubric. Most people never write one.
4. **You keep versions.** Almost nobody does, and it's the only reason this audit was possible.

## Where your method can become repetitive, unstable, or misleading

1. **No completion test, so the loop exits on fatigue.** The filenames record this: `Optimized` → `Final` → `Perfected` → `v2` → `FINAL_Perfected_Prompt_v2` → `Red_Team_Edition`. Escalating superlatives are a stopping rule made of feelings.
2. **Revision without field evidence.** `FINAL_OPTIMIZED_PROMPTS.md` and `PERFECTED_PROMPTS.md` are both dated 15 March 2026. The Ghusoon v1.0 and v2.0 files are both dated 5 April 2026. v1 was rewritten before it was ever used, so "v2 is better" is an opinion, not a result.
3. **Taste oscillation dressed as improvement.** Ghusoon v1 justified numbered requirements as *"numbered for parallel execution."* v2 removed the numbering *"to prevent procedural scripting."* Same feature, opposite rationale, same day. At least one of those was not an improvement.
4. **Growth mistaken for rigor.** The Dubai prompt went from 134 to 283 lines between versions. Anthropic warns the other way: *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"*
5. **False precision.** A file in your Microsoft 365 store reads `Confidence: 98.7`. A number to one decimal place, with no method behind it, is a confidence claim you can't defend.
6. **Asking for critique guarantees critique.** Per Anthropic's own caution, a reviewer told to find gaps will find them whether or not they matter. That is the engine of endless revision.

---

## A simple improved workflow

1. **Write the completion test first, in one sentence, before the prompt.** "Done = a nontechnical reader can restate the idea in their own words."
2. **Send a short first attempt.** Not your best — your shortest honest one.
3. **Grade it against your own three headings** (Vulnerability / Ambiguity / Inefficiency) plus "does it pass the completion test?"
4. **Fix only what failed.** Name the defect before you touch anything.
5. **Stop when the next change would only alter wording** — or after two failed corrections on the same point, at which point start over with a fresh prompt containing what you learned.

---

## One concrete before-and-after, from your actual habits

**Before** — your real recurring opener, preserved in two of your file names:

> "Voice / Whisper — With my verbal input, below, I need you to formulate the prompt, but 1st rigorously curate the most advanced strategies for…"

What's wrong with it: no outcome, no audience, no completion test. "Most advanced" is unbounded, so the model pads. And it makes a research phase mandatory for every single task, which is why your documents keep opening with survey material you didn't need.

**After** — same voice, same intent, with a test attached:

> "Here's my verbal input below. Turn it into a working prompt for [platform].
>
> **Outcome:** [one sentence — what the finished thing must let me do].
> **Audience:** [who reads it].
> **Done when:** [the test — e.g. "it names the three deliverables and every claim has a source"].
>
> Draft it short first. Then grade your own draft on Vulnerability / Ambiguity / Inefficiency and fix only what fails. Don't research best practices unless a specific gap requires it — if it does, say which gap."

The changes: the outcome is stated, the test is stated, research became conditional instead of mandatory, and "fix only what fails" blocks the full rewrite.

---

## The three most important takeaways

1. **"Loop engineering" is not Anthropic's term.** The Anthropic-supported ideas are the **evaluator-optimizer workflow**, the **agent loop driven by environmental feedback**, and the instruction to **give the model a way to verify its work**.
2. **What gets engineered is the check and the stopping condition** — not the prompt. Without a check, Anthropic's words apply exactly: *"you become the verification loop."*
3. **Nothing about the model improves while you iterate.** Only your folder learns — and only if you record *why* a version changed, not just that it did.

---

## Concept table

| Concept | Plain-English meaning | Evidence from Anthropic | Connection to my habits | Practical implication |
|---|---|---|---|---|
| **Evaluator-optimizer** | One pass writes, another pass grades, repeat | "one LLM call generates a response while another provides evaluation and feedback in a loop" — [*Building Effective Agents*](https://www.anthropic.com/engineering/building-effective-agents), 19 Dec 2024 | You already do this by hand — you *are* the evaluator | Write the criteria down once; stop re-deciding what "better" means each round |
| **Agent loop / ground truth** | Model acts, reads a real result, adjusts | "LLMs using tools based on environmental feedback in a loop"; agents must "gain 'ground truth' from the environment" — same post | Your loops mostly consult opinion, not results | Add one real check per loop: a source, a file, a test |
| **Verify its work** | Give it a pass/fail it can run itself | "Without a check it can run, 'looks done' is the only signal available, and you become the verification loop" — [Claude Code best practices](https://code.claude.com/docs/en/best-practices) (retrieved 2 Aug 2026) | This is exactly why you keep saying "redo it" | State "Done when…" before the first draft |
| **Two-correction rule** | After two failed fixes, restart clean | "After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned" — same page | Your loops run well past two | Restart instead of revising a third time |
| **Context engineering** | Curating the smallest high-signal input | "the natural progression of prompt engineering"; "smallest *possible* set of high-signal tokens" — [*Effective context engineering*](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), 29 Sept 2025 | Your `medical_context.md` move, exactly | Promote repeated instructions into one standing file; keep prompts short |
| **Prompt generator / improver** | Anthropic's own AI-writes-prompts tools | ["Automatically generate first draft prompt templates"](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator); [prompt improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver) | Your "formulate the prompt for me" opener | Legitimate move — just bound it with an outcome and a test |
| **Recursive self-improvement** | An AI autonomously building its successor | "We are not there yet, and recursive self-improvement is not inevitable" — [*When AI builds itself*](https://www.anthropic.com/institute/recursive-self-improvement), May 2026 | What your loop is **not** | Don't expect the model to get smarter mid-session; only your notes persist |
| **"Loop engineering"** *(disputed / informal)* | Designing the repeating work cycle | **No Anthropic source uses this phrase.** Anthropic's [loops webinar](https://www.anthropic.com/webinars/startup-builds-getting-started-with-loops) (24 July 2026) says "loops" and "loop patterns" | The term you brought in | Safe to use casually; don't cite it as Anthropic's |

---

## Sources

**Anthropic (official):**
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — 19 Dec 2024, Erik S. & Barry Zhang
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 29 Sept 2025, Rajasekaran, Dixon, Ryan, Hadfield et al.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — 26 Nov 2025, Justin Young
- [When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement) — May 2026, Marina Favaro & Jack Clark
- [Startup Builds: Getting Started with Loops](https://www.anthropic.com/webinars/startup-builds-getting-started-with-loops) — webinar, 24 July 2026, Mark Nowicki
- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) — undated living doc, retrieved 2 Aug 2026
- [Prompt generator](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-generator) · [Prompt improver](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver) · [Prompt generator announcement](https://www.anthropic.com/news/prompt-generator)

**Practitioner (not Anthropic — interpretation only):**
- [Prompt Engineering vs Loop Engineering vs Graph Engineering](https://www.marktechpost.com/2026/07/29/prompt-engineering-vs-loop-engineering-vs-graph-engineering/) — MarkTechPost, 29 July 2026
- [What Is Loop Engineering?](https://explainx.ai/blog/what-is-loop-engineering-ai-agents-2026) and [Anthropic Engineer: Build Loops That Prompt AI](https://explainx.ai/blog/anthropic-engineer-loops-prompts-ai-coding-harness-engineering-2026) — explainx.ai, 2026. *Contains unsourced quotes attributed to Anthropic staff.*
- [Loop Engineering: The Anthropic Playbook](https://www.aibuilderclub.com/blog/loop-engineering-anthropic-playbook) — AI Builder Club
