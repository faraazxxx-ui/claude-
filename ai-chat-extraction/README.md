# AI Chat Extraction → Obsidian + Notion (Karpathian Structure)

A complete, working system for pulling **years of AI conversations off every
platform** into an Obsidian vault and Notion database — and then making that
archive *bilateral and active*: it automatically deposits, transforms, links,
loops back to you, and lets an AI reach back into it to generate new work
with you.

This extends the architecture in `../daily-note-ai-integration/SYSTEM.md`
(Obsidian = see, Notion = store, AI = pipeline). That doc solved *prospective*
capture. This one solves the **retrospective archive**, the **wiki layer on
top of it**, and the **loop**.

---

## 0. The mental model — the karpathian extraction structure

Andrej Karpathy published two ideas this system is built on:

**The append-and-review note** ([karpathy.bearblog.dev](https://karpathy.bearblog.dev/the-append-and-review-note/)) —
one single note; new thoughts appended to the top; old items "sink as if
under gravity"; periodic review rescues what still matters back to the top.
Nothing is filed, nothing is lost, resurfacing does the remembering.

**The LLM Wiki** ([gist, Feb 2026](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) —
a three-layer, compiler-shaped knowledge base:

```
raw/        immutable sources        ← "source code"   (your exported chats)
wiki/       LLM-maintained pages     ← "compiled output" (entities, concepts, syntheses)
CLAUDE.md   schema & conventions     ← "the compiler's config"
```

Three operations: **ingest** (LLM reads a source, updates 5–15 wiki pages,
logs it), **query** (ask the wiki, file valuable answers back in), **lint**
(find contradictions, orphans, stale claims). Two special files: `index.md`
(catalog) and `log.md` (append-only provenance). The core claim:
**compilation over retrieval** — read each source once, integrate it, and
never re-derive it. *"The wiki is the product; the chat is just the
interface."*

Your linked YouTube short couldn't be fetched from this environment, but this
is the method it's circulating — the gist hit 5,000+ stars within days and
the Obsidian + Claude Code implementation is the canonical build (Obsidian is
the viewer, Claude Code is the writer, the wiki is the codebase).

This repo implements all of it, plus a fourth and fifth operation Karpathy
doesn't need but you do (see §7): **resurface** and **reflect**.

```
                 RETROSPECTIVE                          PROSPECTIVE
  ChatGPT ─ Claude ─ Gemini ─ Grok ─ Perplexity        new chats daily
        │ official data exports (§1)                        │ (§6)
        ▼                                                   ▼
  extract_chats.py (§2) ──────────────►  Vault/raw/  ◄──── auto-capture
                                             │ immutable
                            distill_wiki.py / Claude Code "ingest" (§3)
                                             ▼
                                        Vault/wiki/  ← entities · concepts ·
                                             │          projects · self
                    ┌────────────────────────┼──────────────────────┐
                    ▼                        ▼                      ▼
          vault_to_notion.py (§4)   resurface.py (§5)      Claude Code (§6)
          Notion mirror (invisible) daily notes loop       query · generate ·
                                                           reflect — bilateral
```

---

## 1. Export everything (the retrospective sweep)

Every major platform has an official bulk export. UI paths drift — if a menu
moved, search "export data" in that platform's settings. Do all of these in
one sitting; each arrives by email.

| Platform | Where | You get | Notes |
|---|---|---|---|
| **ChatGPT** | Settings → Data Controls → **Export data** | zip with `conversations.json` (every conversation, full tree) | Email link expires in ~24h — download immediately |
| **Claude** | Settings → Privacy → **Export data** | zip with `conversations.json`, `projects.json` | Same 24h-style expiry |
| **Gemini** | [takeout.google.com](https://takeout.google.com) → deselect all → **My Activity** → filter to *Gemini Apps* → JSON format | `MyActivity.json` | Takeout logs prompts (and often responses) as activity records, not full transcripts — the weakest export of the majors |
| **Grok** | grok.com → Settings → Data Controls → export; or your X/Twitter archive (X-based Grok chats ride along in it) | JSON | Format shifts; use `--source generic` if the parser balks |
| **Perplexity** | Settings → Account → data export request; individual threads also export as Markdown (`⋯` on a thread) | varies | Bulk export is email-request based; thread-level Markdown goes straight to `--source generic` |
| **Copilot** | [Microsoft privacy dashboard](https://account.microsoft.com/privacy) → activity data | limited | Weakest export; screenshot/paste valuable threads to a folder and use `--source generic` |

**Do this today for ChatGPT and Claude even if you build nothing else** —
exports are also your backup against account loss.

## 2. Extract into the vault

Create (or pick) your Obsidian vault, then run the extractor once per export.
No dependencies — Python 3.9+ only.

```bash
cd ai-chat-extraction/scripts

python3 extract_chats.py --source auto --input ~/Downloads/chatgpt-export.zip --vault ~/Vault
python3 extract_chats.py --source auto --input ~/Downloads/claude-export.zip  --vault ~/Vault
python3 extract_chats.py --source auto --input ~/Takeout/MyActivity.json      --vault ~/Vault
python3 extract_chats.py --source generic --platform-label perplexity \
        --input ~/perplexity-threads/ --vault ~/Vault
```

Each conversation becomes one Markdown note in
`Vault/raw/conversations/<platform>/<year>/` with frontmatter the rest of the
pipeline keys off:

```yaml
type: conversation      platform: chatgpt     date: 2023-05-14
distilled: false        # → flipped by the ingest step
notion_synced: false    # → flipped by the Notion sync
last_resurfaced: never  # → managed by the resurface loop
```

Re-runs are idempotent (existing notes are skipped), so when you re-export
in six months, run the same command and only new conversations land.

**Point Obsidian at the vault** and open the graph view — years of your
thinking are now visible as nodes, colorable by platform folder.

## 3. Build the wiki layer (this is the karpathian part)

Copy the schema into your vault, once:

```bash
cp ../vault/CLAUDE.md      ~/Vault/CLAUDE.md
cp -r ../vault/templates   ~/Vault/templates
```

`CLAUDE.md` is the whole trick. It tells Claude Code how to be a disciplined
wiki maintainer instead of a chatbot: the raw/wiki/schema layers, page types,
frontmatter, wikilink conventions, provenance rules, and five operations —
**INGEST / QUERY / LINT / RESURFACE / REFLECT**. Read it; it's short and it's
the one file you're allowed to keep editing as your conventions evolve
("the schema file is everything").

Then start compiling. Either drive it from the terminal:

```bash
python3 distill_wiki.py --vault ~/Vault --batch 10          # deep pass via Claude Code
python3 distill_wiki.py --vault ~/Vault --backend api --batch 50   # fast bulk first-pass
```

…or just open Claude Code inside the vault and talk to it:

```bash
cd ~/Vault && claude
> ingest 10
> what do I know about discovery strategy?     # QUERY — answer gets filed back in
> lint                                          # health check
```

Every ingest reads undistilled conversations, updates/creates entity, concept
and project pages with `[[wikilinks]]` and source citations, updates
`wiki/index.md`, appends to `wiki/log.md`, and flips `distilled: true`.
A few thousand conversations take a few evenings of `ingest` batches — run
the cheap API first-pass across everything, then let the deep pass work
through it over weeks. There is no deadline: the system is useful from the
first batch.

## 4. Mirror to Notion

Per your SYSTEM.md philosophy: **you never open Notion** — it's the invisible
structured mirror (queryable database, mobile search, sharing surface).

One-time setup: create a Notion integration + a database with properties
`Name / Type / Platform / Date / Tags / VaultPath` and share the database
with the integration (details in the script header). Then:

```bash
export NOTION_API_KEY=secret_xxx NOTION_DB_ID=xxxx
python3 vault_to_notion.py --vault ~/Vault              # incremental — safe to cron
```

Sync direction is deliberately **one-way, vault → Notion**. The vault is the
single source of truth; Notion is a projection. (Two-way sync between two
mutable stores is where these systems go to die.) "Bilateral" lives in §6 —
between **you and the AI**, not between the two databases.

## 5. Close the loop — resurfacing (the gravity engine)

```bash
python3 resurface.py --vault ~/Vault --count 4
```

Picks 3–5 notes weighted toward *never-resurfaced, old, open-loop* items and
appends them with one-line teasers to today's daily note under
`## 🔁 Resurfaced`. Schedule it so it never depends on you remembering:

```
# crontab -e            (macOS/Linux — every morning at 6:00)
0 6 * * * /usr/bin/python3 /path/to/resurface.py --vault "$HOME/Vault"

# Windows: Task Scheduler → Daily 06:00 → python resurface.py --vault C:\Users\you\Vault
# Bonus: weekly Notion sync
0 7 * * 0 /usr/bin/python3 /path/to/vault_to_notion.py --vault "$HOME/Vault"
```

This is Karpathy's "scroll down and rescue" step, made involuntary. The smart
version is the RESURFACE operation in CLAUDE.md — ask Claude Code
*"what am I forgetting?"* and it picks with judgment instead of weighted
randomness. Use both: dumb-daily, smart-weekly.

## 6. Bilateral & active — the AI reaches back in

Everything above deposits *into* the system. What makes it bilateral:

**Claude Code inside the vault is the read/write interface.** Because the
vault is plain Markdown on disk, `claude` in the vault root can search it,
read it, and write to it under the CLAUDE.md contract. That gives you:

- **Query** — *"Across all my chats, what were my strongest arguments about
  X?"* Answers come from the compiled wiki with wikilink citations, and real
  syntheses get filed back into `wiki/syntheses/` — explorations compound
  instead of evaporating.
- **Generate from the corpus** — *"Draft the Dubai risk memo using everything
  in wiki/projects/Minecore and my prior risk frameworks."* New work is built
  *out of* your accumulated thinking, not from a cold start.
- **Prospective work** — *"Look at my open action items across projects and
  plan my week; write it into today's daily note."*
- **Reflect ("form me")** — the REFLECT op maintains `wiki/self/`: your
  thinking patterns, recurring questions across years and platforms,
  abandoned threads with drop reasons, and dated principles (including
  reversals). Run it monthly. This is the corpus turned into a mirror — the
  system doesn't just remember *for* you, it shows you *who you've been
  becoming* and hands you one pattern to use each week.

**Ongoing capture** (the prospective side, from your SYSTEM.md): a capture
extension (e.g. Pactify) auto-saves new chats → Notion → a sync drops them
into `Vault/raw/` — or simpler and sturdier: re-run your platform exports
monthly and let the extractor's idempotency pick up only what's new. New
material becomes `distilled: false` and the same ingest → link → resurface
machinery digests it. The loop is closed: **capture → compile → resurface →
new conversation → capture.**

Optional upgrades when you want them: an Obsidian MCP server (or `qmd`-style
local hybrid search) so claude.ai / Claude Desktop can also query the vault;
Obsidian's official Claude-Code-in-Obsidian integration; NotebookLM pointed
at `wiki/` exports for weekly audio digests.

## 7. The ADHD design layer — filleting the limits

Honest framing first: no system changes your neurology, and this one doesn't
claim to. What it does is **relocate the functions ADHD taxes most from your
brain into the system**, so working memory and prospective memory stop being
load-bearing. Every design choice above maps to a specific failure mode:

| Executive function load | Where it usually fails | What carries it here |
|---|---|---|
| Working memory | "I had it a second ago" | Everything captured verbatim in `raw/`; nothing depends on holding a thought |
| Prospective memory | "I was supposed to look at that" | `resurface.py` on cron — remembering is scheduled, not willed |
| Task initiation / filing | The 40-minute "organize my notes" session that never happens | You never file. The LLM files. `raw/` is append-only chaos by design |
| Out of sight = out of existence | Great ideas rot in old chats | Gravity loop pushes old thinking into today's note, where your eyes already are |
| Context reconstruction after interruption | 20 minutes rebuilding "where was I" | `wiki/projects/` pages + daily-note next-actions are permanent re-entry points |
| Working-memory overflow in conversation | Insights lost mid-chat | Chats are the *input medium*; the wiki is the retained product |
| Self-observation across time | Patterns invisible at day-scale | REFLECT reads years at once — recurring questions, abandoned threads, reversals |
| Decision fatigue | "Where does this go?" kills capture | One rule: everything → `raw/` or the daily note. Zero filing decisions, ever |

Three operating rules that keep it working:

1. **Never let the system demand tidiness.** The moment maintenance becomes
   your job, it dies. Lint is the LLM's job, on a schedule.
2. **One next action, always.** Every Claude session ends with exactly one —
   in the reply and in today's note. Lists of five are lists of zero.
3. **The daily note is the only place you must look.** Everything important
   flows *to* it. One surface, one habit, everything else is machinery.

## 8. Maintenance rhythm

| Cadence | What | Who does it |
|---|---|---|
| Daily, automatic | `resurface.py` → daily note | cron |
| Whenever you work | `claude` in vault: query, generate, capture | you + Claude |
| ~Weekly | `ingest 10` until backlog clears; smart RESURFACE | Claude (you say two words) |
| ~Monthly | `lint` · `reflect` · re-export platforms → re-run extractor · Notion sync check | Claude + one command |

If you skip a month, nothing breaks — the backlog just waits. That is the
point: this system degrades gracefully in exactly the way ADHD needs.

---

## Files in this kit

```
ai-chat-extraction/
├── README.md                      ← you are here
├── scripts/
│   ├── extract_chats.py           # exports → raw/ notes (stdlib only)
│   ├── distill_wiki.py            # ingest runner: Claude Code CLI or API backend
│   ├── vault_to_notion.py         # vault → Notion mirror (stdlib only)
│   └── resurface.py               # daily gravity loop (stdlib only)
└── vault/
    ├── CLAUDE.md                  # ★ the schema — copy to your vault root
    └── templates/
        ├── wiki-page.md
        └── daily-note.md
```

**Sources:** Karpathy, [The append-and-review note](https://karpathy.bearblog.dev/the-append-and-review-note/) ·
Karpathy, [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) ·
community builds: [Obsidian + Claude Code walkthrough](https://aimaker.substack.com/p/llm-wiki-obsidian-knowledge-base-andrej-karphaty),
[llm-wiki setup gist](https://gist.github.com/kennyg/6c45cace2e1c4e424a28fcd51dd6c25b),
[critique & v2 (confidence scoring, supersession)](https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres)
