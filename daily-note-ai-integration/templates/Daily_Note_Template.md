---
date: "{{date:YYYY-MM-DD}}"
day: "{{date:dddd}}"
type: daily
created: "{{date:YYYY-MM-DD HH:mm}}"
tags: [daily, reflection, tasks]
eisenhower_sync: true
---

# {{date:dddd, MMMM D, YYYY}}

---

## Yesterday — What Went Well
1.
2.
3.

## Yesterday — What I'd Do Differently
1.
2.
3.

---

## Today's Plan

### My 3 Tasks
- [ ] `🔴`
- [ ] `🟡`
- [ ] `🔵`

> `🔴` = Urgent + Important (must happen)
> `🟡` = Important, not urgent
> `🔵` = If time allows
> *Synced from [[Priority Matrix]] via webhook*

### My 3 Events
| Time | Event | Link |
|------|-------|------|
| **--:--** | | |
| **--:--** | | |
| **--:--** | | |

> *Auto-populated from Google Calendar via Full Calendar plugin*

---

## Inbox
> Everything below auto-populates. Don't type here.

### Surface Notes (OneNote → Power Automate)
```
{{surface-ocr-output}}
```
> *Handwritten notes converted via OneNote Ink-to-Text → Power Automate → this vault*

### AI Conversations Today
```dataview
TABLE platform, summary
FROM "AI"
WHERE date = this.date
SORT file.ctime DESC
```

### Quick Captures (Keep / Bear)
```dataview
LIST
FROM "Inbox/Keep" OR "Inbox/Bear"
WHERE date = this.date
```

---

## Weekly Connections
```dataview
LIST
FROM "Projects"
WHERE contains(file.inlinks, this.file.link)
```

---

*<< [[{{date-1:YYYY-MM-DD}}]] yesterday | tomorrow [[{{date+1:YYYY-MM-DD}}]] >>*
