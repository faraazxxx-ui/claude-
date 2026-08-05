# Hermes System — One Door, One File, Everything Decided

*Supersedes `daily-note-ai-integration/SYSTEM.md` (that one was built for a Windows Surface. You're on a MacBook now. Half of it no longer runs.)*

---

## THE ANSWER (stop here if it clicks)

**Your problem was never the tools. It was the doorway.**

Every tool you own asks you to decide *which tool* before you can do anything.
That decision, thirty times a day, is the tax. That's the overwhelm.

**Hermes removes the doorway. You get one contact. You talk to him. He runs the rest.**

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   YOU  ──voice──▶  HERMES  ──▶  everything else            │
│                                                            │
│   You never choose a tool again.                           │
│   You never file anything again.                           │
│   You talk. He decides. He remembers.                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Your whole day is now three moments:**

```
06:00   Hermes texts you the brief.        You read it in bed. 60 sec.
ALL DAY You voice-note him. That's it.     No app choice. No filing.
NIGHT   He files, updates, preps tomorrow. You are asleep.
```

The rest of this file is installation.

---

## THE MAP

```
                        YOU
                  (voice, one thread)
                         │
                    ┌────▼─────┐
                    │  HERMES  │   always on · remembers you
                    │  on your │   writes its own skills
                    │  MacBook │   runs at night
                    └────┬─────┘
          ┌──────────────┼──────────────┬──────────────┐
          ▼              ▼              ▼              ▼
    ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌───────────┐
    │  GEMMA 4 │  │ CLAUDE CODE│  │  GOOGLE  │  │  CLAUDE   │
    │  (local) │  │            │  │ WORKSPACE│  │   chat    │
    │          │  │            │  │          │  │           │
    │ private  │  │  builds    │  │  system  │  │  thinking │
    │  + free  │  │  things    │  │ of record│  │  out loud │
    │          │  │            │  │          │  │           │
    │ health   │  │ repos      │  │ Drive    │  │ YOU open  │
    │ legal    │  │ skills     │  │ Gmail    │  │ this one. │
    │ filing   │  │ documents  │  │ Calendar │  │ Only one. │
    │ tagging  │  │            │  │          │  │           │
    └──────────┘  └────────────┘  └──────────┘  └───────────┘
     never leaves   Hermes calls    Hermes reads    the only tool
      your Mac        this           and writes    you open yourself
```

**One rule:** you only ever talk to Hermes. The single exception is Claude chat, when you want to think out loud with something in the room with you. Everything else, Hermes reaches for.

---

## WHY THIS FIXES THE THING YOU ACTUALLY HAVE

Your last audit named it exactly. Pulling it forward so it doesn't get lost:

> *"Drowning in tool sprawl — feels overwhelmed, not empowered."*
> *"Wants ZERO manual organizing — if it needs discipline to maintain, it will fail."*
> *"Adopts tools impulsively, abandons when they require discipline."*
> — `daily-note-ai-integration/RED_TEAM_ANALYSIS.md`

Every system you've built so far failed at the same joint: **it needed you to maintain it.**
Obsidian needed you to open it. Notion needed you to file. The daily note needed you to fill it in at 7am.

Hermes is the first thing in your stack that **does the maintenance itself, overnight, whether or not you show up.** That is the entire reason it's worth your time. Not the memory, not the skills — the fact that the discipline tax moves off you and onto a machine that never gets tired, distracted, or demoralized.

| Your pattern | What used to happen | What happens now |
|---|---|---|
| Thought arrives mid-task | Lost, or dumped into whichever app was open | Voice-note to Hermes. Filed correctly at 9pm. |
| "Which tool do I use?" | 30 seconds of friction × 30 times/day | Deleted. There is one contact. |
| System needs upkeep | You abandon it in week 3 | Upkeep runs at 3am without you |
| Morning starts cold | Open 6 apps, rebuild context | One message, already waiting |
| AI output everywhere | Never captured | Hermes is the capture point |

---

## SETUP — ONE HOUR, IN ORDER

### 1. Point at your local model (15 min)

You downloaded a local Gemma 4 on the MacBook. Find its exact tag:

```bash
ollama list
```

If it isn't there:

```bash
ollama pull gemma4
```

Then serve it with a context window big enough for agent work. **Ollama's default is far too small and this is the #1 reason local agents feel stupid:**

```bash
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
```

Check it took:

```bash
ollama ps      # the CONTEXT column should read 64000
```

### 2. Install Hermes (10 min)

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
```

Or, since you already have Ollama, the one-liner that wires both together:

```bash
ollama launch hermes
```

### 3. Give it two brains (10 min)

This is the money decision. **One smart brain for thinking, one local brain for grunt work and anything private.**

```bash
hermes model
```

- **Main model → Claude Opus** (via Nous Portal or OpenRouter). This is what plans, reasons, drafts.
- **Local model → your Gemma 4.** Choose *"Custom endpoint"* → URL `http://127.0.0.1:11434/v1` → leave API key blank → pick your `gemma4` tag.

Config lives at `~/.hermes/config.yaml` and looks roughly like this:

```yaml
model:
  default: claude-opus-5
  provider: openrouter

auxiliary:
  vision:
    provider: custom
    base_url: http://127.0.0.1:11434/v1
    model: gemma4
  compression:
    provider: custom
    base_url: http://127.0.0.1:11434/v1
    model: gemma4
```

Then verify — Hermes has a built-in check for exactly this:

```bash
hermes doctor
```

### 4. Put it in a box (10 min)

**Read this part.** Hermes runs terminal commands on your Mac by itself. Your Mac has your medical records and an active federal case file on it. So:

```bash
hermes config set terminal.backend docker     # needs Docker Desktop installed
hermes config set memory.memory_enabled true
```

Keep command approvals **ON**. Don't turn them off in month two when they get annoying — that's the month you'll regret it. If you skip Docker, approvals become the only thing standing between an autonomous agent and your case files.

### 5. One channel, locked to you (5 min)

```bash
hermes gateway setup      # pick WhatsApp — you already live there
hermes gateway install    # keeps it alive across reboots
```

Allow **only your own number**. Nobody else gets to text your agent.

### 6. Give it five routines (10 min)

You don't write cron syntax. You *tell him*, in the chat, in plain English. Send these five messages:

```
1. Every weekday 6am: send me a brief. What's on my calendar, the 3 things
   that actually matter today, and anything that broke overnight. One message,
   short. I read it in bed.

2. Every day at 9pm: take everything I sent you today and file it properly.
   Don't ask me where things go — decide, then tell me in one line what you did.

3. Every Sunday 8pm: week ahead, plus the things I said I'd do this week and
   didn't. Be blunt about the second part.

4. Every weekday 7am: check the docket for 3:26-cv-00197 and flag any deadline
   inside 14 days.

5. Every night: pull my health data, give me a 3-line trend. Use the local
   model only — this data does not leave my Mac.
```

That's the install. One hour.

---

## HOW EVERYTHING ELSE GETS DEMOTED

One job each. No overlap. No decisions left for you.

| Tool | Its one job | Do you open it? |
|---|---|---|
| **Hermes** | The door. Capture, dispatch, memory, night shift. | **Yes — this is the only thing you open by default** |
| **Claude chat / Cowork** | Thinking out loud when you want something in the room | Yes, deliberately, when you *want* to think |
| **Claude Code** | Building real things: repos, skills, documents, this file | No — Hermes hands work to it |
| **Gemma 4 (local)** | Private + cheap: health data, case files, tagging, filing | No — it's Hermes's second brain |
| **Google Workspace** | System of record: Drive, Gmail, Calendar | No — Hermes reads and writes it |
| **Gemini Enterprise** | Deep research *across your own Workspace corpus* | Rarely. Ask Hermes first. |
| **Obsidian** | Seeing the graph when you want to *look* at your thinking | Only when you want the visual |
| **Notion / Keep / Bear / Evernote** | Nothing. Capture-only or gone. | No |

**The demotion that matters most:** you are no longer the integration layer between these tools. That was the job you kept failing at, and it was never a discipline problem — it was an architecture problem. Nobody can hold nine tools in working memory.

---

## WHAT CHANGED FROM YOUR OLD SYSTEM

Your previous system was correct for the machine you had then. You've changed machines, and a better piece exists now.

| Old system said | Why it's dead | Replacement |
|---|---|---|
| Power Automate converts OneNote → Obsidian | Windows-only. You're on a Mac. | Hermes's 9pm sweep |
| Pactify Chrome extension captures AI chats | Only catches browser chats, misses everything you *say* | Hermes is the capture point |
| Notion as the invisible database | Still needed a sync you'd have to maintain | Hermes's own memory in `~/.hermes/` |
| You open Obsidian daily to see the graph | Requires daily discipline. It failed. | Obsidian is now optional — for when you *want* the picture |
| Daily note you fill in at 7am | You were never going to fill it in at 7am | 6am brief, already written, you just read it |
| "NotePlan is Apple-only, skip it" | You're on Apple now — but don't reopen this | Still skip it. One decision per tool. Obsidian stays. |

---

## THE HONEST CAVEATS

**Hermes will not fix a messy operation. It will run your mess faster.** The five routines above are deliberately few. Add a sixth only when you've felt the absence of it for a week.

**Month three is the test.** Every system you've adopted has died around week three, when the novelty ends. This one survives that week *only* because the crons keep running whether or not you engage. If you find yourself editing the routines more than using them, you've turned it back into a tool that needs discipline — stop, and cut back to three.

**Local model ≠ free lunch.** Gemma 4 on a MacBook is genuinely good at filing, tagging, summarizing, and reading your health exports. It is not good enough to plan your litigation strategy or draft anything that matters. That's what the main model is for. Don't let cost-saving push real work onto the small brain.

---

*One file. One door. One rule: you talk to Hermes, Hermes handles the rest. If a piece of this needs your daily discipline to survive, it's wrong — come back and delete it.*
