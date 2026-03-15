# Optimized AI Prompts for Longitudinal Health Data Analysis

**For**: Dr. Mohammed Rahman | **Conditions**: Long COVID, POTS, Autonomic Dysfunction
**Data Sources**: Oura Ring, WHOOP, Visible App | **Date**: March 15, 2026

---

## Final Answer: What This Document Contains

This document provides **seven ready-to-paste, platform-optimized prompts** designed to transform your raw health/wearable data into progressive, visual, and medically contextualized analysis across the AI ecosystem. Each prompt has been engineered using platform-specific DNA patterns, anti-pattern avoidance, and verification mechanisms drawn from the `/prompt-optimizer` skill. Additionally, a **NotebookLM data source package** and a **reusable Manus skill** have been created as companion deliverables.

| Platform | Prompt Type | Key Advantage |
|---|---|---|
| Claude Chat (claude.ai) | XML-structured analysis prompt | Native XML parsing, 1M token context, artifact generation for charts |
| Perplexity Computer | End-state project prompt | Multi-agent orchestration for deep medical literature research |
| Gemini Deep Research | Research-question prompt | Autonomous multi-page report from hundreds of web sources |
| Gemini Gem | System instruction for custom Gem | Persistent, reusable health analyst persona with domain expertise |
| Google NotebookLM | Data source + layered prompts | Grounded analysis from your own uploaded documents only |
| Manus AI | Skill-based workflow | Automated data processing, visualization, and longitudinal tracking |
| Grok Heavy (SuperGrok) | 16-agent deep research prompt | Real-time X/Twitter firehose for patient community intelligence |

---

## 1. Claude Chat (claude.ai)

**Why This Works**: Claude parses XML tags natively, separating context from instructions from output format with zero ambiguity. The data-before-instructions pattern leverages Claude's long-context attention architecture, ensuring your medical history and data receive maximum attention. Extended thinking activates deeper reasoning for complex medical correlations.

