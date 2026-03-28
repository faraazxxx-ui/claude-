# Daily Workflow Optimizer

**A comprehensive, four-skill execution that analyzes, optimizes, and automates a fragmented note-taking ecosystem for a visual/spatial learner.**

This deliverable was produced by executing four Manus skills in parallel:

| Skill | Purpose | Output |
|-------|---------|--------|
| `/prompt-optimizer` | Rewrite the raw prompt for 10 AI platforms | `prompts/` directory |
| `/github-gem-seeker` | Find battle-tested open-source tools | `research_data.csv` |
| `/skill-creator` | Package the workflow as a reusable Manus skill | `SKILL.md` |
| `/gws-best-practices` | Google Workspace integration guidance | Embedded in workflow |

---

## Table of Contents

1. [Workflow Diagnosis](#1-workflow-diagnosis)
2. [Proposed System Architecture](#2-proposed-system-architecture)
3. [GitHub Gems Discovered](#3-github-gems-discovered)
4. [Daily Note Template](#4-daily-note-template)
5. [Automation Scripts](#5-automation-scripts)
6. [Optimized Prompts for 10 Platforms](#6-optimized-prompts-for-10-platforms)
7. [Implementation Roadmap](#7-implementation-roadmap)

---

## 1. Workflow Diagnosis

Your current system suffers from **tool fragmentation without integration**. Each tool excels at one thing but operates in isolation, creating cognitive overhead and information loss.

### Identified Flaws

| Flaw | Tool | Impact |
|------|------|--------|
| No single source of truth | All tools | Information scattered across 8+ apps |
| Capture without organization | Bear | Every note becomes a new, disconnected entry |
| Visualization without usability | Obsidian | Graph view is powerful but tool complexity is a barrier |
| Integration without depth | Google Keep | Quick capture but no structured workflow |
| Drag-and-drop without understanding | North Plan | Appealing UX but unclear mental model |
| AI outputs without archival | Claude/Grok/Gemini | Chat outputs pile up without structure |
| Physical input without digital bridge | Surface/OneNote | Handwritten plans stay analog |
| Priority system without automation | Eisenhower Matrix | Manual transfer to calendar |

### Root Cause

The core problem is not the tools themselves but the absence of an **automated processing layer** between input and output. You capture information in many places but have no system to funnel it into a unified, searchable, visualizable format.

---

## 2. Proposed System Architecture

```
INPUT LAYER              PROCESSING LAYER           OUTPUT LAYER
─────────────            ─────────────────           ────────────
Surface Pen ──┐                                     ┌── Obsidian Graph View
OneNote ──────┤          ┌─────────────┐            ├── NotebookLM Audio
Whiteboard ───┤          │   Notion    │            ├── Bear (Writing)
Bear ─────────┼─────────>│  (Backend   │───────────>├── Daily Note .md
Google Keep ──┤          │   Database) │            ├── Google Calendar
AI Outputs ───┤          └─────────────┘            └── Eisenhower Matrix
Claude/Grok ──┘               ▲
                               │
                         Automation Layer
                      (Scripts / Make / Zapier)
```

### Tool Role Assignments

| Tool | Assigned Role | Rationale |
|------|---------------|-----------|
| **OneNote / Whiteboard** | Visual Input | Surface pen, spatial planning, drawing |
| **Bear** | Writing Input | Clean, distraction-free writing |
| **Google Keep** | Quick Capture | Fast mobile/desktop capture |
| **Notion** | Backend Database | Structured storage, API-driven, never accessed directly |
| **Obsidian** | Visualization | Graph view, Juggl plugin, node connections |
| **NotebookLM** | Audio Review | Audio overviews of aggregated AI content |
| **Google Calendar** | Scheduling | Event sync, Eisenhower integration |
| **NotePlan / Priority Matrix** | Task Priority | Eisenhower matrix + calendar drag-drop |

### Key Principle

> You never touch Notion directly. It serves as the invisible backend. You interact with your system through Obsidian (visual), Bear (writing), NotebookLM (audio), and your Surface (handwriting).

---

## 3. GitHub Gems Discovered

The parallel research identified these battle-tested open-source tools:

### Handwriting Recognition

| Tool | Stars | URL | Use Case |
|------|-------|-----|----------|
| SimpleHTR | 2.2k | [github.com/githubharald/SimpleHTR](https://github.com/githubharald/SimpleHTR) | Handwriting-to-text recognition |
| handwriting-ocr | 829 | [github.com/breta01/handwriting-ocr](https://github.com/breta01/handwriting-ocr) | Full OCR pipeline |
| Windows Ink API | N/A | [Microsoft Docs](https://github.com/MicrosoftDocs/windows-dev-docs) | Native Surface pen recognition |

### Note Automation and Sync

| Tool | Stars | URL | Use Case |
|------|-------|-----|----------|
| gkeepapi | 1.7k | [github.com/kiwiz/gkeepapi](https://github.com/kiwiz/gkeepapi) | Google Keep API automation |
| nobsidion | 98 | [github.com/quanphan2906/nobsidion](https://github.com/quanphan2906/nobsidion) | Notion-to-Obsidian sync |
| obsidian-notion-sync | 37 | [github.com/Akash-Sharma-1/obsidian-notion-sync](https://github.com/Akash-Sharma-1/obsidian-notion-sync) | Bidirectional sync |

### Obsidian Plugins for Visual Learners

| Plugin | Stars | URL | Use Case |
|--------|-------|-----|----------|
| Templater | 5.5k | [github.com/SilentVoid13/Templater](https://github.com/SilentVoid13/Templater) | Daily note template automation |
| Juggl | 1.9k | [github.com/HEmile/juggl](https://github.com/HEmile/juggl) | Interactive graph exploration |
| ExcaliBrain | 1.8k | [github.com/zsviczian/excalibrain](https://github.com/zsviczian/excalibrain) | Mind-map visualization |
| Calendar | 3.5k | Community plugins | Calendar-based note navigation |
| Obsidian Git | 4.5k | Community plugins | Version control and backup |

### AI Output Aggregation

| Tool | Stars | URL | Use Case |
|------|-------|-----|----------|
| chatgpt-to-notion | 400+ | [github.com/L-a-r-t/chatgpt-to-notion](https://github.com/L-a-r-t/chatgpt-to-notion) | ChatGPT to Notion pipeline |
| ai-chat-exporter | 100+ | [github.com/revivalstack/ai-chat-exporter](https://github.com/revivalstack/ai-chat-exporter) | Multi-platform AI export |
| notionary | 16 | [github.com/mathisarends/notionary](https://github.com/mathisarends/notionary) | Notion API Python wrapper |

---

## 4. Daily Note Template

The template is located at [`templates/daily-note-template.md`](templates/daily-note-template.md). It is Obsidian-compatible with Dataview queries and includes:

- **Yesterday's Wins** (3 reflection points)
- **Areas for Improvement** (3 reflection points)
- **Today's Goals** (3 checkbox tasks, Eisenhower-prioritized)
- **Today's Events** (table format with time/event/location)
- **Quick Capture** (dump zone, auto-sorted by automation)
- **AI Project Notes** (auto-populated via Dataview from Notion sync)
- **Linked Notes** (auto-generated backlinks from Obsidian graph)

---

## 5. Automation Scripts

### `scripts/ai_to_notion.py`

Captures AI chat outputs and creates structured Notion pages with YAML frontmatter.

```bash
# Setup
export NOTION_API_KEY="your_token"
export NOTION_DB_ID="your_database_id"

# Usage
python3 scripts/ai_to_notion.py \
  --source claude \
  --topic "Project Discussion" \
  --file /path/to/exported_chat.md \
  --tags project-x research
```

Supported sources: `claude`, `grok`, `chatgpt`, `gemini`, `claude-code`, `raycast`

### `scripts/handwriting_to_daily_note.py`

Converts handwritten notes from Surface/OneNote exports into structured daily notes.

```bash
# Setup
pip install Pillow pytesseract
sudo apt install tesseract-ocr

# Usage
python3 scripts/handwriting_to_daily_note.py \
  --image /path/to/handwritten_note.png \
  --output ~/obsidian-vault/daily/2026-03-28.md
```

---

## 6. Optimized Prompts for 10 Platforms

Each prompt in the `prompts/` directory is tailored to a specific AI platform's native format, optimization rules, and anti-patterns. See the individual files for copy-paste-ready prompts.

| Platform | File | Format DNA |
|----------|------|------------|
| Manus AI | `prompts/01_manus.md` | Goal + Requirements + Deliverable + Verification |
| Claude Chat | `prompts/02_claude_chat.md` | XML tags: context + instructions + output_format |
| Claude Co-work | `prompts/03_claude_cowork.md` | Goal + Inputs + Output + Quality Criteria |
| Claude Code | `prompts/04_claude_code.md` | Problem + Files + Test + Verify |
| Grok Heavy | `prompts/05_grok_heavy.md` | Role + data_sources + task + output + failure_policy |
| Perplexity Pro | `prompts/06_perplexity_pro.md` | One question + focus + sources + anti-hallucination |
| Perplexity Computer | `prompts/07_perplexity_computer.md` | End-state project + requirements + deliverable |
| Comet Agent | `prompts/08_comet_agent.md` | Task + numbered steps + completion criterion |
| Claude on Chrome | `prompts/09_claude_chrome.md` | instructions + steps + SAFETY (mandatory) |
| Gemini Browser | `prompts/10_gemini_browser.md` | role + constraints + context + task + final_instruction |

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Day 1)
1. Create a dedicated Notion workspace with the "AI Knowledge Base" database
2. Install Obsidian and configure the daily note template with Templater
3. Install Juggl and ExcaliBrain plugins for graph visualization

### Phase 2: Automation (Day 2-3)
4. Set up `ai_to_notion.py` with your Notion API key
5. Install the chatgpt-to-notion browser extension for real-time capture
6. Configure `handwriting_to_daily_note.py` with Tesseract OCR

### Phase 3: Integration (Day 4-5)
7. Set up nobsidion or obsidian-notion-sync for Notion-to-Obsidian sync
8. Configure gkeepapi to pull Google Keep quick captures into daily notes
9. Connect NotebookLM to your Notion exports via Google Drive

### Phase 4: Calendar and Priority (Day 6-7)
10. Set up NotePlan or Priority Matrix for Eisenhower matrix + calendar
11. Configure Google Calendar sync with your daily note events
12. Test the full pipeline: handwriting to daily note to Obsidian graph

---

## File Structure

```
daily-workflow-optimizer/
├── README.md                          # This file
├── SKILL.md                           # Reusable Manus skill definition
├── research_data.csv                  # Raw parallel research data
├── scripts/
│   ├── ai_to_notion.py                # AI chat → Notion automation
│   └── handwriting_to_daily_note.py   # Handwriting OCR → daily note
├── templates/
│   └── daily-note-template.md         # Obsidian-compatible daily note
├── references/
│   └── workflow-architecture.md       # Full system architecture docs
└── prompts/
    ├── 01_manus.md
    ├── 02_claude_chat.md
    ├── 03_claude_cowork.md
    ├── 04_claude_code.md
    ├── 05_grok_heavy.md
    ├── 06_perplexity_pro.md
    ├── 07_perplexity_computer.md
    ├── 08_comet_agent.md
    ├── 09_claude_chrome.md
    └── 10_gemini_browser.md
```
