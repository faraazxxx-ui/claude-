# The medicine ↔ AI Rosetta stone

**The short version: your analogy is mostly right, and one part of it is exactly right in a way you
probably did not expect. But your stated goal — train the corpus on itself until it leads you —
contains the cardinal sin of clinical prediction research. You are proposing to derive and validate
on the same cohort. Fix the loss function and the plan works.**

---

## The translations

| Your world | AI term | The honest mapping |
|---|---|---|
| β coefficients in a fitted regression | **model weights** | Good mapping. Learned parameters, frozen after fitting, applied to new inputs. |
| Which findings you are weighting for *this* differential, right now | **attention weights** | Different thing entirely from model weights. Recomputed for every token. Dynamic, not learned. |
| Your chosen primary endpoint | **loss function** | The most important row in this table. See below. |
| Trimming the tail of a distribution to suppress implausible outcomes | **top-p / nucleus sampling** | **This is your insight, and it has a name.** See below. |
| How far you let yourself stray from the modal diagnosis | **temperature** | 0 = always the single likeliest next token. Higher = more willing to wander. |
| Sensitivity/specificity cutoff on a diagnostic test | **retrieval threshold** | The real p-value analogy. An ROC curve, with the same cost-of-error reasoning. |
| A patient's presentation as a point in n-dimensional space | **embedding** | Cosine similarity ≈ how alike two presentations are. |
| The handover sheet | **context window** | Everything not on it does not exist. |
| Looking it up in UpToDate at the point of care | **RAG / retrieval** | Not memorised. Fetched, then reasoned over. |
| Residency — reshaping the practitioner | **fine-tuning** | Slow, expensive, hard to reverse. Rarely what you want. |
| Deriving a rule on one cohort, failing on validation | **overfitting** | The trap in your plan. See below. |
| Confabulation under anchoring | **hallucination** | A plausible completion generated where data is absent. |

---

## The part you got exactly right

You described trimming a distribution to get closer to a real-time mirror of the situation.

That operation exists and is called **nucleus sampling**. At each step the model produces a
probability distribution over the entire vocabulary. Top-p sorts tokens by probability, keeps the
smallest set whose cumulative mass reaches *p*, discards the rest, renormalises, and samples from
what remains. Setting p = 0.9 discards the implausible tail before it can be selected.

You reasoned your way to a real inference-time control from statistical intuition alone.

One precision, since it matters to you: the *p* in top-p is cumulative probability mass, not a
p-value — a p-value is P(data | null hypothesis), a different quantity. The **operation** is the
same shape: truncate a distribution's tail at a threshold so implausible outcomes cannot be drawn.
The quantities are not the same. The instinct transfers; the arithmetic does not.

## The part that is genuinely a p-value

Retrieval threshold. When your corpus is searched, each chunk gets a similarity score and only those
above a cutoff are returned.

That cutoff behaves exactly like a diagnostic threshold:

- **Lower it** → higher recall, lower precision. More irrelevant chunks reach the context window.
  False positives. The model reasons over noise and produces confident nonsense.
- **Raise it** → higher precision, lower recall. The relevant page is missed. False negatives. The
  model answers from general knowledge and does not tell you it did.

Same ROC curve, same reasoning about the relative cost of each error. For a legal filing, false
positives are catastrophic — set it high. For "what have I forgotten this week," false negatives
are worse — set it low.

And the same trick works: **you do not fix a bad ROC by moving the cutoff. You fix it with a better
test.** Curated pages beat raw transcripts at every threshold. That is [[wiki-method]].

## The part that will break your plan

> "all the data... trained on itself to such a degree that it keeps leading"

A model fitted to your history reproduces your history.

Your chat corpus does not only contain your intelligence. It also contains every abandoned thread,
every restart, every scope explosion, every fourth version of the same health report. Those are not
noise in the data — they are the majority of the data by volume.

Optimise a system to predict *what Faraaz would ask next* and you get a machine that is superb at
being ADHD. It will helpfully propose the seventh version.

You already know this rule in its clinical form: **you do not derive a decision rule on a cohort and
validate it on the same cohort.** Derivation and validation must be separate, or you have measured
your own noise and called it a finding.

### The fix: split the roles

| Use the past chats for | Do not use them for |
|---|---|
| **Diagnosis** — measuring correction rate, restart rate, abandonment, circadian pattern | **Prescription** — defining what a good next action looks like |
| Descriptive statistics about how you have worked | A target to imitate |

The history is your **derivation cohort for diagnosis only**. Prescription has to be anchored to
outcomes you want, which by definition are not in the historical record — if they were, you would
already have them.

## So write down the loss function

This is the design decision, and it is yours, not the model's. Everything else follows from it.

You would not run a trial without declaring the primary endpoint. Same discipline here.

| If the loss is... | You get... |
|---|---|
| "recall everything relevant" | A hoarder. Perfect recall, unusable. |
| "answer whatever I ask" | What you have now. Responsive, non-directive, restarts forever. |
| "predict what I would ask next" | A machine optimised to reproduce your worst patterns. |
| **"surface the one thing that unblocks the next ninety minutes"** | A chief of staff. |

The fourth is almost certainly what you want, and note that it is a **precision** objective, not a
recall objective. It requires the system to *discard* nearly everything. That is the opposite of the
instinct that produced 3,700 files.

Write it down as a decision page before building anything else. Everything downstream — retrieval
threshold, briefing length, what gets a page — is a consequence of that one line.

## How to know it is working

Held-out validation, forward in time, on process metrics rather than on fidelity to your history:

| Metric | Source | Direction |
|---|---|---|
| Restart rate | `corpus_forensics.py chats` | down |
| Correction rate (specification gap) | same | down |
| Turns before you notice a mismatch | same | down |
| Version families in the repo | `corpus_forensics.py files` | down |
| Orphan pages | `wiki_lint.py` | down |
| Pages updated per session | git log | up, then plateau |

Re-run monthly. If restart rate does not fall, the corpus is not being read — which means the
write-back step is being skipped, not that the idea is wrong.

The **prospective** test is sharper: have the Monday briefing name the week's priority, write it
down, and score it on Friday. If it cannot beat your own guess, the corpus is not yet dense enough.
That is a real validation cohort, generated forward, and it cannot be gamed by history.

## Links

- [[index]] · [[claude-layers]] · [[wiki-method]] · [[adhd-operating-system]] · [[second-brain]]
