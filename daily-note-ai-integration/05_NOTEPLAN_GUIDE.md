# NotePlan — What It Is and How YOU Use It

---

## What NotePlan Actually Is

NotePlan is a **markdown-native planner** that combines three things in one app:
1. **Notes** — plain markdown files (just like Obsidian)
2. **Tasks** — todos with due dates, priorities, and scheduling via `>YYYY-MM-DD` syntax
3. **Calendar** — shows your Google/Apple calendar events alongside your tasks in a timeline sidebar

The killer feature you love: **drag tasks from your notes directly onto the timeline to time-block them.**

### What NotePlan Does NOT Have
- **No graph view** — this is Obsidian's territory. NotePlan has backlinks but no visual network diagram.
- **No Windows or Android version** — Apple ecosystem only (Mac, iOS, iPadOS) + limited beta web app
- **Sync is iCloud only** — no cross-platform sync to Windows

---

## Platform Availability (Verified March 2026)

| Platform | Status |
|----------|--------|
| macOS | Native app (primary platform) |
| iOS / iPadOS | Full feature parity including timeline/drag-drop (v3.9+) |
| Web | Beta at beta.noteplan.co — limited functionality |
| **Windows** | **Not available. No plans announced.** |
| **Android** | **Not available. No plans announced.** |
| Linux | Not available |

**Pricing**: ~$100/year (Personal) or available through **Setapp** subscription bundle. 7-14 day free trial.

### Windows Workaround (Critical for You)
Since you use a Windows Surface, you have three options:

1. **Obsidian + Full Calendar plugin** (RECOMMENDED) — replaces NotePlan's calendar view entirely within Obsidian on Windows. Drag-and-drop scheduling, Google Calendar sync via ICS feed.
2. **NotePlan on iPhone/iPad only** — use for on-the-go scheduling, sync markdown files via iCloud to a folder that Obsidian on Windows reads.
3. **Alternative Windows apps**: **Morgen** (drag-and-drop scheduling, integrates with Notion/Todoist) or **Akiflow** (drag-and-drop, integrates with Slack/Gmail/Asana).

---

## How NotePlan Actually Works (Deep Dive)

### Daily Notes
- Each day auto-generates its own note page — today's page is front and center when you open the app
- Tasks scheduled to a date using `>2026-03-28` syntax appear on that day's Daily Note automatically
- Tasks do **NOT** auto-roll-over to the next day (intentional — forces re-evaluation of priorities)
- Reschedule via keyboard shortcuts: `CMD+0` (today), `CMD+1` (tomorrow), etc.
- **Auto-templates**: set a template to pre-populate daily notes automatically when you first open them

### Time Blocking (The Feature You Love)
- **Mac**: Drag tasks from the note pane → drop on timeline sidebar (right side)
- **iOS/iPad** (v3.9+): Tap calendar+clock icon → drag tasks into timeline
- Resize blocks by dragging edges
- Multi-day view shows up to 7 days on timeline
- Time blocks can optionally sync BACK to Apple/Google Calendar
- Also type times inline: `10am - Write report`

### Task System
- Markdown-based: `- [ ] task` or `* [ ] task`
- States: open, done (`[x]`), cancelled (`[-]`), scheduled
- Priority levels, `#tags`, `@mentions`
- Schedule with `>YYYY-MM-DD` — task appears on that day's note

### Linking & Backlinks
- Wiki-links: `[[Note Title]]` with auto-complete
- Heading links: `[[Note Title#Heading]]`
- Date links: `[[2026-03-28]]` links to daily note
- Backlinks shown at top of each note
- If you rename a note, all wiki-links update automatically
- **No graph view** — connections discovered via backlinks panel only

---

## Plugin Ecosystem (JavaScript-based)

