# Workflow Architecture Reference

## System Overview

The Daily Workflow Optimizer unifies a fragmented note-taking ecosystem into a three-layer architecture:

```
INPUT LAYER          PROCESSING LAYER         OUTPUT LAYER
─────────────        ─────────────────        ────────────
Surface Pen ──┐                               ┌── Obsidian Graph
OneNote ──────┤      ┌─────────────┐          ├── NotebookLM Audio
Whiteboard ───┤      │   Notion    │          ├── Bear (Writing)
Bear ─────────┼─────>│  (Backend   │─────────>├── Daily Note .md
Google Keep ──┤      │   Database) │          ├── Google Calendar
AI Outputs ───┤      └─────────────┘          └── Eisenhower Matrix
Claude/Grok ──┘           ▲
                          │
                    Automation Layer
                    (Make/Zapier/Scripts)
```

## Tool Role Assignments

| Tool | Role | Why |
|------|------|-----|
| Microsoft OneNote / Whiteboard | Visual Input | Surface pen, spatial planning |
| Bear | Writing Input | Clean writing experience |
| Google Keep | Quick Capture | Fast mobile capture |
| Notion | Backend Database | Structured storage, API, never accessed directly |
| Obsidian | Visualization | Graph view, node connections |
| NotebookLM | Audio Review | Audio overviews of aggregated content |
| Google Calendar | Scheduling | Event sync, Eisenhower integration |
| Priority Matrix / NotePlan | Task Priority | Eisenhower matrix + calendar drag-drop |

## Automation Flows

### Flow 1: Handwriting → Daily Note
1. User draws/writes daily plan on Surface (OneNote/Whiteboard)
2. Export as image (.png)
3. `handwriting_to_daily_note.py` runs OCR (Tesseract)
4. Classified text maps to daily note sections
5. Output: Markdown daily note in Obsidian vault

### Flow 2: AI Outputs → Notion
1. User completes AI chat (Claude, Grok, ChatGPT, Gemini)
2. Export chat or use browser extension
3. `ai_to_notion.py` creates Notion page with YAML frontmatter
4. Properties: source, date, topic, tags
5. Notion database serves as searchable archive

### Flow 3: Notion → Obsidian Graph
1. Notion database synced to Obsidian vault (obsidian-notion-sync)
2. Each AI output becomes a linked note
3. Obsidian graph view shows connections
4. Juggl plugin enhances visual exploration

### Flow 4: Notion → NotebookLM
1. Export Notion pages as Google Docs (via Notion API)
2. Feed into NotebookLM as sources
3. Generate audio overviews
4. Review via NotebookLM interface

## Notion Database Schema

```
AI Outputs Database
├── Name (title): "[SOURCE] Topic Title"
├── Source (select): claude | grok | chatgpt | gemini | claude-code | raycast
├── Date (date): YYYY-MM-DD
├── Topic (rich_text): Description
├── Timestamp (rich_text): ISO 8601
├── Tags (multi_select): project tags
└── Content (page body): Full chat output with YAML header block
```

## Recommended Obsidian Plugins

| Plugin | Stars | Purpose |
|--------|-------|---------|
| Templater | 5.5k | Daily note template automation |
| Calendar | 3.5k | Calendar view for daily notes |
| Juggl | 1.9k | Enhanced interactive graph view |
| ExcaliBrain | 1.8k | Visual mind-map from notes |
| Obsidian Git | 4.5k | Version control and backup |
| Dataview | 10k+ | Query notes like a database |

## Google Keep Integration

Use `gkeepapi` (1.7k stars) to:
1. Pull quick captures from Google Keep
2. Auto-categorize into daily note sections
3. Archive processed notes in Keep
