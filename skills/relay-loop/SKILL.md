---
name: relay-loop
description: >
  Multi-agent relay protocol: run long or heavy work as a chain of fresh sub-agents connected by compact
  handoff files, with a checker agent looping over every stage's output before it advances. Use whenever the
  user asks for loop prompting, sub-agent handoffs, "hand off before tokens run out", checker/verifier loops,
  agent relays, multi-agent orchestration, workflow pipelines, or when a single context window cannot safely
  hold a task (large transcripts, multi-document analysis, long research chains). Also use when designing any
  Workflow-tool script — it carries the six agent patterns (prompt chaining, routing, parallelization,
  orchestrator-workers, evaluator-optimizer, autonomous agent) as ready templates, plus the archetype-guard
  output check for Dr. Rahman's communication profile.
---

# Relay Loop — fresh agents, compact handoffs, checked at every gate

A loop needs three parts: **an attempt, a check, a decision** (fix and repeat, or stop). Two attempts with
no check between them is just doing it twice. What you design is not the prompt — it is **the standard,
the check, the repair rule, and the exit** (see `prompting/02-loops-plain-english.md` on branch
`claude/prompting-habits-audit-9q0e2h` — the plain-English foundation of this skill).

## The relay principle

Big input enters exactly **one** stage, in segments. Every later stage reads compact structured files from
disk — never a long inherited context. A fresh agent + a small handoff file beats a tired agent with a full
window, every time. The handoff file IS the token-depletion insurance: any stage can be rerun, any session
can resume, nothing depends on one context surviving.

## Protocol (per stage)

1. **Attempt** — agent does the work, writes its full output to a file, returns a compact schema-enforced
   receipt (counts, paths, highlights, warnings — never the payload itself).
2. **Check** — a separate adversarial checker agent compares output to ground truth (raw source, canon
   files, research findings). It is prompted to REJECT, not to approve. It returns
   `{pass, issues[], required_fixes[]}` with file-specific fixes.
3. **Decision** — fixer agents apply `required_fixes` (minimal targeted edits), checker reruns.
   **Max 2 repair rounds**, then escalate to the human with the checker's report. Never loop silently forever.
4. **Handoff** — update `handoff-state.json` (schema: `references/handoff-schema.md`) so the next stage —
   or a brand-new session — starts from the file, not from memory.

## Main-loop gates

Between agent stages, the orchestrating (main) loop runs **deterministic checks that need no model**:
JSON parses, counts match, timestamps monotonic, every citation present in the research file, every dollar
figure present in the model file. Script checks are ground truth; agent checks are judgment. Use both —
an agent checker that passed does not excuse the script gate.

## The six patterns

Templates with schemas and failure modes: `references/patterns.md`; runnable skeletons:
`templates/workflow-snippets.js`. In one line each:

| Pattern | Use when |
|---|---|
| Prompt chaining | Output of one step is the input of the next (draft → check → polish) |
| Routing | An intake decides which specialist handles each piece |
| Parallelization | Independent sections at once (sectioning) or independent votes on one question (voting) |
| Orchestrator-workers | One planner decomposes; workers execute; planner synthesizes |
| Evaluator-optimizer | The checker loop above — generate, evaluate, repair, bounded rounds |
| Autonomous agent | The main loop itself: owns gates, commits, escalation, and the exit |

## Archetype guard (output check for this user)

Every user-facing artifact gets one dedicated check before shipping — style, not facts:
answer first; tables and diagrams over prose; no CS/AI jargon; one word where five would do;
deadlines and warnings visually loud; the document reads standalone. The guard may compress but may
**never** change a fact, figure, timestamp, or citation. Deliver as interactive artifact or PDF by default.

## Hard rules

- A receipt is not evidence. "Checker passed" without sampled ground-truth comparisons is theater.
- Findings that cut against the goal are mandatory to record — the check that only confirms is not a check.
- Every repair is minimal and targeted; wholesale regeneration loses verified content.
- State the exit before you start: what "done" means, and what happens on second checker failure (human).
