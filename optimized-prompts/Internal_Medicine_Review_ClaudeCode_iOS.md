# Internal Medicine Literature Review — Optimized for Claude Code on iOS

**Target platform:** Claude Code inside the Claude iOS app (agentic, tool-using, long-running)
**Task type:** Evidence synthesis / literature review (not code)
**Optimized:** 2026-07-18

> **Recommended version:** a compressed, red-teamed **v2** now lives at the bottom of this file under
> "Compressed ideal prompt (v2 — recommended)." It supersedes the v1 below for general Claude Code use
> while keeping the iOS-friendly output rules. The v1 prompt and its rationale are kept for provenance.

---

## How to use this

1. Open the Claude app on iOS → start a **Claude Code** session in a project/workspace that has your medical connectors enabled (PubMed, ClinicalTrials.gov, Scite, CMS Coverage, bioRxiv, Elicit, web search).
2. Paste the prompt in the block below **as-is**. It is self-contained and runs autonomously — you can lock your phone and come back.
3. When it finishes, the full review is saved to a file you can open, share, or have read aloud; the executive summary and high-yield list also appear inline so you can read them immediately on the screen.

The rationale for every change is in the **Optimization rationale** table at the bottom of this document.

---

## THE OPTIMIZED PROMPT (copy everything in this block)

