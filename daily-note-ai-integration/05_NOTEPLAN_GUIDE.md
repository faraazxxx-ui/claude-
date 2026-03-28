# NotePlan — What It Is and How YOU Use It

---

## What NotePlan Actually Is

NotePlan is a **markdown-native planner** that combines three things in one app:
1. **Notes** — plain markdown files (just like Obsidian)
2. **Tasks** — todos with due dates, priorities, and scheduling
3. **Calendar** — shows your Google/Apple calendar events alongside your tasks

The killer feature you love: **drag tasks from your notes directly onto your calendar to time-block them.**

---

## Platform Availability

- macOS (native app)
- iOS / iPadOS
- **No Windows version** — this is critical for you as a Surface user
- Files sync via iCloud or CloudKit

### Windows Workaround
Since you use a Windows Surface, you have options:
1. **Use NotePlan on an iPhone/iPad** for scheduling, sync markdown files to a shared folder that Obsidian on Windows reads
2. **Alternative for Windows**: Consider **Morgen** or **Akiflow** which offer similar drag-and-drop scheduling on Windows
3. **Obsidian + Full Calendar plugin**: Replaces NotePlan's calendar view entirely within Obsidian (works on Windows)

---

## How to Use NotePlan (Your Workflow)

### Morning Routine (5 minutes)
1. Open NotePlan on your phone/iPad
2. Your **daily note** auto-generates (same template as Obsidian)
3. Review your 3 goals from the daily note
4. **Drag each goal** to a time slot on your calendar
5. Calendar now shows: your Google events + your time-blocked goals

### During the Day
- Check off tasks as you complete them
- New tasks? Type them in the daily note — schedule later
- NotePlan syncs markdown files → Obsidian picks them up

### Evening (2 minutes)
- Incomplete tasks? Drag them to tomorrow
- Fill in "Yesterday's Wins" and "Growth Edges" for tomorrow's note

---

## NotePlan Features You Need

| Feature | What It Does | Why You Need It |
|---------|-------------|-----------------|
| **Daily Notes** | Auto-creates a note for each day | Same as Obsidian daily notes — they can share files |
| **Drag & Drop** | Drag tasks to calendar time slots | This is the feature you love — visual time-blocking |
| **Calendar Integration** | Shows Google/Apple Calendar | See events + tasks in one view |
| **Templates** | Apply templates to new notes | Use the daily note template from this system |
| **Review** | Weekly/monthly review mode | Aggregates incomplete tasks for review |
| **Timeblocking** | Assign duration to tasks | Fills calendar blocks for focused work |
| **Markdown Links** | `[[wikilinks]]` support | Links to Obsidian notes |
| **Tags** | `#tag` support | Same tags as Obsidian for consistency |

---

## NotePlan + Obsidian Sync Strategy

### Option A: Shared Folder (Simplest)
- NotePlan stores files in: `~/Library/Containers/co.noteplan.NotePlan3/Data/Library/Application Support/co.noteplan.NotePlan3/`
- Symlink or sync this folder with your Obsidian vault
- Both apps read/write the same markdown files
- **Caveat**: Only works on macOS

### Option B: iCloud + Obsidian Sync
- NotePlan syncs to iCloud
- Obsidian accesses the same iCloud folder as a vault
- Works for iOS ↔ Mac sync

### Option C: Obsidian Full Calendar Plugin (Windows Alternative)
- Install **Full Calendar** plugin in Obsidian
- It reads Google Calendar via ICS feed
- Create tasks in daily notes → they appear on the calendar
- Drag-and-drop scheduling within Obsidian
- **This may be your best option given Windows Surface usage**

---

## Recommended Setup for You

Given that you're on **Windows Surface** primarily:

```
PRIMARY PLANNING INTERFACE:
  Obsidian (Windows) + Full Calendar plugin
  → Gives you drag-and-drop scheduling IN Obsidian
  → No need for NotePlan on Windows

MOBILE SCHEDULING:
  NotePlan (iPhone/iPad) for on-the-go task scheduling
  → Sync daily notes via cloud folder to Obsidian vault

RESULT:
  Same markdown files, two interfaces
  Surface = Obsidian (write + graph + calendar)
  Mobile = NotePlan (quick scheduling + drag-drop)
```
