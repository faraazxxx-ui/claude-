# Designing the system around ADHD

**The short version: the binding constraint is not attention and not effort. It is initiation and
retrieval-of-intention — remembering, at the moment it matters, that a thing exists and is yours to
resume. Every design choice here removes a remembering step rather than asking for more discipline.**

---

## What the system must not require

Any design that depends on you remembering to check it has already failed. That includes most
productivity systems, and it includes a second brain you have to decide to open.

Three failure modes, all visible in this repository's history:

| Failure | What it looks like here |
|---|---|
| **Initiation cost** | Opening the old thread is harder than starting a new one, so a new one gets started. Four generations of the health analysis. |
| **Lost intention** | The work exists but you cannot recall where, so it is rebuilt. `SECOND_BRAIN_ARCHITECTURE.md`, written well, never read again. |
| **Scope expansion** | One task becomes five mid-session, none finish. Six prompt directories. |

Each has a structural fix. None of them is "try harder."

## The five rules

### 1. One address, always the same

`brain/index.md`. Not a folder you navigate, not a search you have to phrase. One filename you
never have to recall because it is the same every time and `CLAUDE.md` makes every session open it
before doing anything.

You are allowed to forget everything else. That is the point.

### 2. The system starts, not you

Layer 7 in [[claude-layers]]. A scheduled Routine that runs whether or not you thought about it,
reads the corpus, and puts three sentences in front of you.

This converts the hardest executive step — initiation — into a passive one. You are not deciding to
engage; something is already on the screen and you are reacting to it. Reacting is cheap for you.
Initiating is expensive. Design accordingly.

### 3. One next action, never a menu

A list of options is a decision, and decisions are the expensive currency. Any output that ends
with six possibilities has converted work into homework.

The corpus should end every interaction with exactly one named next action. If ranking is needed,
rank silently and present the winner.

This is also an instruction to Claude, and it is in `CLAUDE.md`.

### 4. Closing the loop is a ritual, not a judgement call

The write-back step — updating the page at session end — cannot depend on you noticing it is time.
It is in `CLAUDE.md` as a hard requirement of the session protocol, so the agent does it
unprompted, every time.

This is the single mechanism that turns Layer 8 from a folder into a learning system, and it is
precisely the step that a distractible operator will skip. So it is not the operator's job.

### 5. Work with your circadian pattern, not against it

`corpus_forensics.py chats` produces an hour-by-hour histogram of when you actually engage. Almost
everyone with ADHD has a sharply peaked curve and schedules against it out of guilt.

Once you can see the peak: protect those hours for the work that needs your judgement, and route
everything mechanical to the trough. The corpus can do trough-hours work without you.

## The scope-expansion valve

Scope expansion is not a flaw to suppress. Mid-task, "also, what about..." is frequently your best
thinking — it is associative reach, and it is the same faculty that makes you good at differentials.

The problem is only that it destroys the current task.

So capture it without following it. When a tangent appears, it becomes a stub in `brain/` with one
line and a link back — three seconds — and the current task continues. The idea is preserved at an
address; the thread survives.

Suppressing the tangent loses the idea. Following it loses the task. Filing it costs three seconds
and loses neither.

## The honest limits

Worth stating plainly, because a system that oversells itself gets abandoned on first
disappointment:

- **This does not fix executive function.** It relocates specific steps out of your head. The
  underlying difficulty is unchanged.
- **It degrades if the write-back stops.** Skip it for a month and you have a stale corpus, which is
  worse than none because it is confidently wrong.
- **It cannot want things for you.** Direction is yours. The corpus can only hold a direction you
  have already stated — which is why the loss function in [[ai-medicine-rosetta]] has to be written
  down by you, once, explicitly.
- **Building it is itself a project you could abandon.** This is the real risk. Which is why the
  first version is three files and a commit, not a platform.

## The smallest version that works

If everything else here is too much, this is the irreducible core:

1. `CLAUDE.md` exists and says *read `brain/index.md` first, write back before finishing*.
2. `brain/index.md` exists and links to everything durable.
3. One scheduled Routine puts three sentences in front of you each Monday.

Items 1 and 2 are done as of this commit. Item 3 is fifteen minutes and is the highest-leverage
thing left. See [[second-brain]].

## Links

- [[index]] · [[claude-layers]] · [[wiki-method]] · [[ai-medicine-rosetta]] · [[anti-versioning]] · [[second-brain]]
