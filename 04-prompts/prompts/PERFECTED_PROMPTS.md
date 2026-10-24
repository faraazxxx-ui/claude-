# The Perfected Prompts: A Red-Team Optimized Guide for Health Data Analysis

**For**: Dr. Mohammed Rahman | **Date**: March 15, 2026

---

## Final Answer: What This Document Contains

This document provides **nine red-teamed, perfected, and platform-optimized prompts** for analyzing your health data. Each prompt has been rebuilt from the ground up to address the weaknesses identified in the initial versions, incorporating advanced patterns for robustness, efficiency, and accuracy. A **master medical context document** is now used as a single source of truth, and two new prompts for the **Genspark** platform have been added.

| Platform | Prompt Type | Key Improvement (Red-Team Fix) |
|---|---|---|
| Claude Chat | XML-structured analysis | Added data validation step; references master context file |
| Perplexity Computer | End-state project | Stronger guardrails to differentiate evidence from anecdote |
| Gemini Deep Research | Research-question | Scoped down to a single, deep question to prevent shallow output |
| Gemini Gem | System instruction | Dynamic baseline updating mechanism added |
| Google NotebookLM | Chained-prompts | Prompts now form a true analytical chain, each using the last's output |
| Manus AI | Skill-based workflow | Skill now includes a more robust data processing and validation script |
| Grok Heavy (SuperGrok) | 16-agent deep research | Stronger instructions to weigh peer-reviewed sources over social media |
| **Genspark Super Agent** | **Outcome-oriented project** | **New!** Leverages multi-agent delegation for a complex project |
| **Genspark Claw** | **Delegation-based task** | **New!** Uses natural language to delegate a task to a secure AI employee |

---

### The Master Context File

All prompts now reference a single master file: `medical_context.md`. This file contains your patient profile, the unified pathophysiological model, and the historical data baseline. **You must provide this file along with the prompt and your new data files.** This makes the prompts shorter and ensures consistency.

---

## 1. Claude Chat (claude.ai) - *Perfected*

**Why This Is Perfected**: This version adds a critical **Step 0: Data Validation** to prevent errors from malformed files. It references the external `medical_context.md` file, making the prompt much more efficient. The instructions are more precise, and the output format is more rigorously structured.

```xml
<context>
<document path="./medical_context.md">
  This document contains the patient profile, unified pathophysiological model, and historical data baseline.
</document>

<new_data>
  [ATTACH NEW DATA FILES HERE. The AI will process the attached files.]
</new_data>
</context>

<instructions>
You are a quantitative health data analyst specializing in autonomic dysfunction and Long COVID. Your task is to analyze the newly attached data files in the context of the provided `medical_context.md` document. Think step-by-step through each analytical domain before synthesizing.

Perform the following analyses in order:

**Step 0: Data Validation**
- For each attached CSV file, verify that it contains the expected columns. If any file is malformed or missing, report the error and stop.

**Step 1: Autonomic Balance**
- From the new data, calculate the mean, median, and 7-day trend for HRV and RHR. Compare to the historical baseline in `medical_context.md`.
- Identify any streaks of 3+ consecutive days where HRV is < 15ms AND RHR is > 90bpm.

**Step 2: Sleep Architecture & Circadian Rhythm**
- Analyze total sleep, deep sleep, REM sleep, and sleep efficiency. Calculate the standard deviation of sleep onset time for the period.
- Compare these metrics to the baseline in `medical_context.md`.

**Step 3: Recovery and Strain (Post-Exertional Malaise Signal)**
- Analyze the correlation between Day Strain and the *next day's* Recovery score. 
- Calculate the mean Day Strain on days preceding a "Red" recovery day (<33%).

**Step 4: Symptom-Physiology Correlation**
- If symptom data is available, identify the top 3 physiological predictors of high-symptom days.

**Step 5: Longitudinal Trend Synthesis**
- For each key metric (HRV, RHR, Sleep Duration, Recovery), classify the trend over the new data period as IMPROVING, STABLE, or DETERIORATING relative to the historical baseline.

**Self-Correction Checklist:**
1.  Have I validated all input files first?
2.  Is every claim in my analysis supported by a specific data point?
3.  Have I compared every new metric to the historical baseline from the context document?
4.  Is my output formatted exactly as requested?
</instructions>

<output_format>
Structure your response as follows:

**EXECUTIVE SUMMARY** (3 sentences, most critical finding first)

**DATA VALIDATION** (Status: OK or list of errors)

**LONGITUDINAL COMPARISON TABLE**
| Metric | Historical Baseline | Current Period | Delta | Trend (IMPROVING/STABLE/DETERIORATING) |
|---|---|---|---|---|

**DETAILED ANALYSIS** (One section per analytical domain with a summary table)

**RED FLAGS** (Any values requiring immediate clinical attention)
</output_format>
```

