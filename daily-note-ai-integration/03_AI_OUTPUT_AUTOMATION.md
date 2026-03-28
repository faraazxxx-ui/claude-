# AI Output Automation — Capture, Process, Visualize

---

## Overview

Every AI conversation you have is automatically captured, structured, stored, and made visible in your Obsidian graph — without you ever opening Notion.

---

## YAML Schema for AI Outputs

Every captured AI conversation gets this frontmatter:

```yaml
---
title: "{{conversation_title}}"
date: {{capture_date}}
time: {{capture_time}}
source: "{{platform}}"  # claude | chatgpt | grok | gemini | raycast
session_type: "{{type}}"  # chat | code | research | brainstorm
model: "{{model_name}}"  # e.g., claude-opus-4-6, gpt-4o, gemini-2.5
tags:
  - ai-output
  - "{{auto_generated_topic_tag_1}}"
  - "{{auto_generated_topic_tag_2}}"
project: "[[{{linked_project_or_none}}]]"
status: unreviewed  # unreviewed | reviewed | actionable | archived
key_outputs:
  - "{{summary_point_1}}"
  - "{{summary_point_2}}"
  - "{{summary_point_3}}"
action_items:
  - task: "{{action_1}}"
    priority: "{{Q1|Q2|Q3|Q4}}"
  - task: "{{action_2}}"
    priority: "{{Q1|Q2|Q3|Q4}}"
word_count: {{word_count}}
notebooklm_queued: false
---
```

---

## Capture Methods by Platform

### Verified Chrome Extensions (AI → Notion)

| Tool | Platforms Supported | Method | Auto-sync? |
|------|-------------------|--------|------------|
| **Pactify** (pactify.io) | ChatGPT, Claude, Gemini | Chrome extension, auto on visit | Yes — 540x faster than manual, 97%+ formatting accuracy |
| **Chat to Notion** (open-source) | ChatGPT, Deepseek, Claude, Mistral | Chrome extension | ChatGPT auto-sync, others manual |
| **AI Exporter Hub** | ChatGPT, Gemini, Claude, Perplexity, Grok | Chrome extensions | Varies |
| **ClaudeAI to Notion** | Claude only | Chrome extension | Manual trigger |
| **Save ChatGPT to Notion** | ChatGPT only | Chrome extension | Yes (1-24hr intervals) |

**Recommended**: Install **Pactify** for broadest coverage + auto-sync. Fall back to **Chat to Notion** (open-source, no third-party data sharing) for privacy-sensitive conversations.

### Claude (claude.ai)
- **Primary**: Pactify or ClaudeAI to Notion Chrome extension
- **Alternative**: Claude conversation sharing → webhook → n8n

### Claude Code (CLI)
- **Method**: Session logs stored locally at `~/.claude/projects/`
- **Script**: File system watcher (chokidar/watchman) or nightly cron
- **Pipeline**: Watch for new session files → extract → format with YAML → push to Notion API

### ChatGPT
- **Primary**: Pactify (auto-sync on visit) or Chat to Notion (open-source)
- **Alternative**: Save ChatGPT to Notion (1-24hr auto-sync intervals)

### Grok (x.ai)
- **Primary**: AI Exporter Hub Chrome extension (supports Grok)
- **Fallback**: Tampermonkey userscript to capture conversation DOM → n8n webhook

### Gemini
- **Primary**: Pactify or AI Exporter Hub Chrome extension
- **Alternative**: Google Takeout (bulk export) → Google Drive → Make.com → Notion

### Raycast AI
- **Method**: Raycast stores conversation history locally
- **Path**: `~/Library/Application Support/com.raycast.macos/` (macOS)
- **Trigger**: File watcher on Raycast data directory → n8n webhook

---

## n8n Workflow Specification

### Workflow: "AI Output Processor"