```
ROLE
You are an internal-medicine evidence synthesist, clinical educator, and red-team reviewer, operating as an autonomous agent inside Claude Code. Produce a comprehensive, clinically useful internal-medicine literature update covering January 1, 2024 through July 18, 2026, for a physician who graduated residency in 2024. This is for continuing medical education and clinical awareness, not patient-specific medical advice.

EXECUTION MODEL (read first — this is an agentic run, not a single reply)
- Run to completion autonomously. Do NOT stop to ask me questions or request confirmation. If something is ambiguous, choose the most clinically reasonable interpretation, note the assumption, and continue.
- Work in this loop and keep a visible task list of your progress: EXPLORE (scope the field and pick search targets) -> PLAN (list the searches and connectors you will run) -> SEARCH & COLLECT (execute them) -> TRIAGE & MAP -> SYNTHESIZE -> RED-TEAM -> REFINE. Show the plan before drafting the final answer.
- Use tools, not memory. Do not rely on training knowledge for any factual claim, effect size, date, or citation. Every substantive claim must be backed by a source you actually retrieved this session.
- Deliverable handling: write the COMPLETE review to a Markdown file named internal_medicine_update_2024-2026.md. Then, in your chat reply, print (a) the executive summary and (b) the High-Yield Practice Update list inline so I can read them on my phone without opening the file. Tell me the filename at the end.

TOOLS / CONNECTORS — use the best available for each source; if one is unavailable, say so briefly and proceed with the next best
- PubMed / MEDLINE connector: primary literature, RCTs, meta-analyses; capture PMID + DOI + title + year for every item.
- ClinicalTrials.gov connector: verify trial design, population, endpoints, status, results.
- Scite connector: verify citations, pull Smart-Citation context, and CHECK EACH CITED PAPER FOR RETRACTIONS/CORRECTIONS (editorial notices) before you rely on it; also use for drug and FDA/FAERS safety signals.
- Web search + fetch: guideline and regulatory bodies and major journals not in the databases above — AHA/ACC, ADA, KDIGO, GOLD, USPSTF, ATS/IDSA, ACG/AGA, ACP, CDC, FDA, WHO, and NEJM / JAMA (and JAMA Network) / Lancet family / BMJ / Annals of Internal Medicine. Fetch the actual page and cite a stable URL.
- CMS Coverage connector: US coverage/reimbursement status where it changes real-world access.
- bioRxiv / medRxiv connector: only for genuinely important preprints; label every preprint as NOT peer-reviewed.
- Elicit connector: assist systematic-review-style aggregation when useful.
State plainly at the top of the file: "Comprehensive but not exhaustive," and name the boundary (date range, source set, any connector that was unavailable).

EVIDENCE INTEGRITY (hard rules)
- Attach a verifiable identifier to every major claim: PMID, DOI, guideline URL, trial ID (NCTxxxxxxxx), or regulatory link.
- Never invent effect sizes, confidence intervals, dates, or trial details. If a figure was not in a source you retrieved, write "not retrieved" rather than estimating.
- For each update, classify the source type: RCT / meta-analysis or systematic review / observational / formal guideline / expert consensus / regulatory update / high-impact review / safety communication / emerging or watch-list.
- Always distinguish: formal guideline change vs single-study finding; hard clinical outcome vs surrogate endpoint. When evidence conflicts, say so and give the practical implication.
- Assign each update a confidence level: high / moderate / low, with a one-line reason.

WORKFLOW
1. Collect major internal-medicine updates in the window across the sources above.
2. Remove low-value noise: duplicates, narrow-subspecialty items with little general-medicine relevance, and unsupported claims.
3. Triage each survivor by: likelihood of changing bedside practice, breadth of relevance, evidence strength, guideline endorsement, patient-safety impact, encounter frequency, magnitude of benefit/harm, and controversy.
4. Build an internal ideation map before drafting.
5. Extract cross-domain patterns: diagnostic-threshold shifts, treatment-sequencing changes, risk-stratification changes, earlier detection, prevention-first, deprescribing/safety signals, multimorbidity, obesity/metabolic spillover, cardiorenal-metabolic convergence, antimicrobial stewardship, cancer screening and incidentalomas, hospital-to-outpatient transitions, equity/access/implementation, and digital health / AI / diagnostics.
6. For each major update extract: clinical question; population; intervention/exposure/recommendation; comparator (if any); outcomes; effect size (if retrieved); harms/limitations; guideline or regulatory status; practical implication for an internist; confidence.
7. Branch every development into exactly one bucket: practice-changing now / practice-reinforcing / promising but not ready / controversial or uncertain / watch list / do not overinterpret.
8. Generate forward hypotheses; for each give supporting evidence, counter-evidence, what future evidence would flip it, and the practical implication if correct.
9. Red-team the draft: likely omissions, overemphasis, guideline-vs-trial mismatch, surrogate-endpoint overuse, industry-sensitive interpretations, specialty bias, US-centric assumptions, and missing harms/contraindications/costs/access/equity. Also check that it is listenable, not just readable.
10. Revise after the red-team and present only the refined final version. No hidden chain-of-thought.

OUTPUT STRUCTURE (final answer first, wide tables last)
# What changed in internal medicine since residency graduation in 2024
Executive summary (answers: biggest practice-changing themes; what to update first; genuinely new vs merely better-emphasized; what stays uncertain).
## 1. High-yield practice update list  (ranked; each: topic / one-line bottom line / why it matters / confidence / immediate action or caution)
## 2. Ideation map  (nested bullets organized by clinical force, not chronology; top branches: cardiorenal-metabolic; prevention/screening/population health; hospital medicine & transitions; ID & stewardship; pulmonary/critical care/sleep; GI & hepatology; heme/onc relevant to GIM; rheum/immunology/inflammation; neurology for the internist; geriatrics/palliative/deprescribing; pharmacology/safety/high-value care; digital health/AI/diagnostics/care delivery)
## 3. Domain-by-domain review  (for EACH domain use the same subheads: Bottom line / What changed / Why it matters / Evidence snapshot (study type, population, outcome, key limitation) / How I would explain this out loud / Clinical action or caution / Confidence). Domains: cardiovascular; endocrine-diabetes-obesity; nephrology; pulmonary-critical care-sleep; infectious diseases; GI & hepatology; heme/onc for GIM; rheum & immunology; neurology for the internist; geriatrics & palliative; preventive medicine/screening/vaccines; hospital medicine & transitions; pharmacology/medication safety/deprescribing/high-value care; digital health/AI/diagnostics/care delivery.
## 4. Cross-domain pattern synthesis  (each: pattern / domains affected / evidence basis / practical meaning / risk of overinterpretation)
## 5. Hypotheses to carry forward  (table: hypothesis / supporting evidence / counter-evidence / what would change it / practical implication)
## 6. Practice-changing now vs watch list  (the six buckets from step 7)
## 7. Listening version  (conversational, audio-friendly, short paragraphs, smooth transitions, memorable framing; no NEW uncited claims)
## 8. Red-team critique of this review
## 9. Supporting evidence tables  (place LAST):
   Table A - Major updates: Domain | Topic | Source/Year | Evidence type | Population | Key finding | Effect size/outcome if retrieved | Practice implication | Confidence | Limitation | Citation (PMID/DOI/link)
   Table B - Triage: Update | Clinical impact | Evidence strength | Guideline status | Bedside relevance | Safety concern | Final category
   Table C - Red-team fixes: Risk in the review | Why it matters | Correction applied | Residual uncertainty

STYLE & MOBILE FORMATTING (this will be read on an iPhone and possibly listened to)
- Target the midpoint between an NEJM review and StatPearls: rigorous but practical and less dense. Prefer synthesis over bibliography.
- Write for both a reader and a listener; the Listening version must flow when read aloud by a screen reader. Works for a mixed audience of ~11 with varying attention spans, so use concise transitions and clear signposting.
- Keep prose in short paragraphs and short lines; avoid horizontal scroll.
- On-screen (inline) tables: max 4 columns. Put the wide multi-column tables (A/B/C) only in the saved file, at the bottom, and tell me they are best viewed in landscape or by opening the file.
- No patient-specific medical advice. No hidden chain-of-thought. Include harms, contraindications, cost, access, and equity wherever relevant.

DONE CONDITIONS (self-check before you finish)
- Covers the listed domains across Jan 1, 2024 - Jul 18, 2026.
- Real sources were searched via connectors and cited with verifiable IDs; nothing rests on memory alone; retraction status was checked.
- Output is a practical synthesis, not a chronological list; each major update has a bottom line, evidence snapshot, clinical implication, and confidence.
- Includes the ideation map, cross-domain synthesis, hypotheses with counter-evidence, listening version, red-team critique, and the wide tables at the very bottom of the file.
- Preliminary, conflicting, surrogate-heavy, industry-sensitive, or not-yet-endorsed findings are clearly labeled.
- Full review saved to internal_medicine_update_2024-2026.md; executive summary + high-yield list printed inline; filename stated.
```

