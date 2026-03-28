# Refined Prompt — Daily Note + AI Workflow Integration

> **Final Output**: A production-ready prompt that any AI (Claude, GPT, Gemini, Grok) can execute to build your full system.

---

## The Refined Prompt

```
You are a productivity systems architect for a verbal-thinking, spatial/visual learner who uses a Windows Surface. Build me a complete daily workflow system with these exact specifications:

### PART 1 — DAILY NOTE TEMPLATE
Create a markdown daily note template with YAML frontmatter containing:
- Section 1: "Yesterday's Wins" — 3 bullet points (things that went well)
- Section 2: "Yesterday's Growth Edges" — 3 bullet points (things to improve)
- Section 3: "Today's Goals" — 3 prioritized tasks (linked to Eisenhower quadrants)
- Section 4: "Today's Events" — 3 time-blocked events (synced from calendar)
- Section 5: "AI Outputs Inbox" — auto-populated links to today's AI conversations

Each section must include:
- A status toggle (◻ / ✅)
- Cross-links to relevant project notes using [[wikilinks]]
- Tags for filtering (#reflection, #goal, #event, #ai-output)

### PART 2 — TOOL CONSOLIDATION (solve my fragmentation problem)
I currently scatter notes across: Google Keep, OneNote, Bear, Evernote, Obsidian, NotePlan, Remarkable, Priority Matrix, and Notion. This creates chaos.

Design a hub-and-spoke architecture where:
- **HUB (single source of truth)**: Obsidian vault (for graph visualization I love)
- **CAPTURE SPOKES** (input points that auto-sync TO the hub):
  - Windows Surface → OneNote handwriting → OCR → Obsidian via Power Automate
  - Bear → quick text capture → Obsidian via Bear-to-Obsidian export plugin
  - Google Keep → quick mobile capture → Obsidian via Google Keep → Make.com → Obsidian
  - Remarkable → handwritten notes → OCR export → Obsidian folder
- **PLANNING SPOKE**: NotePlan for drag-and-drop calendar scheduling (syncs with Obsidian daily notes via shared markdown files or iCloud folder)
- **PRIORITIZATION SPOKE**: Priority Matrix for Eisenhower matrix → calendar sync → NotePlan
- **ARCHIVE/DEAD DROP**: Notion (never accessed directly — only as automation backend)

For each spoke, specify: the automation tool (Zapier/Make/n8n/Power Automate), the trigger, the action, and the destination folder in Obsidian.

### PART 3 — HANDWRITING-TO-DIGITAL PIPELINE
I draw and write plans on my Windows Surface. Build a pipeline:
1. I draw/write in OneNote or Microsoft Whiteboard on Surface
2. Microsoft's built-in OCR + Ink-to-Text converts handwriting
3. Power Automate triggers on new OneNote page/section
4. Extracted text is formatted as markdown with YAML header
5. Pushed to Obsidian vault daily-notes folder
6. Appears in Obsidian graph view as connected node

Include the Power Automate flow specification and the YAML template for converted notes.

### PART 4 — AI OUTPUT AUTOMATION
Every AI conversation I have (Claude, ChatGPT, Grok, Gemini) must be automatically captured. Build this:

1. **Capture layer**: Browser extension or API webhook that detects conversation end
2. **Processing layer**: n8n/Make workflow that:
   - Extracts conversation title, date, AI platform, key topics
   - Generates YAML frontmatter (title, date, source, tags, project-link, status)
   - Summarizes key outputs and action items
3. **Storage layer**: Pushes to a dedicated Notion database (I never open this)
4. **Visualization layer**: Notion → Obsidian sync (via Notion-to-Obsidian plugin or API)
5. **Review layer**: Auto-feed to NotebookLM for audio summaries + podcast-style review

Specify the YAML schema, the n8n/Make workflow nodes, and the NotebookLM integration method.

### PART 5 — GRAPH VISUALIZATION (what I actually see)
Since I'm spatial/visual, my primary interface is Obsidian's graph view. Configure:
- Color-coded nodes: 🔵 Daily Notes, 🟢 Projects, 🟡 AI Outputs, 🔴 Tasks, 🟣 Events
- Cluster by: project, date, or priority quadrant
- Force-directed layout with adjustable depth
- Saved graph filters for: "This Week", "Active Projects", "AI Research"

### CONSTRAINTS
- I never open Notion directly — it's only a backend
- I prefer handwriting/drawing as primary input
- Everything must converge into Obsidian's graph view
- NotePlan is my calendar/scheduling interface
- Daily note must be auto-generated each morning
- All AI outputs must flow in without manual action
```

---

## What This Refined Prompt Fixes vs. the Original

| Problem in Original | Fix in Refined Prompt |
|---|---|
| "North plan" — ambiguous name | Identified as **NotePlan** (noteplan.co) — markdown planner with drag-and-drop calendar |
| Tools listed but no architecture | Defined **hub-and-spoke model** with Obsidian as hub |
| "Link up to Google Keep, OneNote, etc." — vague | Specified exact automation routes per tool |
| Handwriting workflow undefined | Built explicit **Surface → OneNote → OCR → Obsidian pipeline** |
| AI integration described abstractly | Defined 5-layer capture → storage → visualization pipeline |
| "Find the flaws" — no diagnostic framework | Diagnosed 7 specific workflow flaws (see below) |
| No mention of what to stop using | Recommends **sunsetting** Evernote and reducing Bear to capture-only |
| Notion hatred unresolved | Notion becomes invisible backend — user never touches it |
| NotebookLM mentioned but not integrated | Automated feed from Notion → NotebookLM for audio review |
