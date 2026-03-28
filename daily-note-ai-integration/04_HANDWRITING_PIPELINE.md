# Handwriting-to-Digital Pipeline — Surface → Obsidian

---

## Overview

You draw and write on your Windows Surface. This pipeline converts your handwriting into structured markdown notes that appear in your Obsidian graph.

---

## Pipeline Steps

```
Surface Pen → OneNote/Whiteboard
       ↓
OneNote Ink-to-Text (built-in OCR)
       ↓
Power Automate (trigger: new/modified page)
       ↓
Format as Markdown + YAML frontmatter
       ↓
Save to Obsidian vault folder (OneDrive/local sync)
       ↓
Obsidian graph view shows new node
```

---

## Step 1: Write/Draw on Surface

**Where**: OneNote (for structured notes) or Microsoft Whiteboard (for freeform spatial planning)

**Tips for best OCR results**:
- Write clearly but naturally — OneNote's OCR handles cursive reasonably well
- Use OneNote's built-in "Ink to Text" button for manual conversion
- Separate drawings from text in different areas of the page
- Use page titles — these become your note titles

---

## Step 2: Power Automate Flow

### Flow: "OneNote to Obsidian"

```
Trigger: "When a page is updated in OneNote"
  - Notebook: [Your Daily Planning Notebook]
  - Section: [Daily Notes] or [All Sections]

Action 1: "Get page content" (OneNote connector)
  - Returns HTML content with converted text

Action 2: "Compose" (Data Operations)
  - Convert HTML to plain text
  - Strip OneNote-specific tags
  - Expression: replace(replace(body('Get_page_content'), '<[^>]+>', ''), '&nbsp;', ' ')

Action 3: "Compose" (Build YAML + Markdown)
  - Template:
    ---
    title: "@{triggerOutputs()?['body/title']}"
    date: @{formatDateTime(utcNow(), 'yyyy-MM-dd')}
    source: onenote-surface
    type: handwritten
    tags:
      - handwritten
      - surface
      - ocr
    status: unreviewed
    ---

    # @{triggerOutputs()?['body/title']}

    ## Converted Text
    @{outputs('Compose')}

    ## Original
    *Handwritten in OneNote on Surface — [view original](onenote:link)*

Action 4: "Create file" (OneDrive/SharePoint connector)
  - Folder: /ObsidianVault/00-Inbox/Surface/
  - File name: @{formatDateTime(utcNow(), 'yyyy-MM-dd')}-surface-@{triggerOutputs()?['body/title']}.md
  - Content: Output from Action 3

Action 5 (Optional): "Send notification" (Teams/Email)
  - "New handwritten note converted: [title]"
```

---

## Step 3: Whiteboard Drawings

For Microsoft Whiteboard spatial planning:

1. **Export**: Whiteboard → Export as PNG/SVG
2. **Power Automate trigger**: New file in Whiteboard export folder
3. **Action**: Copy image to `ObsidianVault/Attachments/Whiteboard/`
4. **Action**: Create markdown note:
   ```markdown
   ---
   title: "Whiteboard — {{date}}"
   type: whiteboard
   tags: [spatial, drawing, planning]
   ---
   # Whiteboard — {{date}}
   ![[Whiteboard/{{filename}}]]
   ```
5. Image embeds in Obsidian and appears as a node in graph

---

## Step 4: Remarkable Integration

If using Remarkable tablet:

1. **Remarkable → Connect app** exports PDFs/PNGs to cloud
2. **Google Drive / Dropbox sync** catches exported files
3. **Make.com workflow**:
   - Trigger: New file in Remarkable exports folder
   - Action: OCR via Google Cloud Vision API or Azure Computer Vision
   - Action: Format as markdown + YAML
   - Action: Save to Obsidian vault

---

## Obsidian Plugin Requirements

Install these Obsidian community plugins:

| Plugin | Purpose |
|--------|---------|
| **Templater** | Auto-generate daily notes with template variables |
| **Dataview** | Query and display notes as tables (e.g., "all unreviewed handwritten notes") |
| **Periodic Notes** | Daily/weekly/monthly note generation |
| **Calendar** | Calendar sidebar widget for navigating daily notes |
| **Excalidraw** | Draw directly in Obsidian (alternative to Whiteboard) |
| **Kanban** | Visual task boards within Obsidian |
| **Style Settings** | Customize graph view colors |
| **Graph Analysis** | Enhanced graph features — clusters, filters |
| **Obsidian Git** | Auto-backup vault to GitHub |
| **Notion-Like Tables** | Better table editing UX |

---

## Obsidian Graph View Configuration

### Custom CSS for Color-Coded Nodes

Add to `.obsidian/snippets/graph-colors.css`:

```css
/* Daily Notes — Blue */
.graph-view .node[data-path^="Daily/"] {
  fill: #4A90D9;
}

/* AI Outputs — Yellow */
.graph-view .node[data-path^="AI/"] {
  fill: #F5A623;
}

/* Projects — Green */
.graph-view .node[data-path^="Projects/"] {
  fill: #7ED321;
}

/* Handwritten/Surface — Purple */
.graph-view .node[data-path^="00-Inbox/Surface/"] {
  fill: #9B59B6;
}

/* Events — Red */
.graph-view .node[data-tag="event"] {
  fill: #D0021B;
}
```

### Vault Folder Structure

```
ObsidianVault/
├── 00-Inbox/
│   ├── Surface/          ← OneNote handwriting conversions
│   ├── Keep/             ← Google Keep captures
│   ├── Bear/             ← Bear exports
│   └── Remarkable/       ← Remarkable exports
├── Daily/                ← Daily notes (auto-generated)
├── Weekly/               ← Weekly reviews
├── Projects/             ← Project notes
├── AI/                   ← AI conversation archives
│   ├── Claude/
│   ├── ChatGPT/
│   ├── Grok/
│   └── Gemini/
├── Events/               ← Calendar events with notes
├── Templates/            ← Note templates
├── Attachments/
│   ├── Whiteboard/       ← Exported drawings
│   └── Images/
└── Archive/              ← Completed/old notes
```
