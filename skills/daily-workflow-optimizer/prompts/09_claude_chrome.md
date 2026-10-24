# Claude on Chrome

## Optimized Prompt

```text
<instructions>
Your primary goal is to analyze my current note-taking and productivity workflow, identify its flaws, and then implement an optimized, automated system using my preferred tools. This involves creating a new daily note structure, integrating various applications, and automating the capture of AI-generated content.
</instructions>

<steps>
1.  First, navigate to onenote.com and examine my notes to understand how I currently structure my handwritten plans. Take a screenshot of a recent daily plan.
2.  Next, navigate to notion.so and create a new, private workspace. Inside this workspace, create a new database named "AI Knowledge Base" with the following columns: `Title` (Text), `Source` (Select: Grok, Claude, Gemini), `Topic` (Multi-select), `Created Date` (Date), `YAML` (Text), and `Content` (Text).
3.  Then, create a new page in Notion titled "Daily Note Template." Structure this page with the following sections as H2 headings: "Yesterday's Wins," "Areas for Improvement," "Today's Goals," and "Today's Events."
4.  Now, propose a detailed workflow automation plan in a Google Doc. This plan should address how to:
    a.  Translate my handwritten notes from OneNote into the structured "Daily Note Template" in Notion.
    b.  Automatically capture my conversations from AI platforms and populate the "AI Knowledge Base" in Notion.
    c.  Use NotebookLM to visualize or interact with the content stored in the Notion knowledge base.
    d.  Integrate my calendar by leveraging features I like from tools such as North Plan or Priority Tree.
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

## Why This Works

This prompt is optimized for Claude on Chrome by using a structured XML format with `<instructions>`, `<steps>`, and a mandatory `<safety>` section, which aligns with the agent's core processing requirements. The clear, numbered steps provide a logical sequence for browser-based actions, while the request for screenshots at key milestones serves as a critical verification pattern. This approach guides the agent through a complex, multi-app workflow, ensuring it acts cautiously and seeks confirmation before performing high-stakes actions, which is essential for an agent that interacts directly with live web applications.