```
Node 1: Webhook Trigger
  - Type: Webhook
  - Method: POST
  - Path: /ai-capture
  - Authentication: Header Auth (API key)
  - Accepts: JSON body with { platform, content, url, timestamp }

Node 2: Text Processor (Code Node)
  - Extract title (first line or first 50 chars)
  - Count words
  - Extract any URLs, code blocks, action items (regex for "TODO", "Action:", numbered lists)
  - Auto-generate topic tags (keyword extraction)

Node 3: AI Summarizer (HTTP Request to Claude API)
  - Endpoint: https://api.anthropic.com/v1/messages
  - Prompt: "Summarize this AI conversation in 3 bullet points. Extract action items. Suggest 2-3 topic tags."
  - Model: claude-haiku-4-5 (fast + cheap for summarization)

Node 4: YAML Builder (Code Node)
  - Construct YAML frontmatter from Node 2 + Node 3 outputs
  - Format full markdown document

Node 5: Notion Create Page
  - Type: Notion API
  - Database: "AI Outputs" database
  - Properties mapped from YAML fields
  - Content: Full conversation markdown

Node 6: Obsidian File Writer (via WebDAV or local file system)
  - Write markdown file to: vault/AI/{{date}}-{{platform}}-{{slug}}.md
  - Include YAML frontmatter for Obsidian Dataview queries

Node 7: NotebookLM Queue (Conditional)
  - If action_items.length > 0 OR word_count > 500
  - Add to Google Drive folder that NotebookLM monitors
  - Flag notebooklm_queued: true
```

---

## NotebookLM Integration

> **CRITICAL LIMITATION**: NotebookLM has **NO public API**. It cannot be triggered programmatically. All automation ends at pushing files to a Google Drive folder — you must manually open NotebookLM to generate Audio Overviews. This is a hard constraint from Google as of March 2026.

### How It Works (Semi-Automated)
1. A Google Drive folder called `AI-Digests/` is the NotebookLM source
2. n8n pushes weekly digest documents to this folder every Sunday (automated)
3. You open NotebookLM once per week and click "Generate Audio Overview" (manual — ~30 seconds)
4. NotebookLM generates:
   - Audio overview (podcast-style summary with two AI hosts)
   - Formats: Deep Dive, Brief, Critique, or Debate mode
   - Interactive Audio: you can "raise hand" to interrupt and ask questions
   - Also: Video Overviews, Infographics, Mind Maps (added 2025)
   - Supports 80+ languages, up to 50 sources (free) or 300 (pro)
5. **Weekly trigger reminder**: n8n sends you a Sunday notification: "Your AI digest is ready in NotebookLM — tap to generate audio"

### Weekly Digest Template
```markdown
# AI Weekly Digest — Week of {{week_start_date}}

## Conversations This Week: {{count}}

### By Platform
- Claude: {{claude_count}}
- ChatGPT: {{chatgpt_count}}
- Grok: {{grok_count}}
- Gemini: {{gemini_count}}

### Top Topics
1. {{topic_1}} ({{count_1}} conversations)
2. {{topic_2}} ({{count_2}} conversations)
3. {{topic_3}} ({{count_3}} conversations)

### Key Action Items (Unresolved)
- [ ] {{action_1}} — from {{source_conversation}}
- [ ] {{action_2}} — from {{source_conversation}}
- [ ] {{action_3}} — from {{source_conversation}}

### Conversation Summaries
{{#each conversations}}
#### {{this.title}} ({{this.platform}} — {{this.date}})
{{this.summary}}
Action items: {{this.action_items}}
{{/each}}
```

---

## Notion Database Schema (Invisible Backend)

### Database: "AI Outputs"

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | Conversation title |
| Date | Date | Capture timestamp |
| Platform | Select | claude / chatgpt / grok / gemini / raycast |
| Session Type | Select | chat / code / research / brainstorm |
| Model | Text | Model identifier |
| Tags | Multi-select | Auto-generated topics |
| Project | Relation | Links to Projects database |
| Status | Select | unreviewed / reviewed / actionable / archived |
| Key Outputs | Rich Text | 3-point summary |
| Action Items | Rich Text | Extracted tasks |
| Word Count | Number | Conversation length |
| NotebookLM Queued | Checkbox | Whether it's been sent to NotebookLM |
| Obsidian Synced | Checkbox | Whether markdown was written to vault |
| Full Content | Rich Text | Complete conversation |
| Source URL | URL | Link back to original conversation |

### Database: "Projects"

| Property | Type | Purpose |
|----------|------|---------|
| Name | Title | Project name |
| Status | Select | active / paused / complete |
| AI Outputs | Relation | Back-relation to AI Outputs |
| Tags | Multi-select | Topic tags |
| Priority | Select | Q1 / Q2 / Q3 / Q4 |
| Obsidian Link | Text | `[[Project Name]]` for cross-reference |