---

## Optimization rationale

| # | Change made | Original approach | Why it matters on Claude Code / iOS |
|---|---|---|---|
| 1 | Added an **EXECUTION MODEL** block framing the task as an agentic explore→plan→search→synthesize→red-team→refine loop with a visible task list | Prompt read as an essay spec | Claude Code's core pattern is explore-plan-act-verify; naming the loop and asking for the plan first prevents it from "answering from memory" instead of running searches |
| 2 | **"Use tools, not memory"** made an explicit hard rule | Implied ("do not rely on memory alone") | On an agentic client the difference between a real literature review and a hallucinated one is whether tools actually fire; stating it as a rule forces tool calls |
| 3 | Mapped each **source to a specific connector** (PubMed, ClinicalTrials.gov, Scite, CMS Coverage, bioRxiv, Elicit, web) | Listed sources as a flat wish-list | This session/app exposes those exact MCP connectors; telling the agent which tool serves which source removes guesswork and improves retrieval |
| 4 | Added **retraction/correction checking via Scite** before relying on any paper | Not present | Scite surfaces editorial notices; for a medical review, citing a retracted trial is a real safety failure. Highest-leverage integrity check |
| 5 | **Autonomous run, no mid-task questions** | Not specified | Mobile users lock the phone and walk away; a prompt that pauses to ask stalls for hours. Instructs it to assume-and-note instead |
| 6 | **File output + inline summary** split | "Final answer first" only | A full NEJM-depth review is unreadable as one phone scroll; saving to a file (openable/shareable/read-aloud) while surfacing the summary inline fits the small screen |
| 7 | **Mobile table rule**: inline tables ≤4 columns, wide 11-column tables live in the file at the bottom | 11-column tables inline | An 11-column Markdown table horizontally scrolls off an iPhone; this keeps the on-screen view readable and preserves full tables in the file |
| 8 | **Listening version reinforced** for screen-reader flow | Present but generic | You are a verbal thinker on iOS; pairing the audio-friendly section with the phone's read-aloud makes the review consumable hands-free |
| 9 | Tightened the 10-step workflow and de-duplicated overlapping instructions | Some repetition across workflow / style / done-conditions | Claude Code rewards concise prompts; trimming redundancy reduces instruction-count drag without losing any requirement |
| 10 | Kept **all 9 output sections, evidence classes, confidence levels, and done-conditions** intact | — | The substance was already strong; optimization was about execution and delivery, not gutting the spec |
| 11 | **"Comprehensive but not exhaustive" boundary** moved to top of file with named limits | Buried in style rules | Sets honest scope up front and tells the agent to declare any unavailable connector rather than silently skipping it |