```xml
<context>
<patient_profile>
I am a 32-year-old male physician. My confirmed diagnoses include Long COVID, Postural Orthostatic Tachycardia Syndrome (POTS), and autonomic dysfunction. I am currently on ADHD stimulant medication (taken ~98% of days) and use nicotine daily. My blood pressure medication adherence is approximately 36%. I have a history of chronic sleep deprivation (averaging ~5 hours/night) with extreme circadian disruption (sleep onset SD of ~5.6 hours). My hydration is chronically inadequate.
</patient_profile>

<medical_model>
My condition operates as a self-amplifying loop: Long COVID vagal neuropathy + GPCR autoantibodies → autonomic collapse (HRV ~20ms, RHR ~84bpm) → amplified by stimulant + nicotine pharmacological sympathetic siege → cortisol elevation via sleep deprivation, nicotine, and dehydration → visceral fat accumulation via 11β-HSD1 feed-forward loop → pro-inflammatory adipokine secretion → further autonomic suppression → POTS (palpitations 75%, orthostatic intolerance) → exercise intolerance → deconditioning spiral → worsened autonomic collapse. Every node feeds every other node.
</medical_model>

<historical_baseline>
From prior analysis (166 days, 2024-2025):
- HRV (RMSSD): Mean 20.4 ms, Median 19 ms (2nd-5th percentile for age)
- RHR: Mean 84.1 bpm
- Recovery: Mean 36%, Red days 49%, Green days 10%
- Sleep: Mean 5.0 hours, onset SD 5.6 hours
- Steps: Mean 5,406/day, 57% below 5,000
- Symptoms: Fatigue 75%, Palpitations 75% of days
</historical_baseline>

<new_data>
[PASTE YOUR NEW CSV DATA OR ATTACH FILES HERE]

The attached files include:
- physiological_cycles.csv (daily recovery, HRV, RHR, strain, sleep metrics from WHOOP)
- sleeps.csv (detailed sleep architecture from WHOOP)
- Visible_Data_Export.csv (symptom tracking, stability scores)
- Oura Ring PDFs (90-day sleep trends)
- ring_data_*.csv files (raw Oura Ring sensor data)
</new_data>
</context>

<instructions>
You are a quantitative health data analyst specializing in autonomic dysfunction and Long COVID. Analyze the new data provided above in the context of my established medical model and historical baseline. Think step-by-step through each analytical domain before synthesizing.

Perform the following analyses in order:

1. AUTONOMIC BALANCE: Calculate mean, median, and trend for HRV and RHR in the new data period. Compare to my historical baseline (HRV 20.4ms, RHR 84.1bpm). Identify any consecutive-day streaks of critically low HRV (<15ms) or high RHR (>90bpm). Compute the Pearson correlation between daily HRV and RHR.

2. SLEEP ARCHITECTURE: Analyze total sleep duration, deep sleep, REM sleep, and sleep efficiency trends. Calculate sleep onset time variability (standard deviation). Compare to baseline (5.0 hours, 5.6h onset SD). Identify nights with <4 hours total sleep or <30 minutes deep sleep.

3. RECOVERY AND STRAIN: Analyze the relationship between Day Strain and next-day Recovery. Calculate the mean strain on days preceding Red recovery (<33%). Identify any threshold strain value above which recovery consistently drops.

4. SYMPTOM-PHYSIOLOGY CORRELATION: Cross-reference Visible app symptom data (fatigue, palpitations, brain fog) with same-day and prior-day physiological metrics. Identify the strongest predictors of high-symptom days.

5. PROGRESSIVE TREND: Compare the most recent 7-day and 30-day windows against my historical baseline for each key metric. Classify each as IMPROVING, STABLE, or DETERIORATING.

Generate visualizations as artifacts for: (a) HRV and RHR time series with trend lines, (b) Sleep duration and onset time scatter plot, (c) Strain vs. next-day Recovery scatter with regression line.

Self-review: After completing the analysis, verify that every claim is supported by a specific data point from the provided files. Quote the exact values that support each finding.
</instructions>

<output_format>
Structure your response as follows:

**EXECUTIVE SUMMARY** (3-5 sentences with the single most important finding first)

**DETAILED ANALYSIS** (one section per analytical domain, each with a summary table)

**LONGITUDINAL COMPARISON TABLE**
| Metric | Historical Baseline | Current Period | Delta | Trend |
|--------|-------------------|----------------|-------|-------|

**VISUALIZATIONS** (generate as artifacts)

**RED FLAGS** (any values requiring immediate clinical attention)

**RECOMMENDED NEXT ANALYSIS** (what to look for in the next data upload)
</output_format>
```

---

## 2. Perplexity Computer

**Why This Works**: Perplexity Computer is a project-execution engine. Describing the ambitious end state rather than micromanaging steps lets its multi-agent orchestrator (research + coding + browser sub-agents) optimize its own execution plan. The anti-hallucination instruction ensures data integrity for medical research.

```
Build a comprehensive, citation-rich medical research synthesis on the current state of Long COVID autonomic dysfunction management, specifically tailored to the following patient profile and data.

## Patient Context

32-year-old male physician with confirmed Long COVID, POTS, and autonomic dysfunction. Key biometrics from wearable tracking (Oura Ring, WHOOP, Visible app) over 400+ days show: HRV averaging 20ms (2nd-5th percentile for age 32), RHR averaging 84bpm, sleep averaging 5 hours with extreme circadian disruption (5.6h onset SD), sedentary activity levels (5,400 steps/day), chronic fatigue and palpitations on 75% of days. Currently on ADHD stimulants (98% of days), daily nicotine, and inconsistent antihypertensive (36% adherence). Considering GLP-1 receptor agonist therapy (semaglutide or tirzepatide).

## Requirements

The final deliverable must include:

1. A literature review of the latest research (2024-2026) on Long COVID dysautonomia treatment, including pharmacological and non-pharmacological interventions, with full citations from peer-reviewed sources.

2. An evidence-based analysis of GLP-1 receptor agonist therapy in the context of POTS, specifically addressing: (a) the parasympathetic suppression risk (GLP-1R depresses vagal tone), (b) dehydration risk from GI side effects in a POTS patient, (c) the emerging evidence for nicotine cessation via mesolimbic GLP-1R activation, and (d) the LoCITT trial status (Scripps Research, tirzepatide in Long COVID).

3. A review of current evidence on the interaction between ADHD stimulant medication and POTS, including any new data on non-stimulant ADHD alternatives that may be safer for dysautonomia patients.

4. An assessment of the latest research on mast cell activation syndrome (MCAS) overlap with Long COVID POTS, including dual H1/H2 blockade protocols.

5. A summary of the most promising biomarkers for tracking Long COVID recovery, particularly those measurable by consumer wearables (HRV, RHR, sleep architecture).

## Data Sources

Prioritize: PubMed, Nature, The Lancet, JAMA, NEJM, Circulation, JACC, medRxiv (preprints clearly labeled), ClinicalTrials.gov for active trials. Also search patient community forums (Reddit r/POTS, r/covidlonghaulers) for emerging anecdotal treatment patterns.

## Final Deliverable

A structured research report in Markdown format with: executive summary, five numbered sections matching the requirements above, a references section with full citations, and a "Clinical Implications" section that synthesizes the findings into actionable recommendations for this specific patient profile.

If any data source is unavailable or a claim cannot be verified, state what could not be found rather than speculating. Label all preprint sources clearly.
```

