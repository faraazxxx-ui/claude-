# Perfected Prompts: Red-Team Analysis & Remediation

**Author:** Manus AI
**Date:** March 28, 2026

This document presents the final, perfected prompts for the Daily Workflow Optimizer task across 10 AI platforms. The initial optimized prompts were subjected to a rigorous red-team analysis evaluating structural integrity, anti-pattern compliance, safety gaps, verification completeness, specificity, and platform DNA alignment.

---

## 1. Red-Team Audit Summary

The parallel red-team analysis identified several vulnerabilities in the first-pass prompts, which have now been remediated:

| Platform | Key Vulnerability Identified | Remediation Applied |
| :--- | :--- | :--- |
| **Manus AI** | Missing `Goal` header; safety check omitted from verification. | Restructured to exact DNA; added explicit safety verification step. |
| **Claude Chat** | Lacked a concrete verification plan for the end-user. | Added a "Verification & Testing Plan" section to the output format. |
| **Claude Co-work** | Missing safety guardrails for the automation script. | Added a "Safety & Security" constraint to the Quality Criteria. |
| **Claude Code** | Overloaded `CLAUDE.md` anti-pattern; vague file references. | Removed `CLAUDE.md` reference; specified exact filenames (`notion_setup.py`). |
| **Grok Heavy** | Missing `<role>` tag; lacked a verification section. | Added `<role>` tag for routing; added a `<verification>` section. |
| **Perplexity Pro** | Deviated from strict `focus` and `sources` keywords. | Re-formatted to strictly use the required keywords. |
| **Perplexity Computer** | Used wrong format DNA; micromanaged tool selection. | Rewritten to use `End-State` -> `Requirements` -> `Deliverable` format. |
| **Comet Agent** | Underutilized the `@tab` feature; vague completion criteria. | Explicitly required `@tab` usage for research; defined concrete deliverable. |
| **Claude on Chrome** | Ambiguous instructions regarding "North Plan" and Notion setup. | Clarified workspace naming and required specific feature investigation. |
| **Gemini Browser** | Missing `<verification>` section; mixed XML and Markdown. | Added a concrete `<verification>` checklist; fixed formatting consistency. |

---

## 2. Perfected Prompts

Below are the perfected, copy-paste-ready prompts for each platform.

### 2.1 Manus AI

```text
## Goal

Analyze my current note-taking and personal knowledge management (PKM) workflow, identify flaws, and build a new, automated system that integrates my preferred tools. The final output should be a report detailing the new system architecture and a `todo.md` file that Manus can execute to implement the system.

## Requirements

1.  **System Analysis:** Analyze the provided description of my current tools (OneNote, Google Keep, Obsidian, Bear) and identify workflow inefficiencies, data silos, and integration gaps.
2.  **Daily Note Automation:** Create a daily note automation that generates a new note each day with the following sections:
    *   Things that went well yesterday (3 points)
    *   Things I could improve from yesterday (3 points)
    *   Goals of today (3 tasks)
    *   Events of today (3 items)
3.  **Handwriting-to-Text:** Develop a workflow to convert handwritten notes and drawings from Microsoft OneNote or Whiteboard on a Windows Surface into the structured digital daily note.
4.  **AI Chat Aggregation:** Set up a new, dedicated Notion workspace. Create an automation to automatically capture the final output from all my AI chats (e.g., Grok, Claude, Gemini) and save them as new pages in this Notion database. Each page must include YAML frontmatter detailing the source, date, and topic.
5.  **PKM Visualization:** Create a method to visualize the aggregated notes from the Notion database in a nodal graph format, similar to Obsidian's graph view. This should be a readable output, like an image or a web page.
6.  **Unified Viewer:** Integrate the Notion database with Google's NotebookLM to provide a unified interface for viewing and interacting with the notes, including its audio-visual features.

## Deliverable

*   `/home/ubuntu/pkm_system_report.md`: A Markdown document detailing the analysis of my old workflow and the architecture of the new, automated system.
*   `/home/ubuntu/todo.md`: A detailed, step-by-step plan that you will follow to build and deploy this system.

## Verification

*   **Report Review:** I will review the `pkm_system_report.md` to ensure the analysis is accurate and the proposed architecture is sound.
*   **Execution and Functionality:** I will observe the successful execution of the `todo.md` file, resulting in a functional, automated note-taking system that meets all specified requirements.
*   **Safety Check:** I will confirm that the system paused and asked for confirmation before any action that incurred a cost or made an irreversible change to my existing data.
```

