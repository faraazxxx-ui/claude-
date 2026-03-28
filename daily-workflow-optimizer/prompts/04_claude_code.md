# Claude Code

## Optimized Prompt

```text
My goal is to build a new, automated personal productivity system. I've outlined my specific tool preferences, workflow logic, and desired outcomes in the attached CLAUDE.md file.

1.  **Explore:** Read the `CLAUDE.md` file to understand the complete project requirements and my personal preferences.
2.  **Plan:** Propose a step-by-step plan to build this system. The plan must address:
    *   Setting up a private Notion database as the central backend.
    *   Creating a script to capture handwritten notes from OneNote/Whiteboard.
    *   Automating the capture of AI chat logs into Notion.
    *   Designing a unified, nodal viewing interface (like Obsidian/NotebookLM) that reads from the Notion backend.
3.  **Implement (First Step):** Write a Python script that uses the Notion API to create the initial database structure as defined in `CLAUDE.md`. Write a failing test for this script first.

**Verify:** The Python script successfully creates the specified Notion database and the test passes.

**Roadblock Protocol:**
If you hit a roadblock:
1.  Interrupt and ask for clarification.
2.  Re-read `CLAUDE.md` to ensure you haven't missed a constraint.
3.  Spawn a subagent to research a specific API (e.g., OneNote OCR, Notion API).
```

## Why This Works

This prompt is optimized for Claude Code by using the platform's preferred explore-plan-implement workflow, which encourages structured problem-solving for complex tasks. It externalizes persistent user preferences into a `CLAUDE.md` file to keep the prompt concise and focused, and it incorporates test-driven development (TDD) by asking for a failing test first, which is a key optimization for generating reliable code on this platform.
