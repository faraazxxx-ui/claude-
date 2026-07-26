# Operating instructions

You are working inside Dr. Rahman's second brain. Read this whole file before doing anything.

## Who this is for

A practising physician with ADHD, a verbal thinker, running several serious efforts at once
(clinical work, federal litigation, health analytics, business projects). He thinks out loud and
fast, in speech rather than outline. He does not lack ideas or effort. What he lacks is
**continuity between sessions** — and that is the thing this repository exists to supply.

Consequences for how you work:

- **Lead with the answer.** Conclusion first, reasoning underneath. Never make him read to find it.
- **One decision at a time.** A menu of six options is a way of not helping.
- **Finish.** A half-built thing costs him more than nothing, because it becomes another
  directory he has to remember.
- **Write it down where it can be found again.** An answer that lives only in a chat window
  has a half-life of one session.

## The prime directive

> **Before creating any file, read `brain/index.md` and search `brain/` for the topic.**
> If a page exists, *update it*. If none exists, *create one*. Never open a new top-level directory.

This repository already contains a health analysis in four generations, prompt collections in six
locations, and two separate skill directories. Every one was written by a session that did not know
the previous session existed. You are that next session. Break the loop.

## Hard rules

1. **No finality words in filenames.** Never `FINAL_`, `PERFECTED_`, `MASTER_`, `_v2`, `_v3`,
   `_RED_TEAM`, `_COMPLETE`. Version control is git's job. A filename that claims to be final is a
   promise the next session will break. Use the plain noun: `health-analysis.md`, not
   `PERFECTED_HEALTH_REPORT_v4.md`.
2. **Canonical page or nothing.** One idea, one page, one address. Superseded material stays where
   it is as history; the canonical page links to it and states what it supersedes.
3. **Every new page gets an inbound link.** A page nothing points at will never be found again.
   Link it from `brain/index.md` or from a parent page in the same session you create it.
4. **State evidence separately from inference.** He is a physician — he will act on this. Mark what
   is measured, what is inferred, and what is guessed. Never let the three blur.
5. **Do not put new detail about private third parties into fresh pages.** The existing entity
   registry in `analysis-output/perfected/SECOND_BRAIN_ARCHITECTURE.md` is enough. Link to it.

## Where things live

| Path | What it is |
|---|---|
| `brain/index.md` | **Start here.** The hub. Every durable page is reachable from it. |
| `brain/concepts/` | Ideas that recur. The method itself lives here. |
| `brain/projects/` | Active efforts. Each page points at the real work, wherever it sits. |
| `brain/people/` | One page per recurring person. |
| `brain/decisions/` | Decisions with their reasoning and date. Append-only. |
| `brain/sessions/` | Session logs. What was asked, what was produced, what is next. |
| `brain/_templates/` | Copy these when creating a new page. |
| `brain/_forensics/` | Generated measurements. Do not hand-edit. |
| `tools/` | `corpus_forensics.py`, `wiki_lint.py`. Run them; don't rewrite them. |
| `ingest/` | Drop zone for chat exports and data dumps. Gitignored. |
| everything else at root | **History.** Prior sessions' output. Read it, cite it, don't duplicate it. |

## Session protocol

**Start:** read `brain/index.md`. Search `brain/` for the topic before assuming it is new.

**End:** before you finish, do all three —

1. Update or create the canonical page for whatever you worked on.
2. Append a short entry to `brain/sessions/` using `brain/_templates/session.md` — what was asked,
   what actually got made, and the single next action.
3. Run `python3 tools/wiki_lint.py brain` and fix any broken link you introduced.

If you did not write anything into `brain/`, the session did not happen.

## Definition of done

A task is done when the answer exists at a stable address, something links to it, and a future
session that has never seen this conversation could find it by reading `brain/index.md`.
Not when the answer is correct. Correct-but-unfindable is the failure mode this whole system exists
to prevent.
