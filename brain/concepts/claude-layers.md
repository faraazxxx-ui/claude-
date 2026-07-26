# Claude in its layers

**The short version: nine layers, and only three of them remember anything. You have been
working almost entirely in the six that forget. That is the whole reason you feel a few clicks
behind — not a knowledge gap, a persistence gap.**

---

## The stack, ranked by half-life

| # | Layer | What it actually is | Half-life |
|---|---|---|---|
| 0 | **Weights** | The trained transformer. Frozen at training time. | Permanent, impersonal |
| 1 | **Context window** | The only thing the model can see. Re-sent in full every single turn. | One conversation |
| 2 | **Prompt** | Your instructions inside that window. | One turn |
| 3 | **Project knowledge** | Files attached to a Project; chunked, retrieved, injected into L1. | One project |
| 4 | **Skills** | A folder of procedure — `SKILL.md` + scripts — loaded on demand. | **Permanent** |
| 5 | **Connectors (MCP)** | Live reach into Gmail, Drive, Calendar, GitHub, Scite, Elicit. | Live, remembers nothing |
| 6 | **Agents** | Claude Code and subagents. Filesystem, shell, parallel workers. | One session |
| 7 | **Automation** | Hooks and scheduled Routines. The system starts without you. | **Permanent** |
| 8 | **Corpus** | This wiki. The written record that every other layer reads from. | **Permanent** |

Layers 4, 7, and 8 are the only ones that compound. Everything else evaporates when the tab closes.

You have built L4 seven times over. You have **zero of L7 and, until now, zero of L8.**

---

## Layer 0 — Weights

A fixed function. Not a database, not a mind, not something that learns from talking to you.

**You already understand this one.** You stopped at transformers, and transformers are genuinely
where the model ends. Everything from Layer 1 up is plumbing — clever, but plumbing.

The one correction worth making: nothing you type changes the weights. When you say you want your
data "trained on itself," this is the layer you are imagining, and it is the one layer you cannot
touch. The good news is that you do not need to. Layers 3 and 8 give you everything you actually
want from personalisation, at a fraction of the cost, revisable in seconds rather than weeks.

## Layer 1 — The context window

The model is **stateless**. It has no memory of your last message. Every turn, the entire
conversation is re-sent, and the model reads it fresh, as if for the first time.

The clinical analogy: it is a locum who has never met the patient, cannot remember yesterday, and
gets exactly one handover sheet. Nothing else. The chart does not exist unless it is on the sheet.

Almost every "AI is dumb today" moment is a Layer 1 problem — something needed was not on the sheet.

**Consequence:** context is a budget, not a container. Everything above is a strategy for
deciding what earns space on the handover.

## Layer 2 — The prompt

This is the layer you understood in 2022, and your instinct was correct. Natural language really
does specify constraints the way code does — role, inputs, invariants, stopping condition, output
shape. You were writing function signatures in English.

Where it goes wrong is that a prompt is **rewritten from scratch every time**. A good prompt used
once is a good idea thrown away. That is exactly what Layer 4 fixes.

## Layer 3 — Project knowledge

Attach files to a Project. They are chunked, embedded, and the relevant pieces are retrieved into
Layer 1 when you ask something related. This is retrieval-augmented generation, and it is the
honest answer to "make it know my data."

Retrieval is **lossy and thresholded**. It returns the top-k most similar chunks, not the truth.
Feed it 3,700 raw files and you get plausible fragments from three unrelated documents stitched
into confident nonsense. Feed it 60 curated wiki pages and it is close to reliable.

This is the single strongest argument for Layer 8. See [[wiki-method]].

## Layer 4 — Skills

A folder containing `SKILL.md` — a description plus a procedure — and optionally scripts and
reference files. Only the short description sits in context permanently. When your request matches,
the full body loads. That is progressive disclosure: unlimited procedure, near-zero standing cost.

**A skill is a prompt you only have to get right once.**

