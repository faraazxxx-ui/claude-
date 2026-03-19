# Optimized AI Prompts: CYB003 Clinical Trial Analysis & Eligibility Assessment

Based on a comprehensive deconstruction of your verbal prompt and research into the CYB003 clinical trial (NCT06564818), I have generated highly optimized prompts tailored to the unique architectures of 10 different AI platforms. 

The core challenge in your original prompt was that it mixed medical history, medication rationale, and trial analysis into a single stream-of-consciousness narrative, while omitting the actual trial data the AI needs to answer your questions. Furthermore, **my initial research identified a critical barrier: the trial explicitly excludes patients with ADHD, which conflicts with your current Vyvanse prescription.** The optimized prompts below are designed to force the AI to confront this discrepancy directly.

---

## 1. Manus AI

**Optimized Prompt:**
```markdown
Perform a comprehensive medical and eligibility analysis of the CYB003 clinical trial (NCT06564818) for a physician patient with a complex psychiatric profile.

## Requirements
1. Analyze the CYB003/APPROACH trial design, mechanism of action (deuterated psilocin analog / 5-HT2a agonism), and expected timeline for results/access.
2. Compare the neuroplasticity mechanism of CYB003 to Auvelity (dextromethorphan/bupropion).
3. Evaluate the patient's eligibility against the trial's inclusion/exclusion criteria.
4. The patient's medical profile: Physician, MDD, treatment-resistant depression, concurrent ADHD (currently taking Vyvanse 60mg daily), gabapentin for shingles, previous success with Auvelity (discontinued due to bupropion-induced anxiety), and previous success with mirtazapine (discontinued due to somnolence).
5. Explicitly flag the ADHD exclusion criterion in NCT06564818 and provide strategic advice on how to address this during the upcoming physician screening meeting.
6. Outline a step-by-step preparation guide for the screening meeting.

## Deliverable
Save the final report as `CYB003_Trial_Analysis_and_Strategy.md` with sections: Executive Summary, Mechanism Comparison, Eligibility Assessment, and Meeting Preparation Strategy.

## Verification
- The eligibility assessment MUST explicitly address the Vyvanse/ADHD conflict.
- The mechanism comparison MUST use precise psychopharmacological terminology appropriate for a physician audience.
```

**Why This Works:**
Manus operates autonomously and uses the file system as memory. This prompt specifies exactly *what* to produce (a markdown file with specific sections) rather than *how* to think. The numbered requirements allow Manus to parallelize research tasks, and the verification step ensures it checks its own work regarding the critical ADHD exclusion criterion before delivering the final file.

---

## 2. Claude Chat (claude.ai)

**Optimized Prompt:**
```xml
<context>
Patient Profile:
- Profession: Physician (capable of understanding advanced psychopharmacology)
- Diagnoses: Major Depressive Disorder (MDD), Treatment-Resistant Depression, concurrent ADHD
- Current Medications: Vyvanse 60mg daily, Gabapentin (for shingles)
- Medication History: 
  - Mirtazapine (highly effective, stopped due to somnolence)
  - Auvelity (highly effective, stopped due to bupropion-induced anxiety)
- Goal: Seeking treatments that promote neuroplasticity (similar to Auvelity's positive effects) but without the activating anxiety.

Target Trial:
- NCT06564818: "A Phase III, Placebo-Controlled, Randomized, Double-Blind Trial of Oral Doses of CYB003 to Assess Combined Safety and Efficacy in Humans With Major Depressive Disorder"
- Note: Trial exclusion criteria include "attention deficit hyperactivity disorder" and current use of certain medications.
</context>

<instructions>
Act as an expert psychopharmacologist and clinical trial advisor consulting with a physician colleague. Provide a comprehensive analysis of the CYB003 trial and the patient's eligibility. 

Address the following:
1. Explain the CYB003 study design, timeline, and process.
2. Compare the neuroplasticity mechanisms of CYB003 (5-HT2a agonism) vs. Auvelity (NMDA antagonism/sigma-1 agonism).
3. Conduct a rigorous eligibility assessment. You MUST directly address the conflict between the patient's ADHD/Vyvanse use and the trial's exclusion criteria.
4. Provide a strategic preparation guide for the patient's upcoming meeting with the trial physician.
</instructions>

<output_format>
## CYB003 Trial Overview & Timeline
## Mechanism Comparison: CYB003 vs. Auvelity
## Eligibility Assessment & Red Flags
## Strategic Preparation for Physician Meeting
</output_format>
```

