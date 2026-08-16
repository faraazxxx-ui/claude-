# prompting/

The folder you described — created here, because it doesn't exist yet in Microsoft 365.

Built 2 August 2026.

---

## What's here

| File | What it answers |
|---|---|
| **[01-what-anthropic-actually-says.md](./01-what-anthropic-actually-says.md)** | Which Anthropic concepts match "AI that iterates and critiques itself" — with verbatim quotes, dates, and links. Separates Anthropic's words from practitioner interpretation from synthesis. |
| **[02-loops-plain-english.md](./02-loops-plain-english.md)** | What a loop is, what part gets engineered, why self-critique isn't the model getting smarter, where loops fail, and a before/after worked example. |
| **[03-prompt-folder-audit.md](./03-prompt-folder-audit.md)** | The audit of your actual prompt corpus. Habits, evidence, failure modes, rewritten examples, habit table. |
| **[PROMPT_REVIEW_TEMPLATE.md](./PROMPT_REVIEW_TEMPLATE.md)** | Copy this beside every new prompt. Includes the standing-preferences block. |

---

## The five answers, short

**Which Anthropic idea matches my description?**
Three, not one: the **evaluator-optimizer workflow** (one pass writes, another grades, in a loop), the **agent loop** driven by environmental feedback, and the instruction to **give the model a way to verify its work**. Your folder habit is a fourth thing — **context engineering**.

**Is "loop engineering" the correct term?**
No. It's an informal practitioner term, credited to Peter Steinberger (June 2026). Anthropic says "loops," "loop patterns," "the agentic loop," "evaluator-optimizer." Anthropic's own loops webinar never uses the phrase.

**Why isn't self-critique the AI improving itself?**
The model's weights are frozen during your conversation. Critique improves the *draft in front of it*, not the model. Close the window and it's gone. The thing Anthropic calls **recursive self-improvement** — an AI autonomously building its successor — is a different scale entirely, and Anthropic states plainly: *"We are not there yet."*

**How does saving prompt versions reveal my habits?**
It did, immediately. Your filenames form a ladder — `Optimized` → `Final` → `Perfected` → `v2` → `FINAL_Perfected_Prompt_v2` — which is what iteration looks like when there's no completion test. And your matched version pairs are dated the *same day*, meaning v1 was rewritten before it was ever used.

**What should I do instead of chasing a perfect prompt?**
Write "Done when: ___" before the prompt. Send a short first attempt. Grade it on Vulnerability / Ambiguity / Inefficiency. Fix only what failed. Stop when the next revision wouldn't change management — or restart after two failed corrections on the same point.

---

## The one-line version

**Stop when the next revision won't change management.**