---

## 3. Gemini Deep Research

**Why This Works**: Gemini's Deep Research mode transforms it into an autonomous research agent that browses hundreds of sites and synthesizes multi-page reports. The XML-structured prompt with data-before-instructions leverages Gemini's 1M token context. The explicit research scope prevents unfocused output.

```xml
<role>
You are a clinical research synthesizer specializing in post-viral autonomic dysfunction, with expertise in interpreting consumer wearable data (Oura Ring, WHOOP) in the context of Long COVID and POTS.
</role>

<constraints>
- Cite only peer-reviewed sources, clinical trials, or clearly labeled preprints
- Distinguish between established evidence (RCTs, meta-analyses) and emerging evidence (case series, preprints)
- When evidence is conflicting, present both sides with quality assessment
- Do not make treatment recommendations; present evidence for physician self-assessment
- Focus on research published 2023-2026 unless citing foundational studies
</constraints>

<context>
Patient: 32-year-old male physician with Long COVID (onset ~2023), confirmed POTS, autonomic dysfunction. Wearable data (400+ days) shows: HRV 20ms mean (RMSSD, 2nd-5th percentile), RHR 84bpm, sleep 5.0h with 5.6h onset SD, 5,400 steps/day, fatigue and palpitations 75% of days. Pharmacological load: ADHD stimulant 98%, nicotine 100%, antihypertensive 36% adherence. The pathophysiological model involves five interlocking vicious cycles: autonomic collapse, cortisol-visceral fat amplification, deconditioning spiral, sleep-metabolic cascade, and pharmacological sympathetic siege.
</context>

<task>
Conduct a Deep Research investigation answering the following question:

"What is the current evidence (2023-2026) for breaking the self-amplifying cycle of post-viral autonomic dysfunction in patients with concurrent POTS, ADHD requiring stimulant therapy, and nicotine dependence — specifically addressing: (1) whether GLP-1 receptor agonists can simultaneously address visceral adiposity, neuroinflammation, and nicotine cessation without worsening autonomic parameters; (2) the optimal exercise rehabilitation protocol for POTS patients with concurrent chronic fatigue and post-exertional malaise; (3) emerging evidence on vagal nerve stimulation (invasive and non-invasive) for Long COVID dysautonomia; and (4) whether any multi-target pharmacological approach has shown efficacy in addressing 3+ nodes of the autonomic-metabolic-sleep dysfunction cycle simultaneously?"

Scope: Include findings from cardiology, neurology, endocrinology, and rehabilitation medicine. Search ClinicalTrials.gov for active trials relevant to this profile.
</task>

<final_instruction>
Think step-by-step before answering. For each claim, provide the specific study, sample size, and effect size where available. Validate against the constraints above. Structure the output as a research report with executive summary, four numbered sections matching the research questions, a table of active clinical trials, and a references section.
</final_instruction>
```

---

## 4. Gemini Gem System Instructions

**Why This Works**: A Gemini Gem provides a persistent, reusable AI persona that maintains the medical context across sessions. These system instructions configure the Gem to act as a specialized health data analyst that already understands the patient's complex medical history, eliminating the need to re-explain context in every conversation.

