# Routine spec — Angelic Orchestrator → Asana daily sync

Status: STAGED, awaiting one interactive approval (create_trigger was approval-gated
in the autonomous turn of 2026-08-27). Retry with Dr. Rahman present, or he creates
it from claude.ai/code. Fired sessions carry the Asana connector grant; the first
run creates the Asana project if missing, so in-session Asana access is not needed.

- name: Angelic Orchestrator → Asana daily sync
- schedule: `0 12 * * *` UTC (8:00 AM EDT / 7:00 AM EST daily)
- mode: fresh session per fire
- connectors: ["Asana"]
- notifications: push on completion
- initiation: human_request (asked 2026-08-27)

## Prompt (verbatim)

You are running Dr. Rahman's daily angelic-orchestrator organization pass. If the angelic-orchestrator skill is available, invoke it first and honor its gates (privacy zones, no invented confidence numbers, answer-first output). This is a standalone recurring job; nothing from prior sessions is in your context.

1. READ THE SPINE. In the repo faraazxxx-ui/claude- (cloned in this session), the spine lives in spine/ (hub.md, goal.md, verify.md, progress.md, telemetry.md). If spine/ is absent from the default branch, run: git fetch origin claude/claude-rc-u911rf && git show origin/claude/claude-rc-u911rf:spine/hub.md (and same for goal.md, progress.md) — use whichever branch has the newest spine commit. Read hub.md's task registry, goal.md, and progress.md's latest pass.

2. RECONCILE INTO ASANA (the Asana connector is granted to this routine). Find the project named "Angelic Orchestrator — Spine" (search projects; do not create duplicates). If it does not exist, create it (privacy: private) with sections: "🎯 Goals", "📁 Projects", "♟ Strategy", "📅 This Week", "⏸ Waiting On".
   Then reconcile so Asana mirrors the spine across time:
   - Each active hub.md task → one Asana task in 📁 Projects, assignee "me", with its blocked-on items as subtasks and a due date (default: 3 days out if the spine names none).
   - Standing goals from goal.md → tasks in 🎯 Goals (no due dates; these persist).
   - Strategic plays/decisions in goal.md or progress.md → ♟ Strategy.
   - Anything the spine marks blocked/awaiting → ⏸ Waiting On.
   - Items the spine marks done → mark the matching Asana task complete.
   - Move tasks due within 7 days into 📅 This Week.
   - Never delete or edit tasks a human created; list them in your summary instead.

3. PRIVACY (Confidential zone): task NAMES and repo file pointers only. Do not paste litigation details, dollar figures, account numbers, or statement contents into Asana task descriptions.

4. DO NOT push to the repo. Asana is the only write target of this routine. Do not send emails. Do not create additional triggers.

5. FINISH with a short summary: tasks created / completed / moved, human-added tasks noticed, and anything in the spine that looks stale. If nothing changed since the spine's last telemetry line, say "No changes — spine and Asana already in sync."
