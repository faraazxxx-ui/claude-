# The six agent patterns as Workflow templates

Source concepts: Anthropic, *Building Effective Agents* (Dec 2024) and the agentic-loop docs. Each entry:
when to use, shape, schema hint, failure mode. Runnable skeletons in `../templates/workflow-snippets.js`.

## 1. Prompt chaining
**Use:** each step's output feeds the next; quality gates between steps.
**Shape:** `agent(draft) → gate → agent(refine) → gate → agent(finalize)`
**Failure mode:** silent drift — later steps "improving" verified content. Fix: each step's prompt forbids
changing upstream-verified facts; gates diff against canon.

## 2. Routing
**Use:** heterogeneous inputs, specialist handling (e.g. transcript blocks tagged discovery vs damages).
**Shape:** classifier agent (or deterministic tag) → dispatch table → specialist agents.
**Failure mode:** router invents categories. Fix: closed enum in the routing schema; "other" bucket routes to human.

## 3. Parallelization
**Sectioning:** independent chunks at once (segments of a transcript; one agent per defendant).
Cut at natural boundaries with small overlap; a merge stage dedupes the seams.
**Voting:** same question, independent angles (verify a citation via two databases; N skeptics try to refute).
**Failure mode (sectioning):** seam loss — facts straddling a boundary vanish. Overlap + merge-dedupe fixes it.
**Failure mode (voting):** identical prompts = correlated votes. Give each voter a distinct lens.

## 4. Orchestrator-workers
**Use:** the decomposition itself needs judgment (research questions, fix assignment).
**Shape:** orchestrator emits a typed work-list → `parallel(workers)` → orchestrator (or a synthesizer) merges.
**Failure mode:** orchestrator scope-creeps the work-list. Fix: cap list size in schema; require rationale per item.

## 5. Evaluator-optimizer
**Use:** quality is checkable but not one-shot achievable — the core relay-loop cycle.
**Shape:** `generate → adversarial check {pass, issues, required_fixes} → targeted fixers → recheck`, max 2 rounds, then human.
**Failure modes:** (a) grade-inflation — evaluator prompted to "review" instead of "reject unless"; (b) fixer
regenerates wholesale and loses verified content; (c) unbounded loop. Fixes: reject-framing, minimal-edit rule, hard round cap.

## 6. Autonomous agent (the main loop)
**Use:** the whole mission — owns sequencing, deterministic gates, commits, escalation, the exit.
**Shape:** gates between workflows; script-level checks (parse, count, cite-match) that no model can charm past.
**Failure mode:** "looks done" = done. Fix: the exit condition is written before starting; evidence, not assertion.

## Composition used in practice (the war-room build)
chaining across workflows → sectioning inside forensics → routing by legal tag → orchestrator-workers for
research/strategy → evaluator-optimizer at every stage → autonomous main loop with scripted gates.
One big input entered once; everything else read compact canon files.
