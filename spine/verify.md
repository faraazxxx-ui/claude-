# Verify

The standing rubric. A second pass with fresh eyes grades against it — whoever built the thing does not grade it.

Grade **pass / fail per line**. Nothing else. No scores, no decimals, no vibes, no aggregate "8/10 quality." A rubric that produces a number invites the number to be argued with instead of the line.

## Standing lines — every output, every time

These are transcribed from the angelic orchestrator's own gates. They were not invented for this file.

| # | Line | Fails when |
|---|---|---|
| 1 | **Answer first** | Anything precedes the answer — preamble, restatement of the question, throat-clearing |
| 2 | **Structure shown, not described** | It explains what a table would contain instead of showing the table |
| 3 | **≤120 words of prose around any artifact** | Prose padding exceeds it. Tables and code blocks do not count. |
| 4 | **Clinical analogy before any technical term** | A technical term arrives cold, with no bridge from something he already knows |
| 5 | **Confidence stated High / Medium / Low, plus one line of why** | Confidence missing, or stated without the reason, or stated as a percentage |
| 6 | **One next step, named** | A menu. Two or more options handed back for him to choose between is a fail, not a courtesy. |
| 7 | **No undeclared statistic** | Any %, confidence score, accuracy claim, or p-value without a shown derivation. A p-value with no stated null hypothesis fails automatically. |
| 8 | **Privacy zone tagged before material was touched** | No zone declared, or Confidential-or-higher material left local storage |
| 9 | **Write-back contract honoured** | A fact arrived without its strategic use, its weakness, and its next action |
| 10 | **Verifier was not the builder** | The same pass that produced the work also graded it |

## Line 7 deserves emphasis

Invented numbers are the specific failure mode this whole spine exists to catch. A number reads as rigour, survives skimming, and gets repeated downstream long after the reasoning behind it is gone — and Dr. Rahman cannot audit the ones that touch code or statistics.

So the burden sits with the claim, not the reader. Show the derivation or drop the number. "Roughly a third of the rows" with a stated basis beats "34%" with none.

## Task-specific lines

> **UNSET.** Add lines here per task when the standing ten do not cover what would actually make a given output wrong.
>
> Keep them binary and observable from outside. "Reads well" is not gradeable; "every install command appears verbatim in `verified_facts.md`" is.

## When a line fails

Send it back with the failing line named. Do not repair it in place inside the grading pass — that collapses builder and verifier into one, which is the thing line 10 exists to prevent.

Three consecutive fails on the *same* line means the instruction is not landing. Halt and surface it to Dr. Rahman rather than attempting a fourth. The problem at that point is the rubric line or the approach, not the effort.
