# Manus AI

## Optimized Prompt

```text
Analyze my current note-taking and personal knowledge management (PKM) workflow, identify flaws, and build a new, automated system that integrates my preferred tools. The final output should be a report detailing the new system architecture and a `todo.md` file that Manus can execute to implement the system.

## Requirements
1.  **System Analysis:** Analyze the provided description of my current tools (OneNote, Google Keep, Obsidian, Bear, etc.) and identify workflow inefficiencies and integration gaps.
2.  **Daily Note Automation:** Create a daily note automation that generates a new note each day with the following sections:
    *   Things that went well yesterday (3 points)
    *   Things I could improve from yesterday (3 points)
    *   Goals of today (3 tasks)
    *   Events of today (3 items)
3.  **Handwriting-to-Text:** Develop a workflow to convert handwritten notes and drawings from Microsoft OneNote or Whiteboard on a Windows Surface into the structured digital daily note.
4.  **AI Chat Aggregation:** Set up a new, dedicated Notion workspace. Create an automation to automatically capture the final output from all my AI chats (e.g., Grok, Claude, Gemini) and save them as new pages in this Notion database. Each page must include YAML frontmatter detailing the source, date, and topic.
5.  **PKM Visualization:** Create a method to visualize the aggregated notes from the Notion database in a nodal graph format, similar to Obsidian's graph view. This should be a readable output, like an image or a web page.
6.  **Unified Viewer:** Integrate the Notion database with Google's NotebookLM to provide a unified interface for viewing and interacting with the notes, including its audio-visual features.

## Constraints
*   I must not need to manually access the Notion database; it should serve only as a backend for the system.
*   The system should prioritize visual and spatial interaction (e.g., graph views, handwriting).
*   Pause and ask for confirmation before any action that incurs a cost or makes an irreversible change to my existing data.

## Deliverable
*   `/home/ubuntu/pkm_system_report.md`: A Markdown document detailing the analysis of my old workflow and the architecture of the new, automated system.
*   `/home/ubuntu/todo.md`: A detailed, step-by-step plan that you will follow to build and deploy this system.

## Verification
*   I will verify success by reviewing the `pkm_system_report.md` for a clear plan and then observing the successful execution of the `todo.md` file, resulting in a functional, automated note-taking system.
```

## Why This Works

This prompt works well for Manus AI because it is structured as a clear, imperative task with specific, verifiable deliverables (`pkm_system_report.md`, `todo.md`). It breaks down a complex, multi-step project into numbered requirements, which allows Manus to plan and execute the task systematically. By specifying concrete file names and a verification step, the prompt enables Manus to self-check its work and ensures the final output meets the user's explicit goals.