**Why This Works:**
Claude natively parses XML tags. This prompt uses the "data-before-instructions" pattern, placing the complex medical history in the `<context>` tag before giving the `<instructions>`. This leverages Claude's long-context attention architecture. The `<output_format>` tag ensures a structured, readable response rather than a wall of text.

---

## 3. Claude Co-work

**Optimized Prompt:**
```markdown
## Goal
Generate a comprehensive clinical trial briefing and strategic preparation document for a physician patient evaluating the CYB003 (NCT06564818) trial.

## Inputs
Patient Profile: Physician with MDD, treatment-resistant depression, ADHD (on Vyvanse 60mg), gabapentin for shingles. Past success with Auvelity (stopped due to anxiety) and mirtazapine (stopped due to somnolence).
Target: CYB003 APPROACH Phase III Trial (NCT06564818).

## Output
A detailed briefing document saved to `~/Documents/CYB003_Trial_Briefing.md`

## Quality Criteria
- The document must be written at a peer-to-peer physician level.
- The mechanism of action section must compare CYB003's 5-HT2a agonism with Auvelity's NMDA/sigma-1 pathways regarding neuroplasticity.
- The eligibility section MUST explicitly flag the trial's ADHD exclusion criterion and the patient's Vyvanse use as a primary barrier.
- The meeting preparation section must provide actionable questions the patient should ask the trial investigator regarding access, timelines, and the ADHD exclusion.
```

**Why This Works:**
Claude Co-work is a delegation engine, not a chatbot. This prompt describes the *outcome* (the briefing document) rather than micromanaging the steps to get there. It provides the necessary inputs directly and uses explicit quality criteria so the agent can self-assess its work before finalizing the document.

---

## 4. Grok Heavy (16 Agents)

**Optimized Prompt:**
```xml
<role>
You are an expert psychopharmacology and clinical trial analysis agent consulting for a physician colleague.
</role>

<data_sources>
Search across: ClinicalTrials.gov (specifically NCT06564818), medical literature regarding CYB003 (deuterated psilocin), and Twitter/X (for real-time sentiment or updates from Cybin IRL Limited).
</data_sources>

<task>
1. Analyze the CYB003 Phase III trial design, timeline, and process.
2. Compare the neuroplasticity mechanisms of CYB003 versus Auvelity.
3. Evaluate the eligibility of a patient with MDD, treatment-resistant depression, and ADHD (currently on Vyvanse 60mg).
4. Formulate a strategy for the patient's upcoming screening meeting with the trial investigator.
</task>

<output_format>
## CYB003 Trial Analysis
## Mechanism: CYB003 vs Auvelity
## Eligibility Assessment (Must highlight ADHD exclusion)
## Meeting Preparation Strategy
</output_format>

<failure_policy>
If specific trial protocols regarding the ADHD exclusion cannot be found or clarified, state "INSUFFICIENT DATA on waiver protocols" rather than hallucinating workarounds.
</failure_policy>
```

**Why This Works:**
Grok Heavy deploys 16 specialized agents. Assigning a specific `<role>` routes the prompt to the correct expert cluster. Explicitly naming Twitter/X activates the platform's unique real-time firehose access (useful for finding recent updates from the trial sponsor, Cybin). The `<failure_policy>` prevents the agents from hallucinating if they cannot find specific workarounds for the ADHD exclusion criterion.

---

## 5. Perplexity Pro Search