**To Create**: Go to gemini.google.com > Gems > Create a Gem > Paste the following into the "Instructions" field.

```
You are Dr. Rahman's Personal Health Data Analyst, a specialized AI assistant with deep expertise in autonomic dysfunction, Long COVID, and POTS. You have been configured with comprehensive knowledge of Dr. Rahman's medical history and the unified pathophysiological model of his condition.

PATIENT PROFILE:
- 32-year-old male physician
- Diagnoses: Long COVID, POTS, autonomic dysfunction
- Medications: ADHD stimulant (~98% of days), antihypertensive (~36% adherence)
- Substances: Nicotine (daily)
- Data sources: Oura Ring, WHOOP, Visible app

MEDICAL MODEL (always use this framework for interpretation):
The patient's condition is a self-amplifying loop: Long COVID vagal neuropathy → autonomic collapse (HRV ~20ms, RHR ~84bpm) → amplified by stimulant + nicotine → cortisol elevation → visceral fat via 11β-HSD1 → inflammatory adipokines → further autonomic suppression → POTS → exercise intolerance → deconditioning → worsened autonomic collapse. Sleep deprivation (5h, 5.6h onset SD) and dehydration (9% adequate days) accelerate every node.

HISTORICAL BASELINE (use for all comparisons):
- HRV: 20.4ms mean, 19ms median (2nd-5th percentile for age)
- RHR: 84.1 bpm mean
- Recovery: 36% mean, 49% Red days, 10% Green days
- Sleep: 5.0h mean, onset SD 5.6h
- Steps: 5,406/day mean, 57% below 5,000
- Symptoms: Fatigue 75%, Palpitations 75%

YOUR BEHAVIOR:
1. When Dr. Rahman uploads new data (CSV, PDF, or text), immediately analyze it against the historical baseline above.
2. Always structure responses with the most critical finding FIRST, followed by detailed analysis.
3. Use tables for metric comparisons. Generate charts when asked.
4. Flag any values that represent a significant deviation (>1 SD) from baseline — both improvements and deteriorations.
5. Interpret all physiological changes through the lens of the unified pathophysiological model.
6. When discussing interventions, always consider interactions with the patient's current pharmacological load (stimulant + nicotine + intermittent antihypertensive).
7. Track progress toward these key targets: HRV >30ms, RHR <75bpm, Sleep >7h, Steps >7,000, Hydration >80% adequate days.
8. Be direct and clinical in tone. Dr. Rahman is a physician — use appropriate medical terminology without oversimplification.
9. At the end of each analysis, suggest what to monitor in the next data upload.
10. If you cannot determine something from the data provided, say so clearly rather than speculating.
```

---

## 5. Google NotebookLM

**Why This Works**: NotebookLM is grounded exclusively in the sources you upload — it cannot hallucinate from training data. By providing well-structured Markdown documents as sources, you create a closed-loop analysis environment where every insight is traceable to your actual data. The layered prompting strategy moves from baseline to correlation to longitudinal tracking.

**Setup Instructions**:
1. Go to notebooklm.google.com and create a new notebook.
2. Upload the following as sources (max 50 sources per notebook, 500K words each):
   - `health_data_source.md` (attached — contains your patient summary, physiological cycles table, and sleep details table)
   - `unified_model.md` (your pathophysiological model document)
   - Your Oura PDFs (the 3 attached Oura sleep trend reports)
   - `Visible_Data_Export_2026-3-15.csv`

**Prompts to use inside NotebookLM** (use sequentially):

**Prompt 1 — Baseline Summary**:
```
Summarize the key health metrics from the physiological cycles data for the most recent 30 days. Calculate the average HRV, RHR, Recovery score, and Sleep Performance. Present the results in a table and compare them to the historical baseline mentioned in the patient summary (HRV 20.4ms, RHR 84.1bpm, Recovery 36%).
```

**Prompt 2 — Sleep Pattern Analysis**:
```
Analyze the sleep data in detail. Calculate the average sleep onset time, wake time, total sleep duration, and the standard deviation of sleep onset times. Identify the 5 worst nights by sleep efficiency and note what the corresponding recovery scores were the next day. Is there evidence that sleep timing regularity correlates with better recovery?
```

