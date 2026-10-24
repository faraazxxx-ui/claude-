# MAP — What's in this repository

One page. Every domain, its entry point, and what it's for. If you're lost, start here.

> Organized by **thinking domain**, not by which AI agent produced what.
> Numbered folders = your active work areas. `skills/` = reusable agent skills.

---

## 01-legal — Rahman v. UHS litigation (3:26-cv-00197)

| Entry point | What it is |
|---|---|
| `01-legal/FINAL_DELIVERABLE_Rahman_Risk_Assessment.md` | Consolidated risk assessment — **start here** |
| `01-legal/analysis-output/master_report.md` | Master analysis: reframed $10M strategy, damages, 15 research vectors |
| `01-legal/analysis-output/LEGAL_INTELLIGENCE_SYNTHESIS.md` | Legal synthesis v3.0, 40+ case citations |
| `01-legal/analysis-output/REFRAMED_10M_STRATEGY.md` | The reframed litigation strategy |
| `skills/apex-legal-strategy/`, `skills/legal-endeavors/` | Legal skills (APEX three-phase method, filing/discovery tooling) |

Raw research data (JSON/CSV: entities, precedents, triage, cross-references) lives alongside in `analysis-output/`.

## 02-health — Longitudinal health / autonomic intelligence

| Entry point | What it is |
|---|---|
| `02-health/clinical_report_v4/CLINICAL_REPORT_v4.md` | Latest clinical report — **start here** |
| `02-health/autonomic_intelligence_v3/AUTONOMIC_INTELLIGENCE_REPORT_v3.md` | Loop-score / autonomic dashboard analysis |
| `02-health/health_analysis_v2/` | Perfected v2 (red-teamed, event-aware) |
| `02-health/health_analysis/` | Original longitudinal analysis (sleeps, physio CSVs) |
| `skills/health-data-analyst/` | Health data processing skill + scripts |

Progression: `health_analysis` → `v2` → `autonomic_intelligence_v3` → `clinical_report_v4` (newest last, highest number wins).

## 03-business-minecore — Minecore shipping / geopolitics

| Entry point | What it is |
|---|---|
| `03-business-minecore/WEST_AFRICA_EXPANSION_ASSESSMENT_Minecore_Nuhu.md` | Full West Africa expansion assessment — **start here** |
| `03-business-minecore/EXECUTIVE_SUMMARY_West_Africa_Expansion.md` | One-page summary of the above |
| `03-business-minecore/geopolitical_risk_analysis_minecore.md` | Geopolitical risk analysis |
| `03-business-minecore/Dubai_Risk_Assessment_Minecore.md` | Dubai-specific risk assessment |

## 04-prompts — Prompt engineering & red-teaming

| Entry point | What it is |
|---|---|
| `04-prompts/FINAL_Perfected_Prompt_v2.md` | The perfected prompt (red-teamed, rebuilt) — **start here** |
| `04-prompts/prompts/PERFECTED_PROMPTS.md` | Cross-platform perfected prompts collection |
| `04-prompts/optimized-prompts/` | Ghusaoon-optimized prompt variants + red-team analysis |
| `04-prompts/red_team_prompt_analysis.csv` | Structured red-team findings (31 KB) |
| `04-prompts/CYB003_Optimized_Prompts.md` | CYB003 prompt set |
| `skills/verbal-prompt-optimizer/` | Skill: verbal prompt → 10-platform optimized prompts |

## 05-ai-platforms — AI platform reference & personal data pipeline

| Entry point | What it is |
|---|---|
| `05-ai-platforms/AI_Platform_Master_Reference_FULL.md` | Cheat sheets: Claude, Gemini, Copilot, Grok, ChatGPT, Perplexity, Manus — **start here** |
| `05-ai-platforms/Personal_Data_Embedding_Living_AI_Guide.md` | Personal-data → BigQuery → embedding → self-retraining pipeline |
| `05-ai-platforms/eigent-ai-docs/` | Eigent AI documentation mirror |

## 06-ghusoon — Ghusoon project & prompt hub

| Entry point | What it is |
|---|---|
| `06-ghusoon/ghusoon-project/Ghusoon_Optimized_Mega_Prompt.md` | The mega prompt — **start here** |
| `06-ghusoon/ghusoon-project/knowledge_base.md` | Ghusoon knowledge base |
| `06-ghusoon/ghusoon-prompt-hub-website/` | Prompt hub website (static site, 70 files) |

## 07-workflow — Personal workflow / verbal-thinker stack

| Entry point | What it is |
|---|---|
| `07-workflow/verbal-thinker-stack-audit/verbal_thinker_stack_audit.md` | Your AI stack audit + missing links — **start here** |
| `07-workflow/daily-note-ai-integration/SYSTEM.md` | Daily-note AI integration system design |
| `07-workflow/powertoys_ai_workflow.md` | PowerToys AI workflow (see `.pptx` alongside) |
| `07-workflow/notebooklm/` | NotebookLM prompts + health data source |
| `skills/daily-workflow-optimizer/` | Skill: handwriting → daily note → AI → Notion, 10 platform prompts |

## 08-repo-exports — Prior multi-agent session outputs

| Entry point | What it is |
|---|---|
| `08-repo-exports/exports/repository_export.md` | Repo inventory from the 2026-08-05 dispatch (superseded by this MAP) |
| `08-repo-exports/exports/axiom-dispatch-export-2026-08-05.md` | Axiom wiki dispatch export |

Historical artifacts — read-only context, don't build on these.

## skills/ — Reusable agent skills

All six skills, one home. Each has a `SKILL.md` defining when/how to use it:

| Skill | Purpose |
|---|---|
| `apex-legal-strategy` | APEX Three-Phase Method for Rahman v. UHS |
| `legal-endeavors` | Filing generation, discovery requests, deadline tracking |
| `health-data-analyst` | Longitudinal health data analysis (event-aware, v2+) |
| `life-intelligence-engine` | Life corpus triage/export: Obsidian, Evernote, Notion, NotebookLM |
| `daily-workflow-optimizer` | Daily note → AI routing → Notion workflow |
| `verbal-prompt-optimizer` | Verbal/rambling prompt → 10-platform optimized prompts |

---

## Conventions (keep signal high)

- **One home per domain.** New work on a domain goes into its numbered folder — never loose at root.
- **Skills always live in `skills/<skill-name>/SKILL.md`.** No `skill/` singular, no root-level skills.
- **Versioning by folder suffix** (`_v2`, `_v3`, `_v4`): higher number = newer = preferred.
- **Reports pair with their data.** Keep raw CSV/JSON next to the report that interprets it.
- Root stays clean: `MAP.md`, `README.md`, numbered domains, `skills/`. Nothing else.
