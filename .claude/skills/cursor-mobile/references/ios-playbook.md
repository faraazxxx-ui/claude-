# Cursor for iOS playbook

Official references:

- [Cursor for iOS](https://cursor.com/docs/cloud-agent/mobile.md)
- [Mobile app help](https://cursor.com/help/ai-features/mobile-app.md)
- [Cloud agents](https://cursor.com/docs/cloud-agent.md)
- [Skills](https://cursor.com/docs/skills.md)
- [App Store](https://apps.apple.com/app/cursor/id6767085653)

## Setup

1. Install Cursor from the App Store on iPhone (iOS 26.0+) or iPad (iPadOS 26.0+).
2. Sign in with the Cursor account (SSO if the org requires it).
3. Pick the repository and branch. The picker only shows source control already
   connected on the web. Empty picker → connect GitHub/GitLab at cursor.com,
   then pull-to-refresh the inbox.
4. Send a task. The agent keeps working after the phone locks.

The app is English-only. It is available in all App Store regions except
mainland China. Cloud Agents need Privacy Mode (not Legacy). Plans that can
start agents: Start, Pro, Pro+, Ultra, Teams, Enterprise. Signing in on a free
account does not start runs.

## What to use the phone for

- Kick off a bugfix, incident, refactor, or research task away from the desk
- Watch the chat stream; send follow-ups; open a subagent card
- Review full diffs, checks, comments; request reviewers; merge (squash),
  mark ready, update branch, auto-merge, close
- Dictate with voice; attach camera shots or files; mark up images (Design
  Mode). iPad: Apple Pencil, sidebar chats, review beside chat
- Track up to eight agents via Live Activities / Dynamic Island (enable the
  iOS permission for Cursor)

Agents started on mobile appear at cursor.com/agents, in the desktop Agents
Window, and in the app inbox. Docs tag them `iosApp`; some run metadata
reports `source: mobile`. Treat both as mobile-launched.

## Remote Control (direct your computer from the phone)

Requires Cursor **3.9.8+**, Agents Window, a paid plan with Cloud Agents, and
(on Teams/Enterprise) admin enablement at Dashboard → Cloud Agents → Self-Hosted.

1. On the computer: Settings → Agents → enable Remote Control. Keep the
   machine awake and online (`Keep this computer awake` if plugged in).
2. In the agent input, run `/remote-control`, then send the next message.
3. Open the session from the phone inbox.

The agent loop runs in the cloud; terminal, edits, tests, and git run on the
computer. Repo, secrets, and caches stay on the machine.

## What you cannot do in the app

No editor, terminal, or file browser. Changed files show in the diff view.
Configure environments, secrets, MCP server *definitions*, GitHub/GitLab
connect, automations/rules/skills *config*, billing, and admin on the web.

Skills, slash commands, and automations **already in the repo or account**
work the same on mobile as on web/CLI. They are not edited from the phone.

## If the app feels stuck

1. Update from the App Store
2. Pull down on the inbox to re-sync
3. Reinstall only as a last resort (clears local cache)

Slow starts are usually cloud environment setup, not the phone. Compare with
the same agent on cursor.com/agents.

## Report a problem

Include device + iOS version, app version (profile → version footer), the
agent `bcId` from cursor.com/agents, and a screenshot if possible.