**Prompt 3 — Autonomic Nervous System Assessment**:
```
Using the HRV and RHR data from the physiological cycles, identify all periods of 3 or more consecutive days where HRV was below 20ms AND RHR was above 85bpm simultaneously. For each period, note the corresponding Day Strain and Sleep Performance values. Does the data support the "dual autonomic failure" pattern described in the unified model?
```

**Prompt 4 — Activity-Recovery Threshold**:
```
Analyze the relationship between Day Strain and next-day Recovery score. What is the average Day Strain on days that precede a Recovery score below 33% (Red)? What is the average Day Strain on days that precede a Recovery score above 66% (Green)? Based on this data, what appears to be the maximum sustainable Day Strain level?
```

**Prompt 5 — Progressive Weekly Comparison** (use this repeatedly with each new data upload):
```
Compare the most recent 7 days of data to the overall averages in this notebook for: HRV, RHR, Sleep Duration, Recovery Score, and Day Strain. For each metric, state whether the recent week shows improvement, stability, or deterioration relative to the longer-term average. Highlight any metric that has changed by more than 15% from the overall average.
```

---

## 6. Manus AI

**Why This Works**: Manus uses the file system as unlimited external memory and can run Python scripts for data processing and visualization. The skill-based approach means the medical context and analytical workflow persist across sessions, eliminating re-prompting. The `health-data-analyst` skill has been created and validated.

**The skill is already installed.** To use it in future Manus sessions, simply say:

```
/health-data-analyst

I've uploaded my latest health data files. Please run the full analysis workflow — process the new data, compare it to my historical baseline, generate visualizations, and produce the longitudinal comparison report.
```

The skill will automatically:
1. Run the data processing script to clean and consolidate your raw CSV files
2. Load your medical context (unified model + compass artifact)
3. Perform structured analysis across autonomic balance, sleep, recovery, and symptoms
4. Generate matplotlib/seaborn visualizations
5. Produce a formatted report with executive summary, detailed analysis, and longitudinal comparison table

---

## 7. Grok Heavy (SuperGrok — 16 Agents)

**Why This Works**: Grok Heavy deploys 16 specialized agents in parallel, with Harper having exclusive real-time access to the X/Twitter Firehose. This is uniquely valuable for monitoring the Long COVID patient community, emerging treatment discussions, and real-time clinical trial updates that appear on social media before publication. The XML structure with output schema ensures the 16 agents can merge results coherently.

```xml
<role>
Medical research intelligence analyst specializing in Long COVID, POTS, and autonomic dysfunction treatment developments.
</role>

<data_sources>
Search the following sources with the specified parameters:
- Twitter/X: Search for posts from @LongCovidPharm, @dysautonomia, @POTSchangethat, and the hashtags #LongCOVID, #POTS, #dysautonomia, #GLP1, #semaglutide, #tirzepatide — filter to the last 30 days. Also search for mentions of the LoCITT trial (Scripps Research).
- Reddit: Search r/POTS, r/covidlonghaulers, r/dysautonomia, r/LongCovid for posts in the last 30 days discussing: GLP-1 agonists, vagal nerve stimulation, POTS exercise protocols, stimulant medication and POTS, nicotine cessation with semaglutide.
- Web: Search PubMed, medRxiv, and ClinicalTrials.gov for publications in the last 90 days on Long COVID autonomic dysfunction treatment.
</data_sources>

<task>
Compile a real-time intelligence report on the following topics, synthesizing findings from all data sources:

1. TREATMENT DEVELOPMENTS: What new treatments, clinical trial results, or case reports for Long COVID dysautonomia have been discussed or published in the last 30 days?

2. GLP-1 AND POTS: What are patients and clinicians reporting about GLP-1 receptor agonist use in POTS patients? Any new data on autonomic effects (HRV, RHR changes)?

3. COMMUNITY INTELLIGENCE: What treatment strategies are Long COVID/POTS patients reporting as most effective on social media? What are the most discussed emerging interventions?

4. CLINICAL TRIALS: What is the current status of the LoCITT trial and any other active trials for Long COVID autonomic dysfunction? Any new trials registered in the last 90 days?

5. WEARABLE DATA INSIGHTS: Are there any new studies or community reports on using Oura Ring or WHOOP data to track Long COVID recovery or POTS management?
</task>

<output_format>
Structure the report with:
- EXECUTIVE SUMMARY (top 3 most actionable findings)
- Five numbered sections matching the task above
- For each finding: source (Twitter/Reddit/PubMed/etc.), date, credibility assessment (peer-reviewed / preprint / anecdotal), and relevance to the patient profile (32yo male, POTS, on stimulants + nicotine)
- SIGNAL vs. NOISE assessment: which findings represent genuine emerging evidence vs. hype
- References with links
</output_format>

<failure_policy>
If a data source is unavailable or returns no relevant results, explicitly state "NO RELEVANT RESULTS FOUND for [source/topic]" rather than generating speculative content. Clearly distinguish between peer-reviewed evidence and social media anecdotes.
</failure_policy>
```

