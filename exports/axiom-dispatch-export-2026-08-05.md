# Export: Main Fork Repository Contents + Dispatch Chat Outputs
**Generated:** 2026-08-05 ~02:10 AM EDT  
**Team:** Grok (leader) + Harper, Benjamin, Lucas  
**Format:** Hierarchical Markdown (Obsidian/NotePlan/Axiom Wiki compatible)  
**Purpose:** Park branching ideas into structured export while clarifying remaining ambiguities. Aligns to QIBLA-style hierarchical organization and Axiom dual-path (prompt + compounding wiki).

---

## Goal Anchor
Export **all contents** of "this main fork repository" + **outputs of all chats in this dispatch** → single MD or JSON file.

**True Intent (from project memory + context):** Support the Axiom Cognitive Extender work — turn raw docs/chat outputs into living Karpathy-style wiki pages (persistent, compounding, cross-linked MD). Prefer simplest mass-dump path (Google Drive link) so AI handles parsing into raw + wiki. Not yet comfortable with full RAG; equilibrium on dual-path (pure prompt + Axiom Wiki CLI).

---

## Branch 1: Clarification Needed (Highest Priority)
"This" implies prior context not fully resolved in tools/history. Options:

### 1.1 Repository Identification
- **Candidate A (most likely public match):** `faraazxxx-ui/claude-`  
  - Your only public GitHub repo (authenticated user: faraazxxx-ui).  
  - Not marked as fork. Last updated: 2026-08-05.  
  - Content: Large collection of AI-derived MD/JSON/PPTX outputs — optimized prompts, legal strategy (Rahman case), health/clinical reports (POTS, autonomic, sleep), skills (apex-legal, life-intelligence-engine, verbal-prompt-optimizer), daily workflow, Eigent AI docs, Ghusoon project, NotebookLM sources, red-team analyses, etc.  
  - ~297 items in tree (many MD files with chat/AI synthesis outputs).  
  - **Full tree structure included in Branch 2 below.**

- **Candidate B (matches Axiom project memory exactly):** Fork or local of `abubakarsiddik31/axiom-wiki`  
  - Public source: https://github.com/abubakarsiddik31/axiom-wiki  
  - "The wiki that maintains itself." Inspired by Andrej Karpathy's llm-wiki gist.  
  - AI-powered personal knowledge base: ingest docs → extract entities → interconnected markdown wiki pages. Commands: init, ingest, query, autowiki, sync, watch, graph, etc.  
  - Supports Gemini (recommended), OpenAI, Anthropic, OpenRouter, DeepSeek, Groq, Mistral, Ollama.  
  - Structure: `raw/` (sources), `wiki/pages/{entities,concepts,sources,analyses}/`, `index.md`, `log.md`.  
  - Project memory (2026-08-01): Triggered Axiom Cognitive Extender for living Karpathy-style wiki; equilibrium dual-path (pure prompt + Axiom Wiki CLI); prefer Google Drive mass-dump of files for AI parsing into raw + wiki.  
  - Browsed README content available in artifacts/browsed_files/.

- **Candidate C:** Private fork / other repo / local folder / Google Drive mass-dump folder.  
  Provide: exact URL / owner / repo name / folder link / whether private.

### 1.2 "This Dispatch" Definition
- This multi-agent team session (Grok + Harper + Benjamin + Lucas)?  
- Specific past Axiom / RLN / prompt-optimization chats?  
- All project conversations?  
- The collection of outputs already inside the claude- repo?

### 1.3 Preferred Output & Delivery
- MD (wiki-style, cross-linkable) or JSON (structured dump)?  
- Delivery:  
  - Google Drive file/folder (preferred per memory — simplest for mass)  
  - Push to GitHub repo  
  - Local artifacts (this file)  
  - Paste / download link

**Reply with 1-2 lines clarifying the above and we execute full dump.**

---

## Branch 2: Interim Export (What We Can Deliver Now)
### 2.1 Project Memory (Durable Facts)
```
- User triggered Axiom Cognitive Extender for turning raw documents into living Karpathy-style wiki pages (persistent, compounding, cross-linked MD for insights + live interaction) rather than static RAG. Goal: first-step reframing for interaction, then NotePlan/Obsidian compatibility; BigQuery/Databricks secondary. Not yet comfortable with full RAG. Equilibrium reached on dual-path (pure prompt + Axiom Wiki CLI). [2026-08-01]
- User found previous steps too many; wants mass-dump of files so AI does all parsing into raw + wiki. Preferred simplest: link Google Drive folder (connected tools available). croc secondary. [2026-08-01]
```