### 2.2 Claude Chat

```text
You are an expert in personal knowledge management (PKM), workflow automation, and system design. Your task is to analyze a user's current note-taking and productivity struggles and design a comprehensive, integrated system to solve their problems.

<context>
Here is the user's detailed description of their current workflow, preferences, and pain points:

<document source="user_request">
Create a template for a daily note in which: 1. The first section is things that went well yesterday. 2. The second section would be things that I could improve from yesterday. Each of them would be three points, followed by: 1. Goals of today, which are three points or three tasks. 2. Three events of today, which is the next one, then followed by events. Have these things linked up to my Google Keep, Microsoft OneNote, my Remarkable, and everything else which you think you would need in order to streamline it. Now I want you to understand one more thing: the way I like what I like. I like North plan but I don't understand it. I need you to scrub through all the data in North plan to figure out what it is for me to use, how I utilize it, and utilize it for me. I like Google Keep but it is not integrated well enough into things and it's a bit random all over the place. The thing I like about North plan is that I'm able to drag and drop into my calendar section. Now I'm also a very spatial and a visual learner so I like to write and draw my plans out so I kind of prefer I have a Windows Surface. I prefer writing and drawing in that, especially into my OneNote and Microsoft Whiteboard. If you can create a way in which I draw out and I write out physically my day and my plan and you convert it into my daily note. I like Obsidian especially because I'm able to visualize my notes in the dot format but I struggle immensely to utilize the tools of Obsidian but I love the visualization in which I can see the notes and where it leads to. I love Bear in writing, just in the sheer terms of writing. I write down everything into Bear but the problem is that the notes don't get organized into files and sections appropriately; they become a new note and everything is very chaotic. Evernote has been a perpetual disappointment for me but I kind of like the ability to backlink it and everything is very in one place. Also at the same time I like Prior Tree and a priority matrix because it has the ability to do the Eisenhower matrix, which works very well and schedules into my calendar. Find the flaws of my note-taking in flow not flow system and utilize it for me. The third thing is my AI integration of it. I kind of have all these AI charts and all these AI projects which kind of pile up and pile in. What I need for it to happen is that even in my notes these AI points become topics and projects, for example in Notion. I hate to use Notion but I see the benefit of it. What I need is an automation in which is a completely new Notion login in which everything I output into AI (let's say Grok, Claude, Chat, Gemini) automatically, at the end of all the outputs, are internalized into Notion by themselves, which With their own YAML headers as well as details of it, the idea of it is that I don't ever access it. I only see it through whichever optimized nodal format I choose. The Notion part is for you to use in order to show me what my notes are and I prefer my outputs. For example I have multiple outputs: the same chat in Claude, Claude Code, and Raycast XYZ but I wish to view it in Notebook LLM with their own prompts as well as its audio-visual abilities. I want that to be automated in that regard too. Figure out what my flaws of workflow, input, and output optimizations are and optimize it and produce the final improvement for me
</document>
</context>

<instructions>
Your task is to design a complete, actionable, and verifiable productivity and knowledge management system based on the user's needs. Please think through this complex request step-by-step before presenting your final solution.

1.  **Analyze and Diagnose:** First, analyze the user's current workflow, identifying specific flaws, friction points, and contradictions in their preferences.
2.  **Design the Core System:** Propose a new, integrated workflow that connects their preferred tools (OneNote/Whiteboard for drawing, a central notes app, a calendar, etc.). The system must address their visual/spatial learning style.
3.  **Develop Automation Blueprints:** Design two key automation workflows. For each, specify the tools required (e.g., Make.com, Power Automate) and the trigger/action steps.
    a.  A method to convert their handwritten daily plans from OneNote/Whiteboard into the structured digital 'Daily Note' format using OCR technology.
    b.  An automation that captures outputs from various AI chats (Grok, Claude, Gemini) and saves them into a dedicated Notion database. Define the specific YAML frontmatter to be used (e.g., `source_ai`, `chat_topic`, `creation_date`, `related_project`).
4.  **Create the Daily Note Template:** Provide the final, clean template for the daily note as a Markdown-formatted text block.
5.  **Propose a Viewing Method:** Suggest a concrete solution for their request to view chat outputs in a tool like NotebookLM, considering its features.
6.  **Self-Review:** Before presenting the solution, review your proposal against the user's key requirements: visual/spatial learning, integration, automation of AI chats, and the specific structure of the daily note.
</instructions>

<output_format>
Please structure your response using the following headings:

### 1. Workflow Analysis & Diagnosis
(Your assessment of the user's current state)

### 2. Proposed PKM System Design
(Your high-level solution, explaining how the different tools connect)

### 3. Automation Blueprint: Handwritten Notes to Digital
(A step-by-step description of the automation, naming specific tools and triggers)

### 4. Automation Blueprint: AI Chat Capture to Notion
(A step-by-step description of the automation, including the Notion database structure and specific YAML headers)

### 5. Daily Note Template
(The final, copy-pasteable Markdown template)

### 6. Centralized Viewing Solution
(Your recommendation for viewing consolidated AI outputs)

### 7. Implementation Roadmap
(A brief, step-by-step guide for the user to implement this new system)

### 8. Verification & Testing Plan
(Provide a checklist for the user to confirm the system is working. Example: '1. Handwritten Note Test: Draw a sample plan in OneNote. Does it appear in your notes app within 5 minutes? [ ] Yes [ ] No'. '2. AI Capture Test: Have a conversation with Claude. Does the transcript appear in Notion with the correct headers? [ ] Yes [ ] No'.)

**Roadblock Protocol:** If you encounter ambiguity or cannot devise a feasible solution for a specific part of the request, please state the roadblock clearly, explain the challenge, and propose 1-2 alternative approaches or clarifying questions for the user.
</output_format>
```