Plugins at [github.com/NotePlan/plugins](https://github.com/NotePlan/plugins). Install via Preferences > AI & Plugins.

| Plugin | What It Does |
|--------|-------------|
| **Dashboard** | Compact view of open tasks from today + scheduled tasks |
| **Event Automations & Calendar View** | Apple Calendar-style Year/Month/Week/Day views |
| **np.Templating** | Advanced templating engine (`<%- ... %>` syntax) with conditionals, loops, API calls |
| **Template Forms** | Visual form builder for meeting notes, contacts, etc. |
| **Project Management** | Start, review, pause, complete, cancel projects |
| **Note Helpers** | HTML preview with Mermaid diagrams, MathJax |
| **Note Statistics** | Stats for notes, tasks, words, hashtags over time |
| **Tag Tracking** | Track and chart tag values (e.g., @sleep, @weight) |
| **Search & Replace** | Advanced search operators, saved searches, bulk replace |

### AI Features (v3.9.3+)
- Built-in ChatGPT-4 integration for summarizing, rewriting, idea generation
- OpenAI Whisper voice transcription on iOS
- AI prompts can reference daily notes of specific time periods for context

### Shortcuts Support (v3.13+)
- Full Apple Shortcuts integration
- "Run Plugin Command" action executes any plugin command
- Pre-built: Dictate into Today, New Task with Options, Email Followup
- Trigger via Siri, Lock Screen, Action button (iPhone 15 Pro+)

---

## NotePlan vs Obsidian — Side-by-Side

| Dimension | NotePlan | Obsidian |
|-----------|----------|----------|
| **Core identity** | Calendar-first daily planner | Knowledge-base-first |
| **Learning curve** | Low — intuitive from launch | High — requires setup |
| **Task management** | Built-in, first-class | Requires plugins |
| **Calendar integration** | Native, deep | Requires plugins |
| **Time blocking** | Built-in drag-and-drop | Not native |
| **Graph view** | **None** | Full visual network |
| **Linking** | Wiki-links + backlinks | Wiki-links + backlinks + graph + unlinked mentions |
| **Plugin ecosystem** | Growing (~dozens) | Massive (1000+) |
| **Platforms** | **Apple only** + beta web | **All platforms** |
| **Sync** | iCloud (free, Apple-only) | Obsidian Sync ($5/mo) or DIY |
| **Pricing** | ~$100/year subscription | Free (Sync/Publish extra) |
| **File format** | Plain Markdown | Plain Markdown |
| **AI features** | Built-in (GPT-4, Whisper) | Via plugins |

---

## NotePlan + Obsidian Sync Strategy

### Option A: Shared Folder (Mac Only)
- NotePlan stores files in: `~/Library/Containers/co.noteplan.NotePlan3/Data/Library/Application Support/co.noteplan.NotePlan3/`
- Symlink or sync this folder with your Obsidian vault
- Both apps read/write the same markdown files
- **Caveat**: Only works on macOS — not useful for your Surface

### Option B: iCloud Bridge (iOS → Windows)
- NotePlan syncs to iCloud
- Install iCloud for Windows on your Surface
- Point Obsidian vault to the iCloud NotePlan folder
- **Limitation**: iCloud for Windows can be unreliable

### Option C: Obsidian Full Calendar Plugin (RECOMMENDED for Windows)
- Install **Full Calendar** plugin in Obsidian
- It reads Google Calendar via ICS feed
- Create tasks in daily notes → they appear on the calendar
- Drag-and-drop scheduling within Obsidian
- **This is your best option given Windows Surface usage**

---

## Recommended Setup for You

Given that you're on **Windows Surface** primarily:

```
PRIMARY PLANNING INTERFACE (Windows Surface):
  Obsidian + Full Calendar plugin + Templater + Dataview
  → Drag-and-drop scheduling IN Obsidian
  → Graph view for visual/spatial navigation
  → Auto-generated daily notes with your template
  → No need for NotePlan on Windows

MOBILE SCHEDULING (iPhone/iPad — optional):
  NotePlan for on-the-go task scheduling
  → Sync daily notes via iCloud → Obsidian vault
  → Use for quick task rescheduling when away from Surface

HANDWRITING INPUT (Surface):
  OneNote → Power Automate → Obsidian vault
  → Draw/write on Surface → auto-converts to markdown
  → Appears as node in Obsidian graph

RESULT:
  Same markdown files, multiple interfaces
  Surface = Obsidian (write + graph + calendar + handwriting input)
  Mobile = NotePlan (quick scheduling + drag-drop) — optional
  Both feed the same vault
```

### If You Don't Want NotePlan At All
Given the Apple-only limitation, you can **skip NotePlan entirely** and get the same workflow with:
- **Obsidian + Full Calendar plugin** = calendar view + drag-and-drop
- **Obsidian + Tasks plugin** = task scheduling with `>date` syntax
- **Obsidian + Periodic Notes plugin** = auto-generated daily/weekly/monthly notes
- **Obsidian + Kanban plugin** = visual task boards (another spatial interface you'd like)

This keeps everything in one app on your Windows Surface.