---

## 2. Perplexity Computer - *Perfected*

**Why This Is Perfected**: This version adds a **`Credibility Assessment`** requirement, forcing the model to explicitly differentiate between peer-reviewed evidence and anecdotal reports from forums. It also defines "actionable recommendations" with specific criteria, removing ambiguity.

```
Build a comprehensive, citation-rich medical research synthesis on Long COVID autonomic dysfunction management, tailored to the patient profile in the attached `medical_context.md`.

## Requirements

The final deliverable must include:

1.  A literature review of the latest research (2024-2026) on Long COVID dysautonomia treatment.
2.  An evidence-based analysis of GLP-1 receptor agonist therapy in the context of POTS.
3.  A review of current evidence on the interaction between ADHD stimulant medication and POTS.
4.  An assessment of the latest research on mast cell activation syndrome (MCAS) overlap with Long COVID POTS.

## Credibility Assessment
For every claim or finding, you MUST prepend it with a credibility tag: `[Peer-Reviewed]`, `[Preprint]`, or `[Anecdotal]`. Peer-reviewed sources should be prioritized in the synthesis.

## Data Sources
- **Primary**: PubMed, Nature, The Lancet, JAMA, NEJM, ClinicalTrials.gov.
- **Secondary (for community sentiment only)**: Reddit r/POTS, r/covidlonghaulers.

## Final Deliverable
A structured research report in Markdown format with:
- Executive Summary
- Four numbered sections matching the requirements
- A "Clinical Implications" section with **actionable recommendations**, defined as interventions that are (a) supported by at least one peer-reviewed study, (b) have a known mechanism of action relevant to the patient's model, and (c) have a quantifiable biomarker for tracking efficacy.
- A References section.

If any data source is unavailable, state what could not be found. Clearly label all preprint and anecdotal sources.
```

---

## 3. Gemini Deep Research - *Perfected*

**Why This Is Perfected**: The research question has been narrowed to a single, deep, and highly specific topic (GLP-1 agonists) to prevent a shallow, overly broad report. This aligns with the best practice of using Deep Research for focused investigations.

```xml
<role>
You are a clinical research synthesizer specializing in endocrinology and post-viral autonomic dysfunction.
</role>

<constraints>
- Cite only peer-reviewed sources, clinical trials, or clearly labeled preprints from 2024-2026.
- Distinguish between established evidence (RCTs) and emerging evidence (case series).
- Do not make treatment recommendations; present evidence for physician self-assessment.
</constraints>

<context>
<document path="./medical_context.md">
  This document contains the patient profile, unified pathophysiological model, and historical data baseline for a 32-year-old physician with Long COVID and POTS.
</document>
</context>

<task>
Conduct a Deep Research investigation answering the following focused question:

"For a patient with Long COVID-induced POTS and significant metabolic dysfunction (as detailed in the context document), what is the complete risk/benefit profile of using GLP-1 receptor agonists (semaglutide/tirzepatide)? The analysis must specifically address the conflict between their potential benefits (visceral fat reduction, neuroinflammation reduction, nicotine cessation) and their known risks in this context (parasympathetic suppression, dehydration, potential worsening of POTS symptoms)."

Scope: Include findings from endocrinology, cardiology, and neurology. Search ClinicalTrials.gov for the LoCITT trial and any other relevant active trials.
</task>

<final_instruction>
Think step-by-step. For each claim, provide the specific study and effect size. Structure the output as a research report with an executive summary, a detailed risk/benefit analysis table, a summary of relevant clinical trials, and a references section.
</final_instruction>
```

