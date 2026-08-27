---
name: cursor-mobile
description: >
  Operate Cursor Cloud Agents launched from Cursor for iOS / mobile. Use when
  run source is mobile or iosApp, the user is on a phone or iPad, pastes a
  cursor.com/agents URL, dictates a voice prompt, attaches camera photos, or
  asks to land work on a branch they can review and merge from the phone.
  Also use for Cursor iOS setup, Remote Control, Live Activities, Design Mode,
  and placing repo skills so they load on cloud/mobile workers.
icon: rocket
color: cyan
---

# Cursor Mobile

This skill is the operating playbook for agents started from the Cursor iOS
app (and the mobile web inbox at cursor.com/agents). The user reviews on a
phone, not in a desktop IDE.

Read on demand:

- `references/ios-playbook.md` — app capabilities, limits, Remote Control
- `references/agent-operating.md` — how to run a mobile-launched cloud agent
- `references/prompt-patterns.md` — voice / verbal-thinker / “add this” prompts
- `references/source-agent.md` — originating agent this skill was requested from

## Detect this skill

Apply it when any of these are true:

- `run-info` reports `source` as `mobile` (or the run is tagged `iosApp`)
- The prompt came from a phone: short, dictated, photo-first, or a pasted
  `https://cursor.com/agents/bc-…` link
- The user asks for a named branch so they can review from the Cursor app
- The user mentions Cursor iOS, iPad, mobile agents, Remote Control, or
  Live Activities

## Defaults (do these without being asked)

1. **Execute.** Infer intent from messy voice or short text. Ask at most one
   blocking question. Do not stall for a perfect spec.
2. **Land a reviewable branch + PR.** Mobile has no editor or terminal. The
   PR is the product. Open it as draft until verification is done.
3. **Phone-scannable writing.** Lead with the outcome, then a few bullets,
   then links (PR, agent URL, artifacts). No walls of prose.
4. **Artifacts over “run it locally.”** Screenshots, recordings, and PR diffs
   are how this user checks work from a phone.
5. **Repo skills only.** `~/.cursor/skills/` is invisible to cloud/mobile
   workers. New skills go in `.cursor/skills/<name>/SKILL.md` (and
   `.claude/skills/<name>/` if Claude Code must see them too).
6. **Honor pasted agent URLs.** Treat `cursor.com/agents/<bcId>` as a
   deliverable to import. See the import workflow below.

## Import another cloud agent

When the user pastes `https://cursor.com/agents/bc-…` and says “add this”:

1. Parse the `bcId`.
2. Call Cursor Cloud MCP `batch-fetch-details` with transcripts + diff
   metadata (+ events if useful).
3. If a branch/PR exists, copy or recreate that deliverable on **this**
   branch. Do not wait for the other agent to finish if the request is
   already clear.
4. If the other run is **not accessible** (different environment, not
   owned, expired), say that in one sentence and still complete the named
   request (branch name, skill, file, etc.).
5. Record the source URL in the PR body.

This skill itself was requested that way. The source run was
`bc-01a04166-0796-727e-93d6-04dfd0978582` and was not readable from this
environment; see `references/source-agent.md`.

## What mobile can and cannot do

| On the phone | Stays on web / desktop |
| --- | --- |
| Start, follow, and follow-up agents | Editor, terminal, file browser |
| Review and merge PRs | Secrets, environments, SCM connect |
| Voice, camera, photos, Design Mode markup | Add/manage MCP servers (pick per-run on mobile) |
| Slash commands and **repo** skills | Skill/rule/automation *config* |
| Live Activities (up to 8) | Admin, billing, usage |

Android has no native Cursor app yet. Use [cursor.com/agents](https://cursor.com/agents)
in the browser (install as a PWA).

## This repository

Personal working repo for Dr. Rahman. Verbal-thinker input is the default,
not an edge case. Existing domain skills (legal, health data, prompt
optimization, second brain) still apply — this skill only changes *how*
the run behaves when it started on a phone.

Versioned work goes in a new directory (`_v2`, `_v3`), never an in-place
overwrite of a finished deliverable.

## Done means

- Work is committed and pushed on the requested branch
- A PR exists that can be read and merged from the Cursor iOS review UI
- The final message is short enough to read on a lock screen, with the PR
  link first
