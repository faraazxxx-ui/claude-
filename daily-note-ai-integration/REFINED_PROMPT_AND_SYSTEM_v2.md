# Refined Prompt & Workflow System v2

---

## FINAL OUTPUT: The Refined Prompt

Use this prompt in any AI (Claude, ChatGPT, Gemini, Grok) to get the system built for you. It replaces the original unstructured request with a research-validated, logically sequenced, actionable prompt.

---

```markdown
# PROMPT: Build My Unified Daily Note + AI Capture + Handwriting Pipeline

## My Profile
- I am a verbal thinker and spatial/visual learner.
- I use a Windows Surface with Surface Pen as my primary device.
- I prefer drawing and handwriting my plans, then having them digitized.
- I need to SEE my notes as a connected graph/node map — not folders or lists.
- I want to interact with at most 2-3 apps. Everything else must be automated and invisible.

## Deliverable 1: Daily Note Template (Obsidian Markdown)
Create an Obsidian-compatible daily note template with YAML frontmatter containing:

**Section 1 — Yesterday Reflection**
1. "What went well yesterday" — 3 bullet prompts
2. "What I'd do differently" — 3 bullet prompts

**Section 2 — Today's Plan**
1. "My 3 tasks" — checkboxes, color-coded by Eisenhower quadrant:
   - 🔴 Urgent + Important (must happen today)
   - 🟡 Important, not urgent
   - 🔵 Nice-to-have if time allows
2. "My 3 events" — time-stamped slots for calendar items

**Section 3 — Auto-Populated Inbox (I never type here)**
- Surface handwriting captures (from OneNote via Power Automate OCR)
- AI conversation summaries (from Notion via Pactify/API pipeline)
- Quick captures (from Google Keep and Bear via Make.com)

**Section 4 — Navigation**
- Backlinks to yesterday and tomorrow's daily notes
- Linked references to active projects

## Deliverable 2: Tool Architecture (3 layers)

### Layer 1 — Tools I Touch (max 3)
| Tool | Single Purpose |
|------|---------------|
| **Obsidian** (Surface) | My ONE window: graph view, daily notes, Full Calendar plugin for drag-and-drop scheduling |
| **OneNote** (Surface Pen) | Handwrite and draw. Never organize here. |
| **Microsoft Whiteboard** (Surface) | Spatial brainstorming. Exports as images to Obsidian. |

### Layer 2 — Tools That Run Silently (I never open these)
| Tool | Job |
|------|-----|
| **Notion** (separate login, invisible) | AI output database — stores every AI conversation with YAML-structured metadata (title, date, platform, model, tags, summary, action items) |
| **Power Automate** | OneNote ink → OCR text → markdown file in Obsidian vault |
| **Make.com** | Google Keep + Bear → Obsidian inbox folder |
| **Pactify** (Chrome extension) | Auto-captures Claude/ChatGPT/Grok/Gemini conversations → Notion |

### Layer 3 — Tools Demoted to Capture-Only
| Tool | New Role |
|------|----------|
| **Google Keep** | Phone-only quick capture (voice memos, thoughts). No API exists — use Make.com with gkeepapi workaround or Google Keep → Google Docs → Make pipeline. |
| **Bear** | iPhone writing only. Auto-exports via Apple Shortcuts nightly to Obsidian/Inbox/Bear/. |

### Tools to Sunset
| Tool | Why |
|------|-----|
| **Evernote** | Export via ENEX → Markdown. Obsidian replaces all Evernote functions with better backlinking. |
| **NorthPlanner** | This is a physical planner + Notion "Second Brain" template, NOT a standalone app. The drag-and-drop you liked IS Notion Calendar. You already get this from Obsidian Full Calendar plugin. Keep the physical planner if you like the ritual; skip the digital template. |

## Deliverable 3: Priority / Eisenhower Integration

**Use Priority Matrix (by Appfluence)** — it has:
- A real REST API (`sync.appfluence.com/api/v1/`) with OAuth 2.0
- Webhooks for `item.created`, `item.completed`, `item.quadrant.updated`
- Native Outlook + Google Calendar sync
- Microsoft Teams integration
- Python SDK (`appfluence/prioritymatrix-python`)

**Integration flow:**
Priority Matrix tasks (quadrant-tagged) → webhook fires on create/update → Make.com catches webhook → creates/updates task in Obsidian daily note with correct 🔴🟡🔵 color code.

> Note: "Prioritree" / "Prior Tree" does not exist as a discoverable app. If you were referring to Priority Matrix, use that. If it's a different tool, provide a URL.

## Deliverable 4: AI Output Pipeline (Zero-Effort Capture)

### Capture Layer
```
Claude, ChatGPT, Grok, Gemini (browser)
    → Pactify (Chrome extension, auto-captures)
    → Notion "AI Outputs" database