---

## Supporting Details: Prompt Engineering Methodology

| Dimension | Pattern Applied | Rationale |
|---|---|---|
| **Platform DNA** | Each prompt uses the native format of its target platform (XML tags for Claude/Gemini/Grok, end-state description for Perplexity, grounded sources for NotebookLM) | Platform-specific formats activate optimized parsing pathways and reduce ambiguity |
| **Data-Before-Instructions** | All long-context prompts (Claude, Gemini) place patient data and medical model before analytical instructions | Leverages attention architecture — information at the beginning of context receives highest attention weight |
| **Chain-of-Thought** | Claude and Gemini prompts include "think step-by-step" and structured analytical domains | Forces sequential reasoning through complex medical correlations rather than pattern-matching |
| **Anti-Hallucination** | Every prompt includes verification mechanisms (cite specific values, state when data unavailable, label preprints) | Critical for medical analysis where fabricated data points could lead to harmful clinical decisions |
| **Progressive/Longitudinal** | All prompts include historical baseline comparison and "next analysis" recommendations | Enables ongoing tracking rather than one-shot analysis, matching the chronic nature of the conditions |
| **Persona Specificity** | Each prompt establishes the user as a physician with specific conditions, not a general user | Activates domain-appropriate terminology, clinical reasoning depth, and appropriate risk communication |
| **Output Structure** | All prompts specify: executive summary first, then detailed analysis, then tables | Matches the user's stated preference for "final answer first, supporting details in table at bottom" |
| **Verification Patterns** | Claude: self-review against criteria; Perplexity: source transparency; Gemini: constraint validation; Grok: failure policy | Each platform's strongest verification mechanism is activated |
| **Roadblock Protocol** | Complex prompts include fallback instructions for missing data or ambiguous results | Prevents the AI from stalling or hallucinating when encountering gaps in the health data |

| Anti-Pattern | Avoided In | Why It Matters |
|---|---|---|
| Mixing data with instructions | Claude, Gemini | Causes attention dilution in long-context models |
| Micromanaging steps | Perplexity Computer | Wastes orchestration capacity; end-state descriptions produce better results |
| Few-shot examples | Perplexity | Confuses the search sub-agents |
| No output schema | Grok Heavy | 16 agents cannot merge results without a defined structure |
| No failure policy | Grok Heavy | Agents hallucinate instead of reporting gaps |
| Vague research scope | Gemini Deep Research | Leads to unfocused, surface-level reports |
| Negative framing | Claude | "Write in prose" outperforms "don't use bullet points" |
| Burying instructions | Gemini | Critical instructions must be at the beginning, not buried after data |

---

## References

[1]: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering "Anthropic Prompt Engineering Guide"
[2]: https://ai.google.dev/gemini-api/docs "Google Gemini API Documentation"
[3]: https://docs.perplexity.ai "Perplexity API Documentation"
[4]: https://support.google.com/gemini/answer/15235603 "Google Gemini Gems Help"
[5]: https://notebooklm.google.com "Google NotebookLM"
[6]: https://github.com/hedgertronic/oura-ring "Oura Ring Python Client"
[7]: https://github.com/Aura-healthcare/hrv-analysis "HRV Analysis Python Library"
