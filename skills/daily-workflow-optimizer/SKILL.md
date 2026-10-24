---
name: daily-workflow-optimizer
description: >
  Unified daily note system for visual/spatial learners with fragmented
  note-taking tools. Use when the user needs to: generate a structured daily
  note from handwritten input, auto-capture AI chat outputs to Notion,
  visualize notes in Obsidian graph view, sync across Bear/Keep/OneNote,
  or optimize a multi-tool productivity workflow. Also use when user mentions
  daily planning, handwriting-to-text, AI output aggregation, or Eisenhower
  matrix integration.
---

# Daily Workflow Optimizer

Unify a fragmented note-taking ecosystem into a three-layer system: visual input (Surface pen, Bear, Keep), automated processing (Notion backend), and optimized output (Obsidian graph, NotebookLM audio, calendar sync).

## When to Use

- User wants a structured daily note template
- User needs handwriting/drawing converted to digital notes
- User wants AI chat outputs (Claude, Grok, Gemini) auto-saved to Notion
- User needs to visualize notes in a graph/nodal format
- User struggles with too many disconnected note-taking tools

## Workflow

### Step 1: Generate Daily Note

Use the Obsidian-compatible template:

```bash
cp /home/ubuntu/skills/daily-workflow-optimizer/templates/daily-note-template.md \
   ~/obsidian-vault/daily/$(date +%Y-%m-%d).md
```

The template includes sections for: Yesterday's Wins (3), Areas for Improvement (3), Today's Goals (3), Today's Events (3), Quick Capture, and auto-populated AI Project Notes via Dataview.

### Step 2: Convert Handwritten Notes

For Surface/OneNote/Whiteboard handwritten exports:

```bash
pip install Pillow pytesseract
sudo apt install tesseract-ocr
python3 /home/ubuntu/skills/daily-workflow-optimizer/scripts/handwriting_to_daily_note.py \
  --image /path/to/handwritten_note.png \
  --output ~/obsidian-vault/daily/$(date +%Y-%m-%d).md
```

The script runs OCR, classifies text into daily note sections by keyword matching, and outputs structured Markdown.

### Step 3: Capture AI Outputs to Notion

Set environment variables first:

```bash
export NOTION_API_KEY="your_notion_integration_token"
export NOTION_DB_ID="your_database_id"
```

Then capture any AI chat output:

```bash
python3 /home/ubuntu/skills/daily-workflow-optimizer/scripts/ai_to_notion.py \
  --source claude \
  --topic "Project Discussion" \
  --file /path/to/exported_chat.md \
  --tags project-x research
```

Supported sources: `claude`, `grok`, `chatgpt`, `gemini`, `claude-code`, `raycast`.

Each Notion page includes a YAML frontmatter code block and structured properties (Source, Date, Topic, Tags, Timestamp).

### Step 4: Visualize in Obsidian

Install recommended plugins for visual/spatial learners:

| Plugin | Install Command | Purpose |
|--------|----------------|--------|
| Templater | Community plugins | Auto-generate daily notes |
| Juggl | Community plugins | Interactive graph exploration |
| ExcaliBrain | Community plugins | Mind-map visualization |
| Calendar | Community plugins | Calendar-based note navigation |
| Dataview | Community plugins | Query AI outputs from Notion sync |

### Step 5: Sync Notion to NotebookLM

For audio overviews of aggregated AI outputs:

1. Export Notion pages as Google Docs (Notion API to Google Drive)
2. Add Google Docs as NotebookLM sources
3. Generate audio overview for hands-free review

## Architecture Reference

For the full system diagram, tool role assignments, automation flows, and Notion database schema, consult:

```
/home/ubuntu/skills/daily-workflow-optimizer/references/workflow-architecture.md
```

## Key GitHub Gems Used

| Tool | Stars | Role |
|------|-------|------|
| SimpleHTR | 2.2k | Handwriting recognition |
| gkeepapi | 1.7k | Google Keep automation |
| Templater | 5.5k | Obsidian daily note templates |
| Juggl | 1.9k | Obsidian graph visualization |
| chatgpt-to-notion | 0.4k | AI chat to Notion pipeline |
| notionary | 16 | Notion API Python wrapper |