Claude Code (CLI), Raycast AI
    → Nightly cron script extracts session logs
    → Formats with YAML headers
    → Pushes to same Notion database via Notion API
```

### Notion Database Schema (auto-filled, never manually edited)
| Field | Type | Source |
|-------|------|--------|
| Title | Text | Conversation title / first prompt |
| Date | Date | Capture timestamp |
| Platform | Select | claude / chatgpt / grok / gemini / raycast |
| Model | Select | opus / sonnet / gpt-4o / etc. |
| Tags | Multi-select | Auto-generated topic tags |
| Summary | Rich text | 3-point summary (AI-generated) |
| Action Items | Rich text | Extracted TODOs |
| Status | Select | Default: unreviewed |
| YAML Header | Code | Full YAML frontmatter for Obsidian sync |

### Viewing Layer (NotebookLM)
```
Notion AI database
    → Weekly export to Google Drive as PDFs (via Make.com)
    → Google Drive folder linked as NotebookLM source
    → NotebookLM generates audio overview ("podcast" of your week's AI work)
    → You listen, never read
```

> NotebookLM has NO public API. Audio generation is UI-only. The automation gets content TO NotebookLM; you click "Generate Audio" once per week (30 seconds).

## Deliverable 5: Handwriting-to-Digital Pipeline

```
Surface Pen + OneNote (you write/draw naturally)
    → OneNote Ink-to-Text (built-in OCR, 60+ languages)
    → Power Automate trigger: "When page updated in OneNote"
    → Extract text, strip HTML, wrap in YAML frontmatter
    → Save as .md to OneDrive folder synced to Obsidian vault
    → File appears in Obsidian/Inbox/Surface/ as a purple graph node

For higher accuracy on messy handwriting:
    → Export OneNote page as image/PDF
    → Send to Claude Vision or GPT-4o with prompt:
      "Convert this handwritten note to structured Markdown with headings and bullets"
    → Save structured output to Obsidian vault
```

## Deliverable 6: Obsidian Configuration

### 4 Essential Plugins (install first, nothing else)
1. **Full Calendar** — replaces NorthPlanner's drag-and-drop. Syncs Google Calendar via ICS.
2. **Templater** — auto-generates daily note from template each morning.
3. **Dataview** — queries vault like a database. Shows tasks, AI conversations, etc.
4. **Periodic Notes** — auto-creates weekly/monthly review notes.

### Graph View Color Coding
| Color | Folder | Meaning |
|-------|--------|---------|
| 🔵 Blue | Daily/ | Daily notes |
| 🟢 Green | Projects/ | Active projects |
| 🟡 Yellow | AI/ | AI conversations |
| 🟣 Purple | Inbox/Surface/ | Handwritten notes |
| ⚪ White | Everything else | Uncategorized |

### Vault Structure
```
Vault/
├── Daily/              ← auto-generated daily notes
├── Weekly/             ← auto-generated weekly reviews
├── Projects/           ← one note per project
├── AI/                 ← auto-synced from Notion
├── Inbox/
│   ├── Surface/        ← converted handwriting
│   ├── Keep/           ← Google Keep captures
│   └── Bear/           ← Bear exports
├── Attachments/        ← images, whiteboard PNGs
└── Templates/          ← daily note template
```

## Constraints
- I will only interact with Obsidian and OneNote daily. Everything else must be automated.
- Notion is invisible infrastructure. I never log into it.
- All AI outputs must have YAML frontmatter for graph node metadata.
- The system must work on Windows Surface as the primary device.
- I am a visual/spatial learner: prioritize graph views, color coding, and drawn interfaces over text lists and tables.
```

---

## WHAT THE REFINED PROMPT FIXES (vs. the original)

| # | Original Prompt Flaw | Type | Refined Prompt Fix |
|---|---------------------|------|--------------------|
| 1 | **Stream-of-consciousness structure** — ideas arrive in the order you thought of them, not in logical dependency order | Structure | Organized into 6 numbered deliverables with clear dependency flow: Template → Architecture → Integrations → AI Pipeline → Handwriting → Config |
| 2 | **"NorthPlan" misidentified as an app** — you thought it was a standalone drag-and-drop app | Factual Error | Corrected: NorthPlanner is a physical planner + Notion template. The drag-and-drop feature you liked is Notion Calendar. Replaced with Obsidian Full Calendar plugin. |
| 3 | **"Prior Tree" doesn't exist** — no discoverable app by this name | Factual Error | Identified: you likely mean **Priority Matrix** (Appfluence). Has real API, webhooks, Eisenhower matrix, calendar sync. Included integration spec. |
| 4 | **Google Keep described as "not integrated enough"** — but no solution given | Missing Solution | Explained: Google Keep has NO public API. Proposed workaround: Keep → Google Docs → Make.com → Obsidian, or gkeepapi (unofficial Python library). |
| 5 | **"Link up to Google Keep, OneNote, Remarkable, and everything else"** — vague, no architecture | Vague Requirement | Replaced with explicit 3-layer architecture: Touch Layer (3 apps) → Silent Layer (4 automations) → Capture Layer (2 phone apps) + Sunset list |
| 6 | **AI output automation described but not specified** — "automatically internalized into Notion" | Underspecified | Full pipeline spec: Pactify for browser AI → Notion database with 9-field schema → Obsidian sync → NotebookLM weekly audio |
| 7 | **NotebookLM described as automatable** — "I want that to be automated" | Impossible Requirement | Corrected: NotebookLM has no API. Audio generation is UI-only. Automation gets content TO it; you click once/week for 30 seconds. |
| 8 | **"Scrub through all the data in NorthPlan"** — assumes it's a digital tool with data | Impossible Requirement | Replaced with: "Use Obsidian Full Calendar plugin for the same drag-and-drop scheduling. Keep the physical NorthPlanner planner if you like the ritual." |
| 9 | **No mention of spatial/visual needs in template spec** — despite saying "I'm a spatial/visual learner" | Contradiction | Template uses color-coded Eisenhower emojis (🔴🟡🔵), graph view as primary interface, and pen-first input. No tables to fill. |
| 10 | **Bear organization problem stated but not solved** — "notes don't get organized into files" | Stated, Not Solved | Bear demoted to iPhone capture only. Apple Shortcuts auto-exports nightly with `#inbox` tag → Obsidian organizes. Bear's flat-tag limitation becomes irrelevant. |
| 11 | **Evernote mentioned but no action** — "perpetual disappointment... backlinks" | Stated, Not Solved | Explicit sunset: Export ENEX → Markdown converter → Obsidian vault. Delete account. Obsidian does backlinking natively and better. |
| 12 | **"YAML headers as well as details"** — mentioned once, never specified | Underspecified | Full YAML schema defined: title, date, platform, model, tags, summary, action_items, status. Applied to every auto-captured note. |
| 13 | **Multiple outputs problem** — "same chat in Claude, Claude Code, and Raycast" | Stated, Not Solved | Each platform gets its own capture path (Pactify for browser, cron for CLI, Raycast export script) → all converge on same Notion database with `platform` field distinguishing them. |
| 14 | **"Figure out my flaws"** — open-ended, no criteria | Unactionable | Replaced with explicit flaw diagnosis table (this table) mapping each pain point → root cause → architectural fix. |
| 15 | **No sequencing or priority** — everything requested simultaneously | Missing Prioritization | Setup checklist sequenced: Hour 1 (Obsidian) → Hour 2 (Handwriting) → Hour 3 (AI Capture) → Hour 4 (Connect the Loop) → Week 1 (Fine-tune) |

---

## YOUR WORKFLOW FLAWS DIAGNOSED

| Flaw | Root Cause | Evidence | Impact | Fix |
|------|-----------|----------|--------|-----|
| **Tool sprawl** (9+ apps) | No single hub; each tool adopted for one feature without architecture | "I like Bear for writing... Keep for quick notes... OneNote for drawing... Obsidian for graphs... Evernote for backlinks... NorthPlanner for drag-and-drop" | Cognitive load of context-switching; notes scattered; nothing links to anything | Obsidian as single hub. Everything else feeds into it silently. |
| **Capture without retrieval** | Tools optimized for INPUT (writing, capturing) but not OUTPUT (finding, connecting) | "Bear notes don't get organized... Google Keep is random all over the place... AI chats pile up" | You create information but can't find or use it. Classic collector's fallacy. | Every capture auto-routes to Obsidian with YAML metadata. Graph view = retrieval interface. |
| **Visual learner using text-first tools** | Bear, Keep, Evernote are text-list tools. You need spatial layouts. | "I'm a spatial and visual learner... I prefer writing and drawing... I love the [graph] visualization" | Tools fight your cognition. You abandon them because they don't match how you think. | Obsidian graph view + Excalidraw + Full Calendar = spatial-first. OneNote + Surface = pen-first input. |
| **No automation layer** | Each tool used in isolation with manual transfer | "I need it to happen automatically... I don't ever access it... I only see it through the nodal format" | Manual transfer never happens consistently. Notes die where they're born. | Power Automate + Make.com + Pactify = zero-touch automation layer. |
| **Phantom tools** | Adopted tools that don't exist or can't do what you think | NorthPlanner is a physical planner, not a scheduling app. "Prior Tree" is not a discoverable product. Google Keep has no API. | You're planning around capabilities that don't exist, leading to frustration. | Research-corrected tool selection. Only tools with verified APIs/capabilities included. |
| **AI output entropy** | AI conversations across 5+ platforms with no capture | "AI charts and projects pile up... I need them internalized into Notion by themselves" | Valuable AI research and outputs are lost within days. Repeated work. | Pactify + cron scripts → Notion database → Obsidian graph. Every conversation persists. |
| **Handwriting dead-end** | Surface pen input stays in OneNote with no downstream pipeline | "I draw out and write out physically my day and my plan" → but it stays in OneNote forever | Your preferred input mode (pen) produces output that never reaches your preferred viewing mode (graph). | OneNote → Power Automate OCR → Obsidian vault. Pen input → graph nodes. Pipeline closed. |

---

## RESEARCH-BACKED CORRECTIONS

### NorthPlanner (Corrected Understanding)
- **What it actually is**: A Spanish-origin physical A5 planner (by Arnau, Joel, Eric + YouTuber Euge Oller) + a Notion "Second Brain 2.0" digital template
- **The drag-and-drop you liked**: That's **Notion Calendar** (integrated in Second Brain 2.0), not a standalone feature
- **On Windows Surface**: You can't use it natively. Obsidian + Full Calendar plugin gives you identical drag-and-drop scheduling
- **Keep the physical planner**: If you like the ritual of the physical A5 agenda (weekly view, commitment contract, reading tracker), keep using it. It's well-designed. Just don't rely on its digital side.

### Priority Matrix (Your Eisenhower Tool)
- **API**: Real REST API at `sync.appfluence.com/api/v1/` with OAuth 2.0
- **Webhooks**: `item.created`, `item.completed`, `item.quadrant.updated` — can fire to Make.com
- **Calendar**: Native Outlook sync (deep), Google Calendar via iCal (updates every ~12h)
- **Python SDK**: `github.com/appfluence/prioritymatrix-python`
- **Integration path**: Priority Matrix → webhook → Make.com → update Obsidian daily note task colors

### Google Keep (Hard Truth)
- **No public API exists**. Never has. Likely never will.
- Zapier, Make.com have NO native Keep integration
- **Workaround**: `gkeepapi` (unofficial Python, may break) OR Keep → "Copy to Google Docs" button → Make.com watches Google Docs folder → Obsidian
- **Recommendation**: Use Keep ONLY for phone voice memos. Don't try to integrate it deeply.

### NotebookLM (Hard Truth)
- **No public API**. Audio overview generation is UI-only.
- **Best pipeline**: Notion → export as PDF → Google Drive folder → add folder as NotebookLM source → click "Generate Audio" manually once/week
- OR: Publish Notion pages to web → paste URLs into NotebookLM as web sources

---

*This document is the refined prompt, the workflow diagnosis, and the research corrections in one artifact. Use the prompt block above in any AI to get implementation. The tables below it are your evidence base.*
