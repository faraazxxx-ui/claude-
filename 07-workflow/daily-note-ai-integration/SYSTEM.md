# Your System — One Page, Everything Decided

---

## THE ANSWER (read this first, stop here if it clicks)

**You have 9 tools doing 3 jobs. You need 3 tools doing 3 jobs.**

```
┌──────────────────────────────────────────────────────────────┐
│                     YOUR 3 TOOLS                             │
│                                                              │
│   1. OBSIDIAN ──── See everything (graph, daily notes)       │
│   2. ONENOTE ───── Write everything (Surface pen input)      │
│   3. NOTION ────── Store everything (invisible, never open)  │
│                                                              │
│          You touch: Obsidian + OneNote                        │
│          You never touch: Notion                              │
│          Everything else: sunset or capture-only              │
└──────────────────────────────────────────────────────────────┘
```

**Your daily flow is 3 moments:**

```
MORNING (Surface, 3 min)
  Draw/write today's plan in OneNote → auto-converts to Obsidian

DURING DAY
  AI chats auto-save to Notion → appear as nodes in Obsidian graph

EVENING (Surface, 2 min)
  Open Obsidian → see your day as connected nodes → mark done
```

That's it. The rest of this document is implementation.

---

## THE MAP (how it all connects)

```
                YOU + SURFACE PEN
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
    ┌──────────┐ ┌─────────┐ ┌─────────────┐
    │ OneNote  │ │  Bear   │ │ Google Keep  │
    │ DRAW +   │ │ (phone  │ │ (phone      │
    │ WRITE    │ │  only)  │ │  only)      │
    └────┬─────┘ └────┬────┘ └──────┬──────┘
         │            │             │
         ▼            ▼             ▼
    ┌─────────────────────────────────────┐
    │        POWER AUTOMATE / MAKE        │
    │     (auto-converts everything)      │
    └──────────────────┬──────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────┐
    │                                     │
    │    ★  OBSIDIAN  ★                   │
    │    Your ONE window into everything  │
    │                                     │
    │    📊 Graph View = your thinking    │
    │    📅 Full Calendar = your schedule │
    │    📝 Daily Note = your anchor      │
    │    🔗 Every node = a thought        │
    │                                     │
    └──────────────────┬──────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    ┌─────────┐  ┌──────────┐  ┌──────────────┐
    │ Google  │  │ Priority │  │  NotebookLM  │
    │Calendar │  │ Matrix   │  │  (weekly     │
    │ (sync)  │  │(Eisen-   │  │   audio)     │
    │         │  │ hower)   │  │              │
    └─────────┘  └──────────┘  └──────────────┘

    ┌─────────────────────────────────────┐
    │          AI OUTPUT PIPELINE         │
    │                                     │
    │  Claude ──┐                         │
    │  ChatGPT ─┤  Pactify     Notion     │
    │  Grok ────┼─ extension → database → │
    │  Gemini ──┤  (auto)     (invisible) │
    │  Raycast ─┘               │         │
    │                           ▼         │
    │                    Obsidian graph    │
    │                    (you see nodes)   │
    └─────────────────────────────────────┘
```

---

## THE DAILY NOTE (what you actually see each morning)

This is designed for a person who **draws and talks through their day**, not someone who fills tables. It auto-generates. You handwrite into it or just open it and start thinking.

```yaml
---
date: "{{date:YYYY-MM-DD}}"
day: "{{date:dddd}}"
type: daily
tags: [daily]
---
```

```markdown
# {{date:dddd, MMMM D}}

---

## What went well yesterday
1.
2.
3.

## What I'd do differently
1.
2.
3.

---

## Today

### My 3 tasks
- [ ] 🔴
- [ ] 🟡
- [ ] 🔵

> 🔴 = must happen today  🟡 = important not urgent  🔵 = if time allows

### My 3 events
- **___** —
- **___** —
- **___** —

---

## Inbox
> Everything below auto-populates. Don't touch it.

### Surface notes (auto-converted from OneNote)
```{{surface-ocr-output}}```

### AI conversations today
- {{auto: ai-outputs}}

### Quick captures (Keep / Bear)
- {{auto: captures}}

---

*→ [[{{date-1:YYYY-MM-DD}}]] yesterday | tomorrow [[{{date+1:YYYY-MM-DD}}]] →*
```

### Why this template works for you:
- **Top section** = reflection prompts, not tables. You talk through these.
- **Tasks** = 3 max, color-coded by Eisenhower quadrant (visual, instant).
- **Events** = blank slots, not a structured table. Fill by writing.
- **Inbox** = everything below the line is AUTO. You never type here.
- **No sections you'll skip** = if you wouldn't fill it at 7am half-awake, it's not here.

---

## WHAT EACH TOOL DOES (one role, no overlap)

### Tools You Touch

