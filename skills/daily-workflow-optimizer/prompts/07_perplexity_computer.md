# Perplexity Computer

## Optimized Prompt

```text
Design and implement a fully automated, integrated personal knowledge management (PKM) and productivity system. This system will unify my daily planning, note-taking, and AI-generated content into a single, visually intuitive workflow that caters to my spatial and visual learning style. The goal is to eliminate chaotic, disorganized notes and create a streamlined process that connects my handwritten plans, digital notes, calendar events, and AI chat outputs.

## Requirements
- A central daily note template that includes sections for: yesterday's wins, areas for improvement, today's goals, and today's events.
- A workflow that captures my handwritten and drawn plans from my Windows Surface (in OneNote and Microsoft Whiteboard) and automatically converts them into the structured daily note.
- Integration that allows dragging and dropping tasks into a calendar, similar to North Plan's functionality.
- An automated process to capture all outputs from my interactions with AI models (Grok, Claude, Gemini) and file them into a dedicated Notion database. Each entry must include automatically generated YAML frontmatter with appropriate metadata.
- A visual interface, inspired by Obsidian's graph view and Bear's writing experience, to see the connections between my notes and ideas.
- Implementation of the Eisenhower Matrix from Prior Tree for task prioritization, linked directly to my calendar.
- A comprehensive analysis of my current workflow's flaws and a report detailing the new, optimized system.

## Data Sources
- **Note-Taking & Planning Tools**: Google Keep, Microsoft OneNote, Remarkable, North Plan, Microsoft Whiteboard, Obsidian, Bear, Evernote, Prior Tree.
- **AI Content Generators**: Grok, Claude, Gemini, Raycast.
- All analysis should be based on publicly available information regarding the APIs and integration capabilities of these tools.

## Final Deliverable
- A new, private Notion workspace configured with the entire automated system. This includes the necessary databases, templates, and a central dashboard for viewing and managing my notes, tasks, and AI-generated content.
- A detailed document (as a Notion page within the new workspace) that explains the new workflow, how to use it, and the rationale behind the design choices. This document must cite all sources used to determine API capabilities.

If any data source is unavailable or an integration is not technically feasible, state what could not be accomplished rather than speculating.

## Roadblock Protocol
If you encounter an issue:
1. Provide corrective feedback and refine the scope.
2. Break the task into smaller sub-projects.
3. Add more specific constraints to the problematic step.
```

## Why This Works

This prompt works for Perplexity Computer because it describes an ambitious, end-to-end project rather than a series of small steps, which allows the platform's orchestration agent to effectively decompose the task and assign it to specialized sub-agents (research, coding, etc.). By clearly defining the final deliverable (a configured Notion workspace) and specifying all data sources, it provides the necessary parameters for the agents to execute the project from description to delivery. The inclusion of a roadblock protocol and anti-hallucination instructions helps the system handle the complexity and potential dead ends of integrating multiple third-party applications.
