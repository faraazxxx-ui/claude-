---
date: "{{date:YYYY-MM-DD}}"
day: "{{date:dddd}}"
week: "{{date:ww}}"
tags: [daily-note, reflection, planning]
cssclass: daily-note
---

# {{date:dddd, MMMM D, YYYY}}

---

## Yesterday's Wins

> What went well? Celebrate progress, no matter how small.

1. 
2. 
3. 

---

## Areas for Improvement

> What could I have done better? Be honest, not harsh.

1. 
2. 
3. 

---

## Today's Goals

> Three focused tasks. Use the Eisenhower matrix: Urgent+Important first.

- [ ] **Goal 1:** 
- [ ] **Goal 2:** 
- [ ] **Goal 3:** 

---

## Today's Events

> What's on the calendar? Pull from Google Calendar / North Plan.

| Time | Event | Location/Link |
|------|-------|---------------|
|      |       |               |
|      |       |               |
|      |       |               |

---

## Quick Capture

> Dump thoughts here. They will be auto-sorted by the automation.

- 

---

## AI Project Notes

> Auto-populated from Notion AI database. Do not edit manually.

```dataview
TABLE source, topic, date
FROM "AI-Outputs"
WHERE date = this.date
SORT date DESC
```

---

## Linked Notes

> Auto-generated backlinks from Obsidian graph.

```dataview
LIST
FROM [[]]
SORT file.mtime DESC
LIMIT 5
```