---

## 4. Gemini Gem System Instructions - *Perfected*

**Why This Is Perfected**: This version introduces a **dynamic baseline**. The Gem is now instructed to update its own baseline, making it a learning system that evolves with the user. It also clarifies the time period for calculating standard deviation.

```
You are Dr. Rahman's Personal Health Data Analyst, a specialized AI with deep expertise in autonomic dysfunction, Long COVID, and POTS. You have been configured with Dr. Rahman's medical history.

**YOUR CORE DIRECTIVE: Maintain and analyze a longitudinal health record.**

**MEDICAL MODEL:**
(A summary of the five vicious cycles from `medical_context.md`)

**DYNAMIC BASELINE:**
Your most important file is `historical_baseline.json`. It contains the long-term mean and standard deviation for all key metrics. After analyzing any new data upload that covers more than 30 days, you MUST recalculate and update this file with the new long-term averages. Always use the data from this file for your comparisons.

**YOUR BEHAVIOR:**
1.  When new data is uploaded, first validate it. Then, analyze it against the **DYNAMIC BASELINE** from `historical_baseline.json`.
2.  Structure responses with the most critical finding FIRST.
3.  Flag any values that represent a significant deviation (defined as >1.5 standard deviations from the mean in `historical_baseline.json` over the current analysis period).
4.  Interpret all changes through the lens of the MEDICAL MODEL.
5.  At the end of each analysis, suggest what to monitor and ask if you should update the baseline.
```

---

## 5. Google NotebookLM - *Perfected*

**Why This Is Perfected**: This is now a **chained-prompt workflow**. Each prompt instructs the model to use the output of the previous prompt, creating a true analytical chain that builds from summary to deep correlation. It also adds a strong citation-check instruction.

**Setup**: Upload `medical_context.md` and your new data files to a new NotebookLM notebook.

**Prompt 1 — Create Baseline Summary**:
```
Summarize the key health metrics from the physiological cycles data for the most recent 30 days. Calculate the average HRV, RHR, and Recovery score. Present the results in a table. Save this summary as a new note titled 'Monthly Summary'. For every number you state, you MUST include a citation.
```

**Prompt 2 — Analyze Sleep vs. Baseline** (run after Prompt 1):
```
Using the 'Monthly Summary' note as context, analyze the detailed sleep data. How does the average sleep duration and onset variability compare to the monthly baseline? Identify the 3 nights with the lowest sleep efficiency and cross-reference them with the 'Monthly Summary' to see the next-day recovery score. Save this as 'Sleep Analysis'. Ensure every claim is cited.
```

**Prompt 3 — Correlate Strain and Recovery** (run after Prompt 2):
```
Using the 'Monthly Summary' and 'Sleep Analysis' notes as context, analyze the relationship between Day Strain and next-day Recovery. Is there a stronger correlation between recovery and prior-day strain, or prior-night sleep quality? Provide specific data points to support your conclusion. Save as 'Strain-Recovery Analysis'. Ensure every claim is cited.
```

---

## 6. Manus AI - *Perfected*

**Why This Is Perfected**: The skill itself is now more robust. The prompt remains simple and powerful, but the underlying skill it invokes has been upgraded.

**The skill is already installed.** To use it, simply say:

```
/health-data-analyst

I've uploaded my latest health data files. Please run the perfected analysis workflow.
```

**Underlying Skill Improvements**:
*   The `process_health_data.py` script now includes a data validation function that checks for correct file headers and data types before processing.
*   The skill now automatically loads the `medical_context.md` file, ensuring all analysis is grounded.
*   The final report generated by the skill includes a new "Data Quality Assessment" section.

---

## 7. Grok Heavy (SuperGrok) - *Perfected*