### 2.3 Claude Co-work

```text
## Goal
My primary goal is to establish a highly efficient, automated, and visually-integrated productivity system. This system must unify my note-taking and daily planning by converting handwritten thoughts into structured digital notes and automatically archiving all my AI chat interactions into a searchable Notion database. The final outcome should eliminate manual file organization and streamline my entire workflow across my preferred tools.

## Inputs
- **User Preferences & Workflow:** A detailed description of my current workflow, tool preferences (OneNote/Whiteboard, Bear, Obsidian), and pain points is located at `/home/ubuntu/input/user_preferences.txt`.
- **Handwritten Notes:** A directory of sample handwritten notes and drawings, saved as PNG or JPG images, is available at `/home/ubuntu/input/handwritten_notes/`.
- **Exported Digital Notes:** A collection of my existing notes exported from Bear and other platforms can be found at `/home/ubuntu/input/exported_notes/`.

## Output
1.  **Workflow Analysis Report:** A Markdown document named `Workflow_Analysis_Report.md` in `/home/ubuntu/output/`. This report must critically analyze my current system, identify specific flaws, and present a clear, evidence-based rationale for the proposed new workflow.
2.  **Daily Note Skill:** A reusable Manus Skill located in `/home/ubuntu/skills/daily-note/`. This skill must generate a new daily note Markdown file (`daily_note_YYYY-MM-DD.md`) with the following sections: 'Things that went well yesterday', 'Areas for improvement', 'Today’s goals', and 'Today’s events'.
3.  **Notion Automation Script:** A well-documented, standalone Python script (`notion_automation.py`) and its `requirements.txt` file, placed in `/home/ubuntu/output/notion_automation/`. This script will automatically capture all my outputs from Grok, Claude, and Gemini, and then create new, cleanly formatted pages in a dedicated Notion database. Each page must include YAML frontmatter for `source_ai`, `timestamp`, and `topic`.
4.  **System Integration Guide:** A comprehensive `README.md` file in the `/home/ubuntu/output/` directory. This guide must provide clear, step-by-step instructions on how to set up and use the entire integrated system, including the daily note skill and the Notion automation script.

## Quality Criteria
- **Verification:** The Notion Archiving Python automation script must correctly process a sample AI chat output, creating a corresponding, properly formatted page in the Notion database with all required metadata.
- **Tool Integration:** The proposed workflow must explicitly integrate OneNote/Microsoft Whiteboard for visual planning, Bear for writing, and an Obsidian-like nodal visualization, as detailed in my preferences.
- **Zero Manual Filing:** The final solution must be fully automated, requiring no manual organization of files or notes. All categorization and filing must be handled by the system.
- **Safety & Security:** The generated Python script must be secure and sandboxed. It must not contain any functionality that could delete files or access data outside of the specified input/output directories. All API keys or sensitive credentials must be handled securely and not hard-coded into the script.
```