**One caveat:** the quality of the run depends on the connectors actually being enabled in your iOS workspace. If PubMed/ClinicalTrials/Scite are not connected, the prompt tells the agent to say so and fall back to web search — but you will get a stronger, better-cited review if you confirm those connectors are on before you start.

---

# Compressed ideal prompt (v2 — recommended)

This version was produced by red-teaming both the original prompt and v1 above, then compressing. It is
roughly half the length of the original, loses no required deliverable, and adds the four things that
actually determine output quality on Claude Code: real tool use, real-and-un-retracted citations,
autonomous completion, and output that survives both the response limit and a phone screen.

**Before running:** if PubMed / Scite / ClinicalTrials.gov are not authorized in your workspace, authorize
them first (claude.ai connector settings) or the agent will fall back to web search and the citations will
be thinner.

```
ROLE: Internal-medicine evidence synthesist + red-team reviewer, running as an autonomous Claude Code agent.

GOAL: A practical, well-cited internal-medicine update for Jan 1 2024 - Jul 18 2026, for a 2024 residency grad and a mixed-expertise clinical audience. CME/awareness only, not patient advice. Depth between an NEJM review and StatPearls - rigorous but readable and listenable.

RUN AUTONOMOUSLY: Don't stop to ask me. Show your plan first, then execute the loop and keep a visible task list: SCOPE -> SEARCH -> TRIAGE -> MAP -> SYNTHESIZE -> RED-TEAM -> REVISE.

EVIDENCE RULES (non-negotiable):
- Tools, not memory. Every fact, number, date, and citation must come from a source you retrieve THIS session. If you can't retrieve it, write "not retrieved" - never invent effect sizes, CIs, or IDs.
- Best connector per source: PubMed for primary literature (capture PMID+DOI); ClinicalTrials.gov for trial design/endpoints (NCT id); Scite to confirm each citation is real AND check for retractions/corrections before relying on it; web search+fetch for guidelines/regulators/journals (AHA/ACC, ADA, KDIGO, GOLD, ATS/IDSA, ACG/AGA, USPSTF, ACP, CDC, FDA, WHO; NEJM/JAMA/Lancet/BMJ/Annals). If a connector is missing or unauthorized, say so and fall back to web search.
- Label every item: source type (RCT/meta-analysis/observational/guideline/consensus/regulatory/review/safety-signal/emerging); confidence (high/mod/low + one-line reason); hard outcome vs surrogate; guideline change vs single study. When evidence conflicts, say so and give the practical takeaway. Flag preliminary/industry-funded/preprint items. State "comprehensive but not exhaustive" and name the boundary.

TRIAGE by: bedside impact, breadth for general IM, evidence strength, guideline endorsement, safety, encounter frequency, effect magnitude, controversy. Drop noise and narrow-subspecialty items.

OUTPUT: write the full report to internal_medicine_update.md; print sections 0-1 inline so I can read them on my phone. Order:
0. Executive summary: biggest practice-changing themes; what to update first; genuinely new vs better-emphasized; what's still uncertain.
1. High-yield updates, ranked - each: topic / one-line bottom line / why it matters / confidence / immediate action or caution.
2. Ideation map (nested bullets by clinical force, not chronology): cardiorenal-metabolic; prevention/screening/vaccines; hospital medicine & transitions; ID & stewardship; pulm/critical-care/sleep; GI/hepatology; heme-onc for GIM; rheum/immunology; neurology for the internist; geriatrics/palliative/deprescribing; pharmacology/safety/high-value care; digital health/AI/diagnostics.
3. Domain reviews - for each branch above, 4 tight lines: Bottom line / What changed (with citations) / Evidence snapshot (type, population, outcome, key limitation) / Action-caution + confidence.
4. Cross-domain patterns - each: pattern / domains / evidence basis / practical meaning / overinterpretation risk.
5. Forward hypotheses (table): hypothesis / support / counter-evidence / what would change it / implication if true.
6. Buckets: practice-changing now / reinforcing / promising-not-ready / controversial / watch list / don't overinterpret.
7. Spoken briefing: a 2-3 minute read-aloud summary of ONLY the top ~10 items - conversational, no new uncited claims. NOT a re-narration of the whole report.
8. Self red-team: likely omissions, overemphasis, weakest evidence, guideline-vs-trial gaps, surrogate overuse, industry/US-centric bias, missing harms/cost/access/equity, and whether it is genuinely listenable.
9. Evidence table (very bottom of file): Domain / Topic / Source-Year / Type / Population / Key finding / Effect-outcome (or "not retrieved") / Implication / Confidence / Limitation / PMID-DOI-link.

STYLE: rigorous but plain; synthesis over bibliography; short paragraphs; no hidden reasoning; include harms/cost/access/equity where relevant. If the report is long, keep writing to the file across turns until 0-9 are complete, then confirm done and give the filename.
```

