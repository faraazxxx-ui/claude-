# Agent operating rules for mobile-launched runs

You are running in a cloud VM. The user is on a phone. They cannot open a
terminal, edit files, or “just check the repo locally.”

## Start of run

1. Call `run-info` if Cursor Cloud MCP is available. Note `source`, `url`,
   `repoUrl`, and `branchName`.
2. If `source` is `mobile` / the run is from iOS, keep this skill in force
   for the whole session (treat it as a Custom Mode).
3. Check `get-message-queue`. If follow-ups are already queued, finish the
   cumulative request before long verification.

## Git and PRs

- Create a feature branch. If the user named the branch, honor that name
  inside the environment’s required prefix (for this cloud setup:
  `cursor/<descriptive-name>-32b1`).
- Commit with a message that makes sense in a phone PR list.
- Push and open a draft PR early, then update it. The user watches the PR
  from the iOS review UI.
- Put the PR URL in every user-visible wrap-up.

## Communication

Lead with the answer. Then:

- What changed (files / skill name)
- How to review on the phone (open the PR, look at these files)
- Links: PR, this agent, any imported agent

Do not ask the user to run local commands unless there is no alternative.
If a secret or dashboard click is required, say exactly which screen
(Cursor Dashboard → Cloud Agents, etc.).

## Verification

- Markdown / skills: validate frontmatter (`name` matches folder, YAML
  parses) and that Cursor will discover the path (`.cursor/skills/`,
  `.agents/skills/`, or `.claude/skills/`).
- App/UI changes: exercise the flow; attach screenshots or a recording.
- Do not claim browser testing that did not happen.

## Skills on cloud/mobile

These locations load on Cloud Agents:

| Path | Who loads it |
| --- | --- |
| `.cursor/skills/<name>/SKILL.md` | Cursor (cloud, web, iOS, desktop) |
| `.agents/skills/<name>/SKILL.md` | Cursor |
| `.claude/skills/<name>/SKILL.md` | Cursor (compat) **and** Claude Code |
| `~/.cursor/skills/` | Local machine only — **not** cloud/iOS |

`name` in frontmatter must match the folder. Keep `SKILL.md` short; put
depth in `references/` and `scripts/`.

This repo also has legacy `skill/` and `skills/` trees that Claude Code
does not scan. New work belongs in `.cursor/skills/` (and `.claude/skills/`
when Claude Code should load the same playbook).

## MCP and other agents

- Use Cursor Cloud MCP to inspect this run and, when the user pastes a
  `bcId`, to fetch that run’s transcript/diff.
- Non-admins only see their own runs. A “not available” result is a
  permissions/environment miss, not a reason to stop the named task.
- Personal MCP servers are chosen per-run on mobile; they are defined on
  the web.

## Subscriptions

If the user wants “keep it green” or “tell me when CI finishes,” subscribe
(GitHub PR/CI, timer) instead of polling. Wake on the event.