### 2.4 Claude Code

```text
<Problem>
My goal is to create the initial database structure for a new personal productivity system using the Notion API. The database schema is defined in `notion_schema.json`.
</Problem>

<Files>
- `notion_setup.py`: The Python script to be created.
- `test_notion_setup.py`: The test file for the Python script.
- `notion_schema.json`: An existing file containing the database schema.
</Files>

<Test>
Write a failing pytest test in `test_notion_setup.py` that asserts the Notion database is created correctly according to the schema in `notion_schema.json`.
</Test>

<Verify>
The test in `test_notion_setup.py` must initially fail and then pass after the `notion_setup.py` script is implemented and successfully creates the Notion database.
</Verify>
```

### 2.5 Grok Heavy (16 Agents)

```text
<role>
You are a Master Systems Architect and Workflow Integrator agent. Your primary function is to analyze complex, disorganized productivity systems and engineer streamlined, automated, and practical workflows by integrating best-in-class tools and real-world user data.
</role>

<data_sources>
Search across: The public web, Twitter/X (full firehose), and Reddit.
Focus on: Best-practice guides, user-submitted workflows, and integration tutorials for the following tools: Obsidian, Notion, OneNote, Google Keep, Bear, Microsoft Whiteboard, and Eisenhower Matrix principles. Specifically search subreddits like r/ObsidianMD, r/Notion, r/OneNote, r/Productivity, r/PKMS (Personal Knowledge Management Systems), and r/workflow.
Time range: Past two years to ensure modern techniques are used.
</data_sources>

<task>
1.  **Analyze Current State:** Based on the context, produce a bulleted list of the primary flaws and friction points in the user's current workflow.
2.  **Design the Core Workflow:** Propose a new, integrated workflow that designates a primary role for each of the user's preferred tools (especially OneNote/Whiteboard for input, Notion for organization, and Obsidian for visualization). Justify why each tool is chosen for its specific role. Every recommendation must be supported by a source link from your search.
3.  **Create the Daily Note Template:** Design a detailed Markdown template for the user's "Daily Note." It must include the requested sections (Yesterday's Wins, Areas for Improvement, Today's Goals, Today's Events) and be structured for easy parsing.
4.  **Solve the Analog-to-Digital Problem:** Detail a specific, step-by-step process for how the user can write or draw their daily plan on their Windows Surface in OneNote and have it automatically converted and integrated into their Notion database. Specify the automation tool (e.g., Make.com or Zapier) and the OCR capabilities of the chosen tool.
5.  **Design the AI Integration Automation:** Architect a system where outputs from AI chats (Claude, Grok, Gemini) are automatically processed and saved as structured pages in a dedicated Notion database. Specify the required YAML frontmatter for each new page (e.g., `source_ai`, `topic`, `creation_date`, `summary`).
6.  **Specify the Visualization Method:** Explain how the user can connect their consolidated Notion database to a visualization tool (like Obsidian) to achieve the desired "dot format" or nodal graph view of their notes.
</task>

<output>
Produce a single, comprehensive report in Markdown format with the following sections:

# 1. Workflow Analysis & Diagnosis
(Bulleted list of identified flaws)

# 2. The Proposed Integrated Workflow
(Description of the new system, tool roles, and justifications with source links)

# 3. The Daily Note Template
(A code block containing the Markdown template)

# 4. Handwriting Integration Protocol
(Numbered steps for the Surface-to-Notion workflow)

# 5. AI Output Automation Architecture
(Description of the automation, including the trigger, action, and data mapping with YAML structure)

# 6. Knowledge Visualization Guide
(Numbered steps for connecting Notion to a visualization tool)

</output>

<failure_policy>
If you cannot find a reliable, well-documented integration method for a specific step, state "SOLUTION NOT FOUND" for that step and explain the technical limitations. Do not invent or assume solutions exist. Retry each search once before reporting a gap.
</failure_policy>

<verification>
After generating the report, create a final section titled "# 7. Verification Checklist". This section must contain a list of concrete, actionable steps the user can take to confirm that the proposed workflow and automations are configured correctly. For example: "Check if a new handwritten note in OneNote correctly creates a new page in the specified Notion database within 5 minutes."
</verification>
```

### 2.6 Perplexity Pro