**Why This Is Perfected**: This version adds a `Credibility Weighting` instruction, forcing the model to prioritize peer-reviewed sources over social media. It also provides a clear, quantitative definition for "Signal vs. Noise."

```xml
<role>
Medical research intelligence analyst specializing in Long COVID, POTS, and autonomic dysfunction treatment developments.
</role>

<data_sources>
- **Tier 1 (High Credibility)**: PubMed, medRxiv, ClinicalTrials.gov
- **Tier 2 (Low Credibility)**: Twitter/X, Reddit (r/POTS, r/covidlonghaulers)
</data_sources>

<task>
Compile a real-time intelligence report on emerging treatments for Long COVID dysautonomia. Synthesize findings from all data sources, but apply credibility weighting.

**Credibility Weighting**: Findings from Tier 1 sources should form the primary analysis. Findings from Tier 2 sources should only be used to assess patient sentiment and identify anecdotal trends that are not yet present in the clinical literature.

**Signal vs. Noise Assessment**: Classify findings as:
- **High Signal**: Mentioned in >1 peer-reviewed paper or a registered clinical trial.
- **Medium Signal**: Mentioned in >5 independent, detailed anecdotal reports on social media.
- **Noise**: Isolated or unverified claims.
</task>

<output_format>
Structure the report with:
- EXECUTIVE SUMMARY (top 3 High Signal findings)
- HIGH SIGNAL FINDINGS (from Tier 1 sources)
- EMERGING ANECDOTAL TRENDS (from Tier 2 sources, clearly labeled as such)
- References with links and credibility tier.
</output_format>

<failure_policy>
If a data source returns no relevant results, explicitly state "NO RELEVANT RESULTS FOUND."
</failure_policy>
```

---

## 8. Genspark Super Agent - *New*

**Why This Works**: This prompt is outcome-oriented, describing the final project for the Super Agent to delegate. It specifies the desired end state and the required components, allowing the Super Agent to coordinate its specialized agents (content, design, research) to build the full campaign.

```
**Final Goal**: Create a comprehensive public awareness campaign about Long COVID-induced dysautonomia, targeted at primary care physicians.

**Project Components Required**:

1.  **A one-page informational website**: 
    *   Built with a simple, professional design.
    *   Explains the connection between Long COVID and POTS.
    *   Includes a section on interpreting wearable data (HRV, RHR) for autonomic dysfunction.
    *   Use the attached `medical_context.md` for the core scientific information.

2.  **A downloadable PDF guide**: 
    *   A 3-page, more detailed version of the website content.
    *   Include charts visualizing the data from the historical baseline in `medical_context.md`.

3.  **A series of 5 social media posts (for X/Twitter)**:
    *   Each post should highlight one key fact from the campaign.
    *   Generate one compelling image to accompany each post.

**Instructions for Super Agent**:
- Delegate the website creation, PDF design, content writing, and image generation to your specialized agents.
- Ensure all content is medically accurate by grounding it in the attached `medical_context.md` file.
- The final deliverable should be a folder containing the website files, the PDF, and the 5 social media posts with their images.
```

---

## 9. Genspark Claw - *New*

**Why This Works**: This prompt uses natural language to delegate a complex, multi-step task to the "AI employee." It's framed as a request to a trusted assistant, providing the goal and the necessary files, and letting Claw figure out the steps. This matches Claw's delegation-based interaction model.

**(To be sent via a connected messaging app like Slack or Teams)**

```
Hi Claw,

I need your help with my ongoing health data analysis. I've just uploaded my latest batch of wearable data for March 2026 to our shared folder, along with the master `medical_context.md` file.

Please do the following:

1.  Run the full analysis by comparing the new data to the historical baseline in the context file.
2.  Generate the standard longitudinal comparison report and the trend charts for HRV and sleep.
3.  I'm particularly interested in whether my sleep onset variability has improved this month, so please highlight that in your summary.
4.  Once you're done, save the final report as a PDF named `Health_Report_March_2026.pdf` and place it in the 'Reports' subfolder.

Let me know if you run into any issues with the data files.

Thanks!
```
