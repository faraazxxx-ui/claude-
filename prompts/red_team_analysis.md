# Red-Team Analysis and Prompt Perfection Strategy

This document outlines the red-team analysis of the initial seven prompts and the strategy for creating perfected, more robust versions. It also synthesizes the research on Genspark Super Agent and Genspark Claw to develop new, optimized prompts for these platforms.

---

## I. Red-Team Analysis of Original Prompts

Based on the research into red-teaming methodologies, each of the original prompts was analyzed for vulnerabilities, ambiguities, and inefficiencies. The following weaknesses were identified.

### 1. Claude Chat Prompt

*   **Vulnerability**: **Implicit Trust in Data**. The prompt assumes all provided data files are clean and correctly formatted. It lacks a pre-processing or validation step, which could lead to errors if a CSV has a malformed header or unexpected data type.
*   **Ambiguity**: The instruction `[PASTE YOUR NEW CSV DATA OR ATTACH FILES HERE]` is ambiguous for an AI. A perfected prompt should specify how the AI should handle file attachments vs. pasted text.
*   **Inefficiency**: The prompt is very long. While Claude has a large context window, the medical model and historical baseline could be further condensed and structured for better attention allocation.

### 2. Perplexity Computer Prompt

*   **Vulnerability**: **Source Reliability**. While it prioritizes good sources, it also allows searching patient forums (`Reddit r/POTS`). This could introduce anecdotal or unverified information into a medical research synthesis without a strong enough guardrail to differentiate it.
*   **Ambiguity**: The term "actionable recommendations" is subjective. A perfected prompt should define what constitutes "actionable" (e.g., specific, measurable, evidence-based).

### 3. Gemini Deep Research Prompt

*   **Vulnerability**: **Overly Broad Scope**. The research question is extremely complex, touching on four distinct, deep medical topics. This risks a shallow, unfocused report. A perfected prompt would break this into more targeted research questions, possibly for separate Deep Research runs.
*   **Inefficiency**: The prompt repeats a lot of the same context from the Claude prompt. A more efficient approach would be to have a single, master context document and reference it.

### 4. Gemini Gem System Instructions

*   **Vulnerability**: **Static Baseline**. The `HISTORICAL BASELINE` is hardcoded. As new data is analyzed, this baseline will become outdated. A perfected Gem instruction would include a mechanism for the Gem to update its own baseline over time.
*   **Ambiguity**: The instruction to "Flag any values that represent a significant deviation (>1 SD)" is good, but it doesn't specify the time period over which to calculate that standard deviation.

### 5. Google NotebookLM Prompts

*   **Vulnerability**: **Citation Hallucination**. The research indicates that NotebookLM can still struggle with accurate, consistent citations. The prompts don't include a strong enough self-correction mechanism to enforce citation accuracy.
*   **Inefficiency**: The prompts are sequential but don't build on each other's outputs. A more advanced workflow would have Prompt 2 use the summary from Prompt 1, and so on.

### 6. Manus AI Prompt

*   **Strength**: This prompt is already quite robust because it defers to a skill (`/health-data-analyst`), which is the correct pattern for complex, repeatable tasks in Manus.
*   **Weakness**: The skill itself, as created, is a good first version but could be improved. The `process_health_data.py` script is simple; a more robust version would handle more data sources, perform data validation, and merge data more intelligently.

### 7. Grok Heavy Prompt

*   **Vulnerability**: **Source Bias**. The prompt specifies searching Twitter/X and Reddit, which are prone to misinformation. While useful for sentiment, the prompt needs a stronger instruction to weigh peer-reviewed sources more heavily than social media anecdotes.
*   **Ambiguity**: The `SIGNAL vs. NOISE assessment` is subjective. A perfected prompt would provide clearer criteria for what constitutes a 
signal (e.g., multiple independent sources, clinical trial data) vs. noise (e.g., isolated anecdotes, unverified claims).

---

## II. Synthesis of Genspark Platform DNA

Based on the parallel research, here is the synthesized DNA for the two new Genspark platforms.

### Genspark Super Agent

*   **Architecture**: A project-managing Super Agent that coordinates over 15 specialized agents (e.g., AI Chat, AI Image, AI Code). It decomposes a final goal into sub-tasks and delegates them.
*   **Prompt DNA**: **Outcome-oriented**. The user should specify the final, desired end state, not the process. The Super Agent is best for complex, multi-faceted projects that require multiple skills (e.g., "Create a marketing campaign for my new product, including a blog post, social media images, and a launch video script").
*   **Anti-Patterns**: Using the Super Agent for simple, single-skill tasks (e.g., "write a sentence about cats"). This is inefficient and wastes credits. For simple tasks, directly invoke the specialized agent.
*   **Unique Edge**: An integrated multi-agent system in a single workspace, removing the need to switch between different AI tools.

### Genspark Claw

*   **Architecture**: An "AI employee" operating in a dedicated, isolated cloud computer environment for each user. This provides high security and data privacy. It integrates with messaging apps for instruction.
*   **Prompt DNA**: **Delegation-based**. Interact with it like a human employee via natural language in a chat interface. Delegate outcomes, not tasks. For example, instead of "Open the spreadsheet and sum column B," you would say, "Analyze the sales data from the Q1 report and give me the total revenue."
*   **Anti-Patterns**: Micromanaging with step-by-step instructions. Treating it like a simple chatbot for text generation.
*   **Unique Edge**: **Privacy-by-isolation**. The dedicated cloud computer for each user is a major security advantage over open-agent platforms, making it suitable for enterprise use with sensitive data.

---

## III. Strategy for Perfected Prompts

Based on the red-team analysis and new platform research, the following strategy will be used to create the final, perfected prompts:

1.  **Create a Master Context Document**: A single, comprehensive `medical_context.md` file will be created. All prompts will reference this file instead of repeating the context, making them shorter and more efficient.
2.  **Add Data Validation Steps**: Prompts for data analysis (Claude, Manus) will include an initial step to validate the structure and integrity of the input data files.
3.  **Strengthen Guardrails**: Prompts for research (Perplexity, Grok) will have stronger instructions to differentiate between peer-reviewed evidence and anecdotal reports, and to explicitly state the source type for every claim.
4.  **Increase Specificity**: Vague instructions will be replaced with precise, measurable criteria (e.g., defining "actionable recommendations," specifying the time period for SD calculations).
5.  **Introduce Dynamic Baselines**: The Gemini Gem prompt will be updated to include a mechanism for the Gem to update its own historical baseline over time.
6.  **Build Inter-Prompt Workflows**: The NotebookLM prompts will be rewritten to be a true chain, where the output of one prompt becomes the input for the next.
7.  **Develop New Genspark Prompts**: Two new prompts will be created from scratch for Genspark Super Agent and Genspark Claw, leveraging their unique outcome-oriented and delegation-based DNA.
8.  **Refine Output Formats**: All output formats will be made even more structured and specific to ensure consistent, machine-readable results where appropriate, and human-readable results.