```text
What is the optimal Personal Knowledge Management (PKM) methodology for a visual-spatial learner who needs to integrate handwritten notes from a Windows Surface, automate AI chat logs into a structured format with YAML headers, and implement the Eisenhower Matrix for task prioritization?

focus:
- A comparative analysis of methodologies like Zettelkasten, PARA, and Interstitial Journaling.
- Evaluation of their effectiveness in addressing the specified needs.
- Compatibility with tools known for strong visualization and integration capabilities, such as Obsidian, Roam Research, and Logseq.

sources:
- Academic research on cognitive science in note-taking.
- In-depth articles from established PKM expert blogs.
- Official documentation for software with robust API and plugin ecosystems.

anti-hallucination:
If reliable sources cannot be found for a specific part of the query, state that clearly rather than speculating.
```

### 2.7 Perplexity Computer

```text
## End-State

A fully automated, secure, and integrated personal knowledge management (PKM) and productivity system. This system will unify my daily planning, multi-platform note-taking, and AI-generated content into a single, visually intuitive workflow optimized for a spatial and visual learning style. The final state is a private, self-contained Notion workspace that eliminates disorganized notes by creating a seamless, automated flow between my handwritten plans, digital notes, calendar events, and AI chat outputs, with zero manual data entry required.

## Requirements
- **Central Daily Note**: A master daily note template in Notion that includes sections for: yesterday's wins, areas for improvement, today's top 3 goals (Eisenhower Matrix), and a synchronized view of today's calendar events.
- **Handwriting & Sketch Integration**: A fully automated workflow that captures all handwritten notes and sketches from Microsoft OneNote and Microsoft Whiteboard, performs OCR and image analysis, and intelligently files the transcribed text and images into the structured daily note in Notion.
- **Interactive Calendar**: The system must allow dragging and dropping tasks from the daily note directly onto a visual calendar, which then syncs with my primary Google Calendar.
- **AI Content Aggregation**: An automated process to capture all outputs from my interactions with AI models (Grok, Claude, Gemini) and file them into a dedicated 'AI Outputs' Notion database. Each entry must include the following YAML frontmatter: `source_model`, `interaction_date`, `topic_tags`, and a `summary`.
- **Visual Knowledge Graph**: The Notion workspace must feature a visual interface, similar to Obsidian's graph view, that displays the connections between notes, ideas, and tasks based on tags and links.
- **Task Prioritization**: Implement the Eisenhower Matrix for task prioritization. Tasks marked as 'Urgent & Important' in the daily note must be automatically highlighted and suggested for immediate calendar blocking.
- **Data Security**: All data processing and integration must occur in a secure, isolated environment. No personal data from my notes, calendar, or AI interactions shall be logged, stored, or transmitted outside of the designated Notion workspace. All connections must use end-to-end encryption.

## Deliverable
- A new, private Notion workspace fully configured with the entire automated system. This deliverable includes all necessary databases, templates, integrations, and a central dashboard for managing the PKM workflow.
- A comprehensive guide (as a Notion page within the workspace) that details the new workflow, provides step-by-step instructions for use, and explains the architecture of the automation. This document must also explicitly confirm that the security requirements have been met.
```

### 2.8 Comet Agent

```text
**Task:** I need you to design a new, streamlined, and automated workflow for my daily notes and AI project management. You will act as my research and systems design assistant to determine the best way to connect my applications and automate my key processes.

**Numbered Steps:**

1.  **Research Application Integrations.** Open a new @tab for each of the following applications: Obsidian, Bear, Evernote, and NotebookLM. In each tab, search their official website and help documentation for `API documentation`, `webhooks`, `Zapier integration`, and `Make.com integration`. I need to understand the specific technical methods available for connecting each app to external services.

2.  **Analyze Current Workflow Pain Points.** Based on your research, analyze the feasibility of solving my two primary challenges:
    *   **Challenge A:** Connecting handwritten notes and diagrams from my Windows Surface (using OneNote or Microsoft Whiteboard) into a central, searchable digital daily note.
    *   **Challenge B:** Automatically capturing and cataloging all my AI chat outputs (from Claude, Gemini, Grok) into a structured Notion database, complete with metadata such as `date`, `model_used`, and `topic`.

3.  **Design the Integrated Workflow.** Propose a new, integrated workflow in a Markdown document. This document must recommend one application as the central "hub" of my system. It must clearly explain, with diagrams if possible (using Mermaid.js syntax), how the other tools will bi-directionally sync or send data to this hub. The design should prioritize maximum automation.

4.  **Create a Daily Note Template.** Within the same Markdown document, create a template for my "Daily Note." It must include the following sections:
    *   `## What Went Well Yesterday`
    *   `## What I Can Improve Today`
    *   `## Today's Top 3 Goals (Eisenhower Matrix)`
    *   `## Today's Events & Meetings`
    *   `## Raw Inputs & Ideas`

