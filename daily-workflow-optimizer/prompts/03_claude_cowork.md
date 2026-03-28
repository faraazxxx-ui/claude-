# Claude Co-work

## Optimized Prompt

```text
## Goal
Develop a personalized, automated productivity and note-taking system that unifies my preferred tools and workflows. The system should analyze my current processes, address the specified pain points, and create a streamlined, visually-oriented workflow that converts my handwritten notes into an organized digital format and automatically archives my AI chat histories.

## Inputs
- My workflow description and tool preferences are detailed in `/home/ubuntu/input/user_preferences.txt`.
- My handwritten notes and drawings will be uploaded as images (e.g., `.png`, `.jpg`) to `/home/ubuntu/input/handwritten_notes/`.
- My exported notes from Bear and other platforms are located in `/home/ubuntu/input/exported_notes/`.

## Output
1.  **Workflow Analysis Report:** A PDF document named `Workflow_Analysis_Report.pdf` in `/home/ubuntu/output/`. This report must detail the flaws in my current system and provide a clear rationale for the proposed new workflow.
2.  **Daily Note Skill:** Create a Manus Skill in `/home/ubuntu/skills/daily-note/` that generates my daily note template. The template should be a Markdown file (`daily_note_YYYY-MM-DD.md`) and include sections for 'Things that went well yesterday', 'Areas for improvement', 'Today’s goals', and 'Today’s events'.
3.  **Notion Automation:** A self-contained automation script or configuration that captures all my outputs from Grok, Claude, and Gemini. It must save them as new pages in a new, dedicated Notion database, complete with YAML frontmatter for metadata. The script and a README for setup should be placed in `/home/ubuntu/output/notion_automation/`.
4.  **System Guide:** A final `README.md` file in the `/home/ubuntu/output/` directory that explains how to use the new integrated system, including how to use the daily note skill and manage the automated Notion archive.

## Quality Criteria
- The system must successfully convert a test handwritten note from `/home/ubuntu/input/handwritten_notes/` into the structured daily note format.
- The Notion automation must correctly process a sample AI chat output and create a corresponding, properly formatted page in the Notion database.
- The final proposed workflow must integrate OneNote/Microsoft Whiteboard for visual planning, Bear for writing, and an Obsidian-like nodal visualization, as described in my preferences.
- The solution must not require me to manually organize files; the automation should handle all categorization and filing.
```

## Why This Works

This prompt is optimized for Claude Co-work because it is outcome-oriented, clearly defining the final deliverables (`Output`) and success metrics (`Quality Criteria`) without prescribing the specific steps to get there. It specifies exact input and output file paths, allowing Co-work to read from and write to the local file system directly. By requesting a reusable 'Skill' for the daily note, it leverages Co-work's ability to persist and automate recurring tasks, aligning perfectly with its strengths as a planning and execution agent rather than a simple chatbot.