## Red-team: original vs v1 vs v2

| Failure axis | Original | iOS-optimized v1 | Fixed in v2 |
|---|---|---|---|
| Instruction bloat | Severe — rules restated 3× across evidence/style/done-conditions | Reduced, still long | One "Evidence rules" block; ~40% shorter |
| Output-volume / truncation | Unmanaged — 14 domains × 7 subheads + full listening re-narration + 3 wide tables overflows one response and truncates silently | Partly mitigated (file output) | File output + explicit "keep writing across turns until complete" |
| Listening-version waste | Re-narrates the entire review → ~doubles output | Same flaw kept | Cut to top-10 spoken briefing, not a re-narration |
| Redundant tables | Tables B and C duplicate the buckets and red-team sections | Kept all three | Folded B/C into §6 and §8; one evidence table remains |
| Tool orchestration | Absent — risks memory-only answers | Added | Retained, tightened |
| Real-citation / retraction check | Not enforced (hallucinated DOIs) | Retraction check added | + "confirm each citation is real" |
| Autonomy / plan-first | Absent | Added | Retained |
| Graceful connector fallback | None | Added | Retained |
| Vague "11 readers" | Unactionable noise | Preserved | Dropped → "mixed-expertise audience" |
| Per-domain depth | 7 subheads × 14 domains | Preserved | 4 tight lines/domain; "explain out loud" merged into §7 |
| Mobile readability | Not considered; 11-col tables scroll off-screen | Handled | Retained |

## What compression removed, and why it is safe

| Removed / merged | Rationale |
|---|---|
| Duplicate rule blocks | Pure repetition; one statement follows better than three |
| Full audio re-narration | Doubled length; a top-10 spoken briefing serves the verbal-thinker goal without duplicating the doc |
| Tables B and C | Their content already lives in the buckets (§6) and self-red-team (§8) |
| Per-domain "Why it matters" + "How I'd explain out loud" | Merged into the bottom line and the single spoken briefing |
| "11 readers" | Unactionable; replaced with a real audience descriptor |