### 2.2 Public Repo Structure: faraazxxx-ui/claude- (Full Recursive Tree Summary)
**Owner/Repo:** faraazxxx-ui / claude-  
**Tree SHA:** main (3b6aac4339f7cbad8c120518851d210c09a17b31)  
**Item count:** ~297  

**Top-level & Key Directories/Files (hierarchical):**
- **Root MD files (chat/AI outputs):**  
  AI_Platform_Master_Reference_FULL.md, CYB003_Optimized_Prompts.md, Dubai_Risk_Assessment_Minecore.md, FINAL_DELIVERABLE_Rahman_Risk_Assessment.md, FINAL_Perfected_Prompt_v2.md, Optimized_Prompt_Manus.md, PERFECTED_PROMPT_Red_Team_Edition.md, Personal_Data_Embedding_Living_AI_Guide.md, PowerToys_AI_Workflow.pptx, README.md, geopolitical_risk_analysis_minecore.md, powertoys_ai_workflow.md, red_team_prompt_analysis.csv

- **analysis-output/**  
  LEGAL_INTELLIGENCE_SYNTHESIS.md, REFRAMED_10M_STRATEGY.md, cross_references.json, damage_reframe_research.json, deep_analysis_segments.csv/.json, domain_map.json, entity_registry.json, extraction_stats.json, legal_precedent_research.json, master_report.md, triage_classification.json  
  - perfected/: ACTIONABLE_BRIEFING.md, EXECUTION_PROMPT.md, GITHUB_GEMS_INTEGRATION.md, PERFECTED_MASTER_REPORT.md, SECOND_BRAIN_ARCHITECTURE.md, red_team_analysis.json

- **autonomic_intelligence_v3/**  
  AUTONOMIC_INTELLIGENCE_REPORT_v3.md, alerts.json, autonomic_dashboard.png, execute_master_prompt.py, glp1_readiness.json, loop_score_timeline.png, loop_scores.csv, medication_adherence_v3.json, quarterly_comparison.json, snapshot.json, trend_7d.json

- **clinical_report_v4/**  
  CLINICAL_REPORT_v4.md, analysis_results.json, master_analysis.py, validation.json  
  - charts/: 01_autonomic_balance.png … 05_symptom_correlation.png

- **daily-note-ai-integration/**  
  RED_TEAM_ANALYSIS.md, SYSTEM.md

- **daily-workflow-optimizer/**  
  FINAL_COMPARATIVE_ANALYSIS_AND_PERFECTED_PROMPT.md, PERFECTED_PROMPTS.md, README.md, SKILL.md, research_data.csv  
  - prompts/: 01_manus.md … 10_gemini_browser.md  
  - references/, scripts/, templates/daily-note-template.md

- **eigent-ai-docs/** (full docs set)  
  Eigent_AI_Documentation.md, agent-skills.md, bug.md, byok.md, concepts.md, ernie.md, gemini.md, installation.md, kimi.md, local-model.md, minimax.md, quick_start.md, sambanova.md, support.md, tools.md, welcome.md, workforce.md, workers.md

- **ghusoon-project/**  
  Ghusoon_Optimized_Mega_Prompt.md, context_summary.md, knowledge_base.md  
  - parallel-outputs/ (multiple MD outputs)

- **ghusoon-prompt-hub-website/** (React/TS app structure)  
  index.html, src/App.tsx, components/, contexts/, hooks/, lib/promptData.ts, pages/, etc. (full UI component tree)

- **health_analysis/** + **health_analysis_v2/**  
  Longitudinal reports, charts (HRV, recovery, sleep, strain, symptoms, medication), CSVs, JSONs, red_team_analysis.md, PERFECTED_REPORT.md

- **legal-endeavors/**  
  SKILL.md, references/ (case-context, defense-analysis, litigation-playbook), scripts/, templates/

- **notebooklm/**  
  health_data_source.md (large), notebooklm_prompts.md

- **optimized-prompts/**  
  Ghusoon_Optimized_Prompts_Final.md, Ghusoon_Perfected_Prompts_v2.md, red_team_analysis.md, research_findings.md

- **prompts/**  
  FINAL_OPTIMIZED_PROMPTS.md, PERFECTED_PROMPTS.md, geopolitical_risk_analysis_prompt.md, medical_context.md, red_team_analysis.md

- **skill/** + **skills/**  
  health-data-analyst/, verbal-prompt-optimizer/, apex-legal-strategy/ (full references + scripts), life-intelligence-engine/ (export scripts for Evernote/NotebookLM/Notion/Obsidian, assemble/triage/extract tools)

- **verbal-thinker-stack-audit/**  
  parallel research CSVs/JSONs, verbal_thinker_stack_audit.md, voice-first-verbal-thinker-skill/

**Note:** Full binary contents (PPTX, PNGs) and every file body cannot be inlined here due to size/rate limits. Tree is complete. Use `get_file_contents` or clone when ready for specific files.

### 2.3 Axiom Wiki (Public Source) Structure Snapshot
From browsed README of abubakarsiddik31/axiom-wiki:

```
raw/                  Source files (PDF, MD, DOCX, images, HTML)
wiki/
  pages/
    entities/         People, places, organisations
    concepts/         Ideas, topics, theories
    sources/          One summary per source file
    analyses/         Filed answers, comparisons
  index.md            Page catalog
  log.md              Operation history
  usage.log           Token usage and cost
map-state.json        Autowiki/sync state
```

Quick start: `npm i -g axiom-wiki && axiom-wiki init && axiom-wiki ingest`  
Key commands: autowiki, query, sync, watch, graph, embed, mcp.

### 2.4 This Dispatch (Multi-Agent Session) Summary
- User request received.  
- Explored artifacts, project_memory, said_unsaid_memory, browsed axiom-wiki README.  
- Authenticated GitHub: faraazxxx-ui (1 public repo: claude-).  
- Rate limits (429) hit on multiple GitHub API calls; switched to browse + tree fetch (successful for claude-).  
- Conversation_search: No direct "main fork / dispatch" hits; many prior RLN / NotePlan / prompt-optimizer / verbal-thinker / health / legal chats.  
- Google Drive: No obvious Axiom/wiki folders in quick searches; personal files present.  
- Consensus: Ambiguity on exact repo + dispatch scope → hierarchical clarification first, interim structure export now, full dump after confirmation.  
- Team messages coordinated via chatroom; ready for next action.

### 2.5 Related Conversation Highlights (from semantic search)
Prior chats heavily feature:
- Recursive Living Notebook (RLN) → Evernote / Notion / Obsidian / NotePlan migrations and templates.
- Prompt optimization (Grok 4.3, Claude, Gemini, Manus, Perplexity, multi-platform).
- Verbal / spatial / ADHD-friendly systems, daily-note AI integration, handwriting → digital.
- Health (POTS, autonomic, sleep, recovery charts, medication adherence).
- Legal (Rahman case, APEX strategy).
- Skills creation and multi-agent (Eigent, Ghusoon).
- No exact match for "main fork repository" or "dispatch" export request prior to this session.

---

## Branch 3: Full Execution Path (After Clarification)
1. Confirm repo (or Drive folder ID/link).  
2. Clear rate limits → recursive tree + selective/all file contents via GitHub tools (or Drive read).  
3. Assemble:
   - Single hierarchical MD with `[[wikilinks]]` ready for Obsidian/NotePlan/Axiom.  
   - Or JSON: `{ "repo": {...}, "tree": [...], "files": {path: content}, "chats": [...], "memory": [...] }`  
4. Deliver via preferred path (create Google Drive file/folder + share link, or push to repo, or update this artifacts file).  
5. Optional: Run Axiom Wiki CLI style ingest on the dump for compounding pages.

**Threat flags / Buffers:**  
- GitHub API rate limits (already encountered).  
- Full historical chat transcripts not available (only summaries + this session).  
- Large binaries (PPTX, many PNGs) better left as references or separate download.  
- Private repos may require different auth / explicit share.

---

## Next Action Options (Choose / Reply)
- **A.** "It's the claude- repo" → I fetch priority files or full text dump of MD/JSON into expanded MD/JSON here or Drive.  
- **B.** "It's my fork of axiom-wiki / this Drive folder: [link]" → Proceed with mass parse.  
- **C.** "Compile more chat summaries + expand specific sections of claude-" → Specify which.  
- **D.** "Just give me this file as-is + put a copy in Drive" → Done.  
- **E.** Other (1-2 lines).

This parks the overflow, ladders tactics under the Axiom goal, and keeps energy low. Ready when you confirm.

---
*End of interim export. File location: `/home/workdir/artifacts/main_fork_repo_and_dispatch_export.md`*  
*Team ready for follow-through.*