| Tool | One Job | How You Use It |
|------|---------|---------------|
| **Obsidian** (Windows Surface) | See + think + connect | Open daily. Graph view is your thinking. Full Calendar plugin is your schedule. This is your ONE app. |
| **OneNote** (Surface pen) | Handwrite + draw | Write/draw plans with your pen. Never organize here. Power Automate pulls it into Obsidian automatically. |
| **Microsoft Whiteboard** (Surface) | Spatial brainstorm | Freeform drawing for big-picture thinking. Exports as images → Obsidian attachments. |

### Tools That Run Silently

| Tool | One Job | You Never Open It |
|------|---------|------------------|
| **Notion** | AI output database | Every AI chat auto-saves here. You only see it as nodes in Obsidian's graph. |
| **Power Automate** | Convert handwriting | Watches OneNote → extracts text → writes markdown to Obsidian vault. |
| **Make.com** | Sync captures | Pulls Google Keep / Bear notes into Obsidian's inbox folder. |
| **Pactify** (Chrome extension) | Capture AI chats | Auto-saves Claude/ChatGPT/Gemini/Grok conversations to Notion. |

### Tools Demoted to Phone-Only Capture

| Tool | New Role | Why |
|------|----------|-----|
| **Google Keep** | Quick phone capture | Voice memos, quick thoughts on the go. Auto-syncs to Obsidian inbox. No organizing here. |
| **Bear** | Writing on iPhone | Beautiful quick writing. Tagged `#inbox` → auto-exported to Obsidian nightly via Shortcuts. |

### Tools You Stop Using

| Tool | Why You're Done |
|------|----------------|
| **Evernote** | Export all notes to Obsidian (ENEX → Markdown converter). Obsidian does everything Evernote does, better. Backlinks broke Oct 2025. Delete account. |
| **NotePlan** | Apple-only. No Windows version exists or is planned. Obsidian + Full Calendar plugin gives you the same drag-and-drop on your Surface. Skip it. |

---

## THE 4 OBSIDIAN PLUGINS (install these, nothing else to start)

Don't install 20 plugins. Install 4. Add more only when you hit a wall.

| Plugin | What It Replaces | Install Priority |
|--------|-----------------|-----------------|
| **Full Calendar** | NotePlan's drag-and-drop scheduling | Day 1 — this is your calendar |
| **Templater** | Manual daily note creation | Day 1 — auto-generates your daily note each morning |
| **Dataview** | Searching through notes manually | Week 1 — queries your vault like a database |
| **Periodic Notes** | Remembering to create weekly reviews | Week 1 — auto-generates weekly/monthly notes |