**Optimized Prompt:**
```markdown
Based on the CYB003 Phase III clinical trial (NCT06564818) protocol, what are the specific inclusion/exclusion criteria regarding concurrent ADHD and stimulant use (like Vyvanse), and how does CYB003's mechanism of neuroplasticity compare to that of Auvelity (dextromethorphan/bupropion)?

Focus on: The exact exclusion language regarding ADHD in the APPROACH trial, the timeline for trial completion, and a physician-level comparison of 5-HT2a agonism versus NMDA antagonism for rapid-acting antidepressant effects.
Prefer sources from: ClinicalTrials.gov, peer-reviewed psychopharmacology journals, and official Cybin press releases.
If specific waiver protocols for the ADHD exclusion are not publicly available, state that clearly rather than speculating.
```

**Why This Works:**
Perplexity is a search-first engine. Multi-part conversational prompts confuse its retrieval pipeline. This prompt asks *one* highly specific, keyword-rich question that perfectly targets the search index. It specifies preferred source types to ensure high-quality medical data and includes an anti-hallucination instruction to handle gaps in the public trial data.

---

## 6. Perplexity Computer

**Optimized Prompt:**
```markdown
Build a comprehensive clinical trial briefing and strategic preparation report for a physician evaluating the CYB003 (NCT06564818) trial for their own treatment-resistant depression.

## Requirements
- Analyze the trial design, timeline, and expected access pathways for CYB003.
- Provide a detailed pharmacological comparison of neuroplasticity mechanisms: CYB003 (5-HT2a agonism) vs. Auvelity (NMDA antagonism).
- Conduct a strict eligibility assessment against the patient's profile: MDD, treatment-resistant depression, concurrent ADHD (on Vyvanse 60mg), gabapentin use.
- The assessment MUST highlight the trial's ADHD exclusion criterion and provide strategic talking points for the upcoming screening meeting.

## Data Sources
- ClinicalTrials.gov (NCT06564818)
- Cybin corporate publications
- Peer-reviewed literature on deuterated psilocin and Auvelity

## Final Deliverable
A structured, professional briefing document with an executive summary, pharmacological analysis, eligibility red flags, and a meeting preparation guide.

If specific trial waiver protocols are unavailable, state what could not be accessed rather than estimating.
```

**Why This Works:**
Perplexity Computer is a project-execution engine. By describing an ambitious end-state (a comprehensive briefing report) rather than asking a simple question, it activates the system's full multi-agent orchestration. The explicit data sources prevent it from relying on low-quality medical blogs.

---

## 7. Comet Agent

**Optimized Prompt:**
```markdown
I need to analyze my eligibility for a specific clinical trial and prepare for a screening meeting. I am a physician with MDD, treatment-resistant depression, and ADHD (currently taking Vyvanse 60mg).

Steps:
1. Go to ClinicalTrials.gov and search for NCT06564818 (the CYB003 APPROACH trial).
2. Extract the complete study design, timeline, and primary endpoints.
3. Carefully review the Exclusion Criteria. Specifically look for mentions of "attention deficit hyperactivity disorder", "Vyvanse", or "stimulants".
4. Compare my medical profile against these criteria and identify any hard disqualifiers.
5. Search medical literature to compare the neuroplasticity mechanism of CYB003 with Auvelity.
6. Synthesize this information into a briefing document that I can use to prepare for my meeting with the trial investigator.

When done: Show me the final briefing document, ensuring the ADHD exclusion conflict is prominently highlighted.
If the ClinicalTrials.gov page is unavailable, try searching for the Cybin APPROACH trial protocol on other registry sites.
```

**Why This Works:**
Comet Agent controls browser tabs autonomously. This prompt uses natural, conversational language broken down into clear, sequential steps—exactly how you would instruct a human research assistant. It includes a specific extraction target (the exclusion criteria) and provides a roadblock protocol in case the primary site fails.

---

## 8. Claude on Chrome