**Roadblock Handling:** If you cannot find definitive API or integration information for a specific application after a thorough search, document the limitation clearly in the final report. Then, propose the next best alternative for that component of the workflow, explaining your reasoning.

**Completion Criterion:** The task is complete when you have created and saved a single Markdown file named `workflow_proposal.md` in my `/home/ubuntu/documents/` directory. This file must contain the full workflow design, the integration analysis for each app, and the complete "Daily Note" template as specified in the steps above. Do not provide a summary; the final file is the only deliverable required.
```

### 2.9 Claude on Chrome

```text
<instructions>
Your primary goal is to analyze my current note-taking and productivity workflow, identify its flaws, and then implement an optimized, automated system using my preferred tools. This involves creating a new daily note structure, integrating various applications, and automating the capture of AI-generated content.
</instructions>

<steps>
1.  First, navigate to onenote.com and analyze the structure of my three most recent daily plan notes. Identify recurring sections and common elements (e.g., task lists, meeting notes, habit trackers). Take a screenshot of one of these notes for reference.
2.  Next, navigate to notion.so and create a new, private workspace named "Automated Daily Workflow". Inside this workspace, create a new database named "AI Knowledge Base" with the following columns: `Title` (Text), `Source` (Select: Grok, Claude, Gemini), `Topic` (Multi-select), `Created Date` (Date), `YAML` (Text), and `Content` (Text).
3.  Then, create a new page in the "Automated Daily Workflow" workspace titled "Daily Note Template." Structure this page with the following sections as H2 headings: "Yesterday's Wins," "Areas for Improvement," "Today's Goals," and "Today's Events."
4.  Now, propose a detailed workflow automation plan in a Google Doc. This plan should address how to:
    a.  Translate my handwritten notes from OneNote into the structured "Daily Note Template" in Notion, based on the recurring elements you identified.
    b.  Automatically capture my conversations from AI platforms (Claude, Gemini, Grok) and populate the "AI Knowledge Base" in Notion.
    c.  Investigate and propose a method for using NotebookLM to visualize or interact with the content stored in the Notion knowledge base.
    d.  Sync events from my primary Google Calendar to the "Today's Events" section in the Notion Daily Note Template.
5.  After I approve the plan in the Google Doc, begin implementing the automation. Start by setting up the connection between my AI chat platforms and the Notion "AI Knowledge Base."
6.  Take a screenshot of the new Notion database and the daily note template to confirm they have been set up correctly.
</steps>

<safety>
- Pause and ask for my explicit permission before submitting any forms, making any purchases, or creating accounts on my behalf.
- Never enter or ask for my passwords. If a login is required, pause and notify me so I can handle it manually.
- Do not attempt to bypass any CAPTCHA or multi-factor authentication (MFA) prompts. Pause and wait for my intervention.
- If any step appears to modify or delete my personal data in an unintended way, stop immediately and ask for clarification.
- Take screenshots of key checkpoints, especially after creating new pages or databases, for verification.
</safety>
```

### 2.10 Gemini Browser

```text
<role>
    You are an expert productivity consultant and workflow automation specialist. You have deep knowledge of personal knowledge management (PKM) systems, note-taking applications (like Obsidian, Notion, OneNote, Bear), and API integrations for creating automated, cross-platform workflows.
</role>

<constraints>
    1.  You must design a complete, end-to-end workflow and system, not just a single template.
    2.  The solution must prioritize the user's preference for visual and spatial learning (drawing/writing on a Windows Surface).
    3.  The system must automate the capture, organization, and visualization of notes from multiple sources (physical writing, AI chats).
    4.  The user explicitly dislikes directly using Notion; it should only be used as a backend database, which is accessed through a different, preferred front-end.
    5.  The final output should be a detailed plan explaining the new workflow, the tools used, how they connect, and the rationale for each choice.
    6.  Rely ONLY on the provided context to understand the user's needs and pain points.
</constraints>