**Later (only when you need them):**
- Kanban (visual task boards — you'll like this as a spatial thinker)
- Excalidraw (draw directly in Obsidian — may replace Whiteboard)
- Style Settings (customize graph colors by node type)

---

## OBSIDIAN GRAPH VIEW (your actual interface)

You said you love the visualization where you can see notes and where they lead. This is your primary interface. Configure it:

### Color Coding (by folder)
```
🔵 Blue    = Daily notes        (Daily/ folder)
🟢 Green   = Projects           (Projects/ folder)
🟡 Yellow  = AI conversations   (AI/ folder)
🟣 Purple  = Handwritten notes  (Inbox/Surface/ folder)
⚪ White   = Everything else
```

### Vault Folder Structure
```
YourVault/
├── Daily/              ← auto-generated daily notes
├── Weekly/             ← auto-generated weekly reviews
├── Projects/           ← one note per project
├── AI/                 ← auto-populated AI conversations
├── Inbox/
│   ├── Surface/        ← converted handwriting from OneNote
│   ├── Keep/           ← phone captures from Google Keep
│   └── Bear/           ← exports from Bear
├── Attachments/        ← images, whiteboard exports
└── Templates/          ← daily note template lives here
```

### Graph Filters (save these)
- **"Today"** — show only nodes linked to today's daily note
- **"This Week"** — show daily notes + any linked nodes from this week
- **"AI Research"** — filter to AI/ folder only
- **"Active Projects"** — filter to Projects/ folder, tag:active

---

## AI OUTPUT PIPELINE (zero-effort capture)

### What You Install

**One Chrome extension: [Pactify](https://pactify.io)**
- Supports: Claude, ChatGPT, Gemini, Grok
- Auto-saves conversations to your Notion database on every visit
- 97%+ formatting accuracy
- You install it once and forget it exists

**For Claude Code** (CLI sessions like this one):
- A file watcher script monitors `~/.claude/projects/`
- Nightly cron extracts sessions → formats with YAML → pushes to Notion

### What Happens Automatically

```
You have an AI conversation
        ↓
Pactify captures it (you do nothing)
        ↓
Notion database stores it with:
  - Title, date, platform, model
  - Auto-generated topic tags
  - Key outputs summary
  - Action items extracted
        ↓
Obsidian sync pulls it as a markdown file into AI/ folder
        ↓
It appears as a yellow node in your graph
        ↓
Weekly: files push to Google Drive folder
        ↓
You open NotebookLM once (30 sec) → get audio summary of your week's AI work
```

### Notion Database (you never see this)

| Field | Type | Auto-filled? |
|-------|------|-------------|
| Title | Text | Yes — from conversation |
| Date | Date | Yes — capture timestamp |
| Platform | Select | Yes — claude/chatgpt/grok/gemini |
| Tags | Multi-select | Yes — auto-generated topics |
| Summary | Text | Yes — 3-point summary |
| Action Items | Text | Yes — extracted TODOs |
| Status | Select | Default: unreviewed |
| Obsidian Synced | Checkbox | Yes — after markdown written |

---

## HANDWRITING PIPELINE (Surface → Obsidian)

### What Happens When You Write

```
You pick up your Surface Pen
        ↓
Write/draw in OneNote (your natural behavior — change nothing)
        ↓
OneNote's Ink-to-Text converts your handwriting (built-in, English)
        ↓
Power Automate detects the new/edited page
        ↓
Extracts text, wraps in YAML frontmatter, saves as .md
        ↓
File lands in YourVault/Inbox/Surface/2026-03-28-my-note.md
        ↓
Obsidian sees it. It's now a purple node in your graph.
```

### Power Automate Flow (set up once)
1. **Trigger**: "When a page is updated in OneNote"
2. **Action**: Get page content (OneNote connector)
3. **Action**: Strip HTML tags, keep plain text
4. **Action**: Wrap in markdown with YAML header (title, date, source: surface, tags: handwritten)
5. **Action**: Create file in OneDrive folder synced to Obsidian vault

### For Whiteboard drawings:
- Export as PNG → save to `Attachments/` folder
- A markdown note auto-creates with `![[image.png]]` embed
- Drawing appears in Obsidian as an embedded visual node

---

## SETUP CHECKLIST (do this once, in order)

### Hour 1: Obsidian
- [ ] Install Obsidian on Windows Surface
- [ ] Create vault with the folder structure above
- [ ] Install 4 plugins: Full Calendar, Templater, Dataview, Periodic Notes
- [ ] Paste the daily note template into `Templates/Daily.md`
- [ ] Configure Templater to auto-apply template to new daily notes
- [ ] Connect Google Calendar to Full Calendar plugin via ICS URL

### Hour 2: Handwriting Pipeline
- [ ] Open Power Automate on Windows
- [ ] Create the OneNote → Obsidian flow (5 nodes, described above)
- [ ] Test: write something in OneNote → verify it appears in Obsidian

### Hour 3: AI Capture
- [ ] Create a Notion account (or use new login as you requested)
- [ ] Create "AI Outputs" database with the schema above
- [ ] Install Pactify Chrome extension → connect to Notion database
- [ ] Test: have a short Claude chat → verify it appears in Notion

### Hour 4: Connect the Loop
- [ ] Set up Notion → Obsidian sync (use "Notion to Obsidian" plugin or n8n workflow)
- [ ] Verify: AI conversation in Notion → appears as node in Obsidian graph
- [ ] Export all Evernote notes → import to Obsidian vault (use Evernote ENEX to MD converter)
- [ ] Set up Bear auto-export via Apple Shortcuts (if using iPhone)

### Week 1: Fine-Tune
- [ ] Adjust graph view colors and filters
- [ ] Add Kanban plugin if you want visual task boards
- [ ] Set up NotebookLM Google Drive folder for weekly AI digests
- [ ] Delete Evernote account

---

## WHAT I FIXED FROM YOUR ORIGINAL WORKFLOW

| Your Pain | Root Cause | What Changes |
|-----------|-----------|--------------|
| "Notes everywhere, nothing connected" | 9 tools, no architecture | 3 tools, one hub (Obsidian) |
| "Bear notes are chaotic" | No folders, just tags | Bear demoted to capture. Obsidian organizes. |
| "Google Keep isn't integrated" | No personal API exists | Keep demoted to phone capture. Auto-syncs via Make.com. |
| "I like NotePlan but don't understand it" | It's Apple-only, can't use on Surface | Replaced by Obsidian + Full Calendar (same feature, works on Windows) |
| "I write on Surface but it goes nowhere" | No OCR pipeline | OneNote → Power Automate → Obsidian (automated) |
| "AI chats pile up everywhere" | No capture mechanism | Pactify auto-saves every chat to Notion → Obsidian |
| "Evernote is a disappointment" | Backlinks broke, aging API | Sunset. Export to Obsidian. |
| "I love graph visualization" | Only had it in Obsidian but didn't use Obsidian as hub | Obsidian IS the hub now. Everything feeds into its graph. |
| "I hate Notion but see the benefit" | Forced to interact with it | You never open Notion. It's an invisible database. |
| "AI outputs should be in NotebookLM" | No automation to NotebookLM | Weekly auto-push to Google Drive → you click once for audio |

---

*This is one system. One file. One decision per tool. If a section doesn't apply to your morning, your automation handles it. You write with your pen, you think in your graph, and everything else is silent.*
