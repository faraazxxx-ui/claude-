---
title: "Daily Note — {{date:YYYY-MM-DD}}"
date: {{date:YYYY-MM-DD}}
day: "{{date:dddd}}"
type: daily-note
status: active
tags:
  - daily
  - reflection
  - planning
links:
  weekly-review: "[[Weekly Review — {{date:YYYY-[W]ww}}]]"
  monthly-goals: "[[Monthly Goals — {{date:YYYY-MM}}]]"
integrations:
  noteplan-sync: true
  google-calendar: true
  priority-matrix: true
  ai-inbox: true
---

# {{date:dddd, MMMM D, YYYY}}

---

## 🔙 Yesterday's Wins
> *What went well? Anchor these — they're your momentum.*

- [ ] 1.
- [ ] 2.
- [ ] 3.

**Pattern link**: [[Wins Log]] | Tags: #reflection #wins

---

## 🔄 Yesterday's Growth Edges
> *Not failures — edges to sharpen. Be specific and actionable.*

- [ ] 1.
- [ ] 2.
- [ ] 3.

**Action**: Convert each edge into a micro-goal below or a [[Growth Tracker]] entry.
Tags: #reflection #improvement

---

## 🎯 Today's Goals
> *Max 3. Prioritized by Eisenhower quadrant. Drag these into NotePlan for time-blocking.*

| # | Goal | Quadrant | Time Block | Status |
|---|------|----------|------------|--------|
| 1 |  | 🔴 Q1: Urgent+Important |  | ◻ |
| 2 |  | 🟡 Q2: Not Urgent+Important |  | ◻ |
| 3 |  | 🔵 Q3/Q4 |  | ◻ |

**Linked**: [[Priority Matrix Export — {{date:YYYY-MM-DD}}]]
Tags: #goal #today #eisenhower

---

## 📅 Today's Events
> *Next 3 events from calendar. Auto-populated via NotePlan/Google Calendar sync.*

| Time | Event | Location/Link | Prep Needed |
|------|-------|---------------|-------------|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

**Calendar source**: Google Calendar → NotePlan → Daily Note
Tags: #event #calendar

---

## 🤖 AI Outputs Inbox
> *Auto-populated. Every AI conversation from today lands here via Notion webhook.*

| Platform | Title | Key Output | Action Items | Link |
|----------|-------|------------|--------------|------|
| Claude |  |  |  | [[AI/{{date:YYYY-MM-DD}}-claude-]] |
| ChatGPT |  |  |  | [[AI/{{date:YYYY-MM-DD}}-chatgpt-]] |
| Grok |  |  |  | [[AI/{{date:YYYY-MM-DD}}-grok-]] |
| Gemini |  |  |  | [[AI/{{date:YYYY-MM-DD}}-gemini-]] |

Tags: #ai-output #inbox

---

## ✍️ Handwritten Notes (Surface Input)
> *Converted from OneNote/Whiteboard via OCR pipeline. Review and link.*

```
{{surface-ocr-output}}
```

**Source**: OneNote Section → Power Automate → This Note
**Attachments**: [[Surface Sketches/{{date:YYYY-MM-DD}}]]
Tags: #handwritten #surface #ocr

---

## 🔗 Quick Capture Inbox
> *Items captured via Google Keep, Bear, or Remarkable throughout the day.*

### From Google Keep (via Make.com)
-

### From Bear (via export)
-

### From Remarkable (via USB/cloud sync)
-

Tags: #capture #inbox

---

## 📊 End-of-Day Review
> *Fill at end of day. 2 minutes max.*

- **Energy level today** (1-5):
- **Goals completed**: /3
- **Biggest insight**:
- **Tomorrow's #1 priority**: [[Daily Note — {{date+1:YYYY-MM-DD}}]]

---

*This note is a node in your [[Obsidian Graph]]. It connects to: projects, AI outputs, events, and weekly reviews.*
