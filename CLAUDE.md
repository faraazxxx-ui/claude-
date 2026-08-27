# claude-

Personal knowledge and working repository for Dr. Rahman. It holds project
workspaces, generated deliverables, and the Claude skills that produce them.

## Skills

Project skills live in `.claude/skills/` and load automatically in this repo.

| Skill | Purpose |
| --- | --- |
| `apex-legal-strategy` | Strategic analysis layer for the federal litigation (3:26-cv-00197, NDNY). Ships 6 reference docs: case timeline, damages calculator, defendant answers, discovery strategy, evidence inventory, policies violated. |
| `health-data-analyst` | Longitudinal analysis of Oura / WHOOP / Visible data against a Long COVID, POTS, and autonomic-dysfunction context. Event-aware v2 pipeline. |
| `life-intelligence-engine` | Document triage and second-brain builder; exports to Notion, Evernote, Obsidian, NotebookLM. |
| `verbal-prompt-optimizer` | Turns verbal-thinker prompts and voice transcripts into platform-specific prompts for 10 AI agents. |

`apex-legal-strategy` also exists at user level in a reduced form (SKILL.md only,
no references). The project copy here is the fuller one and takes precedence when
working in this repo — edit this copy, not the synced one.

## Layout

Working directories, each self-contained:

- `legal-endeavors/` — case file operations, deadline tracking, filing templates
- `health_analysis/`, `health_analysis_v2/`, `clinical_report_v4/`,
  `autonomic_intelligence_v3/` — successive generations of health analysis output
- `ghusoon-project/`, `ghusoon-prompt-hub-website/` — Ghusoon prompt work and its site
- `daily-workflow-optimizer/`, `daily-note-ai-integration/` — workflow tooling
- `prompts/`, `optimized-prompts/` — prompt libraries
- `eigent-ai-docs/`, `notebooklm/` — scraped and external reference material
- `analysis-output/`, `exports/` — generated artifacts

Top-level `.md` files are finished deliverables (risk assessments, platform
references, expansion assessments). Treat them as outputs, not working drafts.

## Conventions

- Versioned work is a new directory (`_v2`, `_v3`, `v4`), not an edit in place.
  Preserve superseded generations rather than overwriting them.
- Skill reference material belongs in that skill's `references/`; executable
  helpers belong in its `scripts/`.
- Skill scripts read from and write to absolute paths under `/home/ubuntu/work/`.
  These are inherited from the environment the skills were authored in and are
  not portable — check and adjust paths before running a script here.
