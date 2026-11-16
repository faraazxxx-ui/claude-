# Hub

Gate 0 of the angelic orchestrator reads this file, `goal.md`, and `verify.md` before anything is dispatched. All three are fixed for the duration of a task. Work writes *down* into them; nothing edits them from above mid-task.

If a task does not fit the live `goal.md`, stop and say so before spending a single sub-agent call.

## The spine

| File | Holds | Written by |
|---|---|---|
| `hub.md` | This index and the fixed rules | Dr. Rahman only |
| `goal.md` | What the current push is for | Dr. Rahman only |
| `verify.md` | The standing pass/fail rubric | Dr. Rahman only |
| `progress.md` | Current state as of the last pass | Every session |
| `telemetry.md` | One line per session, minimum one per day | Every session |
| `failure.md` | What went wrong and what it cost | Whenever something fails |
| `learnings.md` | What is now known that was not before | Whenever something is learned |

The top three are read-only during a task. The bottom four are append-only — never rewrite history in them, because the value is in the pattern across entries, not in any single line.

## Fixed rules

**Mode.** Is there a lead that has confirmed more than once? Yes → fast-twitch: take the non-contiguous jump, and if the next checkpoint also confirms, allocate *more* to that lead, never less. No, or standing work → slow-loop: gather, reason, verify, write back, repeat. The slow loop never reports itself done, only current as of this pass.

**Privacy zone.** Tag before any material is touched: Public / Private work / Confidential / Privileged / Restricted. Apex litigation, medical and journal material, and anything under a `*_PRIVILEGED` folder default to Confidential-or-higher and stay local — no public RAG, no shared index — until Dr. Rahman personally downgrades the tag.

**Write-back contract.** No sub-agent returns raw material. Every fact arrives with its strategic use, its weakness, and its next action. Missing any of the three, it goes back — it does not reach the hub.

**Separate verifier.** Whoever built it does not grade it. Pass/fail per rubric line only. Any statistics-shaped number — a percentage, a confidence score, an accuracy claim — shows its derivation or fails that line by default.

**Stop budget.** 2 rounds per task. 3 consecutive same-line verifier fails → halt and surface. 10 actions with no forward progress → halt. Compact at ~70% context.

## Standing skills

| Skill | Covers |
|---|---|
| `skills/voice-capture-setup` | Getting speech into text — dictation stack, Sony pipeline |
| `verbal-thinker-stack-audit/voice-first-verbal-thinker-skill` | Turning that text into structure and routing it |
| `skills/apex-legal-strategy` | Litigation. Confidential-or-higher by default. |
| `skills/life-intelligence-engine` | Standing background work |