You already have seven: `life-intelligence-engine`, `legal-endeavors`, `daily-workflow-optimizer`,
`health-data-analyst`, `verbal-prompt-optimizer`, `apex-legal-strategy`, `subscription-bleed-killer`.
That is genuinely advanced. Most people never write one.

The problem is not the skills. It is that they live in two competing directories (`skill/` and
`skills/`), duplicate each other's reference files byte-for-byte, and none of them read from a
shared corpus. Seven excellent instruments, no score.

## Layer 5 — Connectors (MCP)

Tools that reach live systems: Gmail, Drive, Calendar, GitHub, Asana, Scite, Elicit, CourtListener.
Read and, where you allow it, write.

Two things to hold onto. **Connectors have no memory** — pulling an email into context does not
file it anywhere; when the session ends it is gone unless something wrote it down. And **a connector
is reach, not judgement**: it can fetch a thousand messages, and choosing which fifty matter is
still Layer 2 and Layer 8 work.

## Layer 6 — Agents

Claude Code is the model with hands: filesystem, shell, ability to run the code it writes and read
the error. Subagents fan out with isolated context windows and report back.

The difference from chat is that an agent can **verify**. It writes the script, runs it, sees the
traceback, fixes it. Chat can only assert.

This is where a computer full of data actually gets processed, because the data never has to fit in
a context window — the agent greps it, samples it, and summarises it in passes.

**But an agent with no Layer 8 is an amnesiac with hands.** That is precisely how this repository
grew four generations of the same health report.

## Layer 7 — Automation

Hooks fire on events. Scheduled Routines fire on a clock. Both mean **the system starts without you
deciding to start it**.

For ADHD this is not a convenience feature. It is the whole point.

Every layer above requires you to initiate: open the tab, remember the project exists, recall what
you were doing. That initiation step is exactly the one executive function taxes hardest. Layer 7
removes it. A Monday-morning routine that reads the corpus and produces three sentences —
*here is what you left unfinished, here is what is now urgent, here is the one thing to do today* —
does more for output than any prompt improvement available at any other layer.

**You have none of this. It is the highest-leverage gap in your entire stack.**

## Layer 8 — The corpus

The wiki. The only layer that compounds.

Every other layer reads from it and writes back to it. Retrieval (L3) gets clean pages instead of
raw chat fragments. Skills (L4) get shared references instead of duplicated ones. Agents (L6) find
the previous answer instead of regenerating it. Automation (L7) has something to be proactive
*about*.

Without Layer 8, every session starts at zero, and starting at zero always produces a new folder.
That is the loop. This repository is the evidence, and `brain/_forensics/` has the measurements.

See [[wiki-method]] for why this is a wiki and not a folder of documents.

---

## Where you actually are

| Layer | Your position |
|---|---|
| 0–2 | Strong. Your 2022 insight was right and you have been compounding it. |
| 3 | Sporadic. Used, but over raw dumps rather than curated pages. |
| 4 | **Advanced.** Seven skills. Two directories. No shared spine. |
| 5 | Broad reach, no capture. Things come in; nothing gets filed. |
| 6 | Active, but amnesiac — each session opens a new folder. |
| 7 | **Absent.** Highest leverage available to you. |
| 8 | **Absent until now.** The reason 4, 5, and 6 keep restarting. |

## The next three clicks, in order

1. **This commit.** `CLAUDE.md` plus `brain/` gives you Layer 8. Every future Claude Code session
   reads it automatically, before you type anything.
2. **Merge your skills into one directory** and point their references at `brain/` instead of at
   private copies. Turns seven instruments into one system. See [[second-brain]].
3. **Add one Routine.** Monday 07:00: read the corpus, produce the three sentences. That is
   Layer 7, and it is roughly fifteen minutes of setup.

Do them in that order. Two and three are worth little without one.

## Links

- [[index]] · [[wiki-method]] · [[ai-medicine-rosetta]] · [[adhd-operating-system]] · [[second-brain]]