<context>
    User's Goal:
    To overhaul a chaotic note-taking and productivity system into a streamlined, automated workflow that aligns with their visual learning style and integrates their preferred (and disliked) applications effectively.

    Daily Note Structure Requirement:
    - Section 1: "Things that went well yesterday" (3 bullet points)
    - Section 2: "Things I could improve from yesterday" (3 bullet points)
    - Section 3: "Goals of today" (3 tasks)
    - Section 4: "Events of today" (3 events)

    Tool Preferences and Pain Points:
    - North Plan: Likes the drag-and-drop to calendar feature but does not understand the application well enough to use it.
    - Google Keep: Likes its simplicity but finds it poorly integrated and disorganized.
    - Windows Surface (OneNote/Whiteboard): Strongly prefers writing and drawing out plans physically.
    - Obsidian: Loves the graph/node visualization for seeing connections between notes but struggles to use the software's features.
    - Bear: Loves the writing experience but finds the organization chaotic as every entry becomes a new, disconnected note.
    - Evernote: Generally a disappointment, but likes the backlinking and having everything in one place.
    - Priority Tree/Eisenhower Matrix: Likes the ability to schedule tasks based on priority directly into a calendar.
    - Notion: Hates using it but recognizes its benefits as a structured database.

    Key Automation Requirements:
    1.  Physical to Digital: Create a method to convert the user's physical writing and drawings from their Windows Surface (in OneNote or Whiteboard) into the structured digital "Daily Note."
    2.  AI Chat Integration: Automatically capture the full output from AI chats (Grok, Claude, Gemini, Raycast) and save them into a new, dedicated Notion database. Each entry must include YAML frontmatter for metadata. The user must not need to interact with this Notion database directly.
    3.  Unified Viewing: The AI chat logs stored in Notion should be viewable through a preferred nodal interface (like Obsidian's graph view or NotebookLM), including the original prompts and any audio-visual content.
    4.  Tool Integration: The daily note system should link with Google Keep, Microsoft OneNote, and Remarkable.
</context>

<task>
    Based on the context provided above, your task is to perform a deep analysis of the user's workflow and design a comprehensive, automated, and personalized productivity and note-taking system. Your final output must be a detailed report that outlines this new system.

    Your report must address the following:
    1.  Flaw Analysis: Begin by identifying the core flaws and friction points in the user's current workflow.
    2.  Proposed Workflow: Describe the new, integrated workflow step-by-step. Explain how the user will move from planning their day (writing/drawing) to having their notes and tasks organized and visualized.
    3.  Tool Integration Plan: Detail which tools should be used and, crucially, how they will be connected. Specify the role of each tool in the new system (e.g., OneNote for input, Notion as a backend database, Obsidian for visualization).
    4.  Automation Strategy: Explain how the required automations (physical-to-digital conversion, AI chat capture) will be implemented. Suggest specific tools or services (e.g., Make/Integromat, Zapier, or custom scripts) to achieve this.
    5.  Addressing Ambiguity: Investigate the "North Plan" application to identify its core calendar and task management features. Propose a method to replicate its drag-and-drop calendar functionality using the selected tools. Design a visualization method for the Notion data that mimics Obsidian's graph view, showing connections between notes. Specify the tool and configuration needed to achieve this.
</task>

<verification>
    Before completing the report, verify the following:
    - [ ] The proposed solution uses a tool for physical writing/drawing on the Windows Surface.
    - [ ] The solution includes a method to convert handwriting to structured text for the Daily Note.
    - [ ] The solution automates the capture of AI chat logs to a Notion database.
    - [ ] The solution provides a way to view the Notion database content in a nodal format (like Obsidian).
    - [ ] The plan integrates Google Keep, Microsoft OneNote, and Remarkable.
    - [ ] The role of Notion is limited to a backend database, with no direct user interaction required.
    - [ ] The report includes a step-by-step workflow description.
    - [ ] The report details the specific tools and their connections.
    - [ ] The report explains the automation strategy, suggesting tools like Make/Zapier.
    - [ ] The report addresses the "North Plan" and "nodal format" ambiguities with concrete proposals.
</verification>

<final_instruction>
    Think step-by-step to construct the full workflow before writing the final report. Ensure your proposed solution directly addresses every pain point and requirement mentioned in the context. Use the verification checklist to confirm all requirements are met. Your final output should be the report itself, not the daily note template. Begin by outlining the flaws in the user's current system.
</final_instruction>
```