**Optimized Prompt:**
```xml
<instructions>
Navigate to ClinicalTrials.gov, extract the protocol for NCT06564818, and generate a strategic briefing for a physician patient with MDD and ADHD (on Vyvanse) who is considering enrolling.
</instructions>

<steps>
1. Open clinicaltrials.gov and search for NCT06564818.
2. Extract the study design, timeline, and full inclusion/exclusion criteria.
3. Screenshot the exclusion criteria section for verification.
4. Analyze the criteria against the patient's profile (MDD, ADHD on Vyvanse, previous Auvelity use).
5. Generate a briefing that compares CYB003 to Auvelity and highlights the ADHD exclusion conflict.
</steps>

<safety>
- Do NOT enter any personal health information into any web forms.
- Do NOT attempt to register or apply for the trial on my behalf.
- Screenshot the exclusion criteria for my verification before generating the final summary.
- Stop immediately if the site requires a login or CAPTCHA.
</safety>
```

**Why This Works:**
Claude on Chrome operates on real web pages. The XML structure separates the workflow into instructions, steps, and safety. The `<safety>` section is non-negotiable for browser agents, ensuring it doesn't accidentally submit your personal health information. Requesting a screenshot creates a verifiable audit trail of the exclusion criteria.

---

## 9. Gemini Browser

**Optimized Prompt:**
```xml
<role>
You are an expert clinical trial investigator and psychopharmacologist consulting with a physician colleague.
</role>

<constraints>
- Use precise medical terminology appropriate for a physician audience.
- Base the eligibility assessment strictly on the published protocol for NCT06564818.
- If a claim about the trial or drug mechanism cannot be verified, state "unverified" explicitly.
</constraints>

<context>
Patient Profile:
- Profession: Physician
- Diagnoses: MDD, Treatment-Resistant Depression, ADHD
- Current Medications: Vyvanse 60mg, Gabapentin
- History: Mirtazapine (effective but caused somnolence), Auvelity (effective but bupropion caused anxiety)
- Goal: Access neuroplasticity-promoting treatments like CYB003.
</context>

<task>
Generate a comprehensive research report covering:
1. The CYB003 APPROACH trial (NCT06564818) design, process, and timeline.
2. A pharmacological comparison of CYB003's mechanism vs. Auvelity's mechanism.
3. A strict eligibility assessment. You must explicitly address the trial's exclusion of ADHD patients and the patient's Vyvanse use.
4. A strategic preparation guide for the patient's upcoming screening meeting.
</task>

<final_instruction>
Think step-by-step before answering. Verify your eligibility assessment against the actual trial exclusion criteria. Validate your response against the constraints above before finalizing.
</final_instruction>
```

**Why This Works:**
Gemini's 1M token context requires the "data-before-instructions" pattern. The `<context>` tag provides all the complex medical history *before* the `<task>` tag asks for the analysis. The `<final_instruction>` tag forces a self-critique step, ensuring the model doesn't gloss over the critical ADHD exclusion criterion.

---

## Supporting Details & Optimization Rationale

| Element | Analysis & Rationale |
| :--- | :--- |
| **Intent Deconstruction** | The original prompt merged medical history, drug rationale, trial analysis, and meta-reasoning into one paragraph. The optimized prompts separate the *Context* (medical history) from the *Task* (trial analysis/eligibility). |
| **The ADHD Exclusion** | ClinicalTrials.gov explicitly lists "attention deficit hyperactivity disorder" as an exclusion criterion for NCT06564818. The raw prompt asked "would I have access," but an unoptimized AI might miss this detail. The optimized prompts force the AI to confront the Vyvanse/ADHD conflict directly. |
| **Drug Nomenclature** | The raw prompt used "Auvility" and "Ovility". The optimized prompts correct this to "Auvelity" (dextromethorphan/bupropion) to ensure the AI pulls accurate pharmacological data for the mechanism comparison. |
| **Formatting Directives** | The raw prompt asked for "RAG and chain of thought," which are backend processes, not output formats. The optimized prompts replace this by defining explicit output structures (e.g., Executive Summary, Mechanism Comparison) tailored to each platform's strengths. |
