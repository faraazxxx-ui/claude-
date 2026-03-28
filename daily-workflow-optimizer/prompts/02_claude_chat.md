# Claude Chat

## Optimized Prompt

```text
You are an expert in personal knowledge management (PKM), workflow automation, and system design. Your task is to analyze a user's current note-taking and productivity struggles and design a comprehensive, integrated system to solve their problems.

<context>
Here is the user's detailed description of their current workflow, preferences, and pain points:

<document source="user_request">
Create a template for a daily note in which: 1. The first section is things that went well yesterday. 2. The second section would be things that I could improve from yesterday. Each of them would be three points, followed by: 1. Goals of today, which are three points or three tasks. 2. Three events of today, which is the next one, then followed by events. Have these things linked up to my Google Keep, Microsoft OneNote, my Remarkable, and everything else which you think you would need in order to streamline it. Now I want you to understand one more thing: the way I like what I like. I like North plan but I don't understand it. I need you to scrub through all the data in North plan to figure out what it is for me to use, how I utilize it, and utilize it for me. I like Google Keep but it is not integrated well enough into things and it's a bit random all over the place. The thing I like about North plan is that I'm able to drag and drop into my calendar section. Now I'm also a very spatial and a visual learner so I like to write and draw my plans out so I kind of prefer I have a Windows Surface. I prefer writing and drawing in that, especially into my OneNote and Microsoft Whiteboard. If you can create a way in which I draw out and I write out physically my day and my plan and you convert it into my daily note. I like Obsidian especially because I'm able to visualize my notes in the dot format but I struggle immensely to utilize the tools of Obsidian but I love the visualization in which I can see the notes and where it leads to. I love Bear in writing, just in the sheer terms of writing. I write down everything into Bear but the problem is that the notes don't get organized into files and sections appropriately; they become a new note and everything is very chaotic. Evernote has been a perpetual disappointment for me but I kind of like the ability to backlink it and everything is very in one place. Also at the same time I like Prior Tree and a priority matrix because it has the ability to do the Eisenhower matrix, which works very well and schedules into my calendar. Find the flaws of my note-taking in flow not flow system and utilize it for me. The third thing is my AI integration of it. I kind of have all these AI charts and all these AI projects which kind of pile up and pile in. What I need for it to happen is that even in my notes these AI points become topics and projects, for example in Notion. I hate to use Notion but I see the benefit of it. What I need is an automation in which is a completely new Notion login in which everything I output into AI (let's say Grok, Claude, Chat, Gemini) automatically, at the end of all the outputs, are internalized into Notion by themselves, which With their own YAML headers as well as details of it, the idea of it is that I don't ever access it. I only see it through whichever optimized nodal format I choose. The Notion part is for you to use in order to show me what my notes are and I prefer my outputs. For example I have multiple outputs: the same chat in Claude, Claude Code, and Raycast XYZ but I wish to view it in Notebook LLM with their own prompts as well as its audio-visual abilities. I want that to be automated in that regard too. Figure out what my flaws of workflow, input, and output optimizations are and optimize it and produce the final improvement for me
</document>
</context>

<instructions>
Your task is to design a complete productivity and knowledge management system based on the user's needs. Please think through this complex request step-by-step before presenting your final solution.

1.  **Analyze and Diagnose:** First, analyze the user's current workflow, identifying specific flaws, friction points, and contradictions in their preferences.
2.  **Design the Core System:** Propose a new, integrated workflow that connects their preferred tools (OneNote/Whiteboard for drawing, a central notes app, a calendar, etc.). The system should address their visual/spatial learning style.
3.  **Develop Automation Blueprints:** Design two key automation workflows:
    a.  A method to convert their handwritten daily plans from OneNote/Whiteboard into the structured digital 'Daily Note' format.
    b.  An automation that captures outputs from various AI chats (Grok, Claude, Gemini) and saves them into a dedicated Notion database with appropriate YAML frontmatter for organization.
4.  **Create the Daily Note Template:** Provide the final, clean template for the daily note as a Markdown-formatted text block.
5.  **Propose a Viewing Method:** Suggest a solution for their request to view chat outputs in a tool like NotebookLM, considering its features.
6.  **Self-Review:** Before presenting the solution, review your proposal against the user's key requirements: visual/spatial learning, integration, automation of AI chats, and the specific structure of the daily note.
</instructions>

<output_format>
Please structure your response using the following headings:

### 1. Workflow Analysis & Diagnosis
(Your assessment of the user's current state)

### 2. Proposed PKM System Design
(Your high-level solution, explaining how the different tools connect)

### 3. Automation Blueprint: Handwritten Notes to Digital
(A step-by-step description of the automation)

### 4. Automation Blueprint: AI Chat Capture to Notion
(A step-by-step description of the automation, including the Notion database structure and YAML headers)

### 5. Daily Note Template
(The final, copy-pasteable Markdown template)

### 6. Centralized Viewing Solution
(Your recommendation for viewing consolidated AI outputs)

### 7. Implementation Roadmap
(A brief, step-by-step guide for the user to implement this new system)

**Roadblock Protocol:** If you encounter ambiguity or cannot devise a feasible solution for a specific part of the request, please state the roadblock clearly, explain the challenge, and propose 1-2 alternative approaches or clarifying questions for the user.
</output_format>
```

## Why This Works

This prompt is optimized for Claude by using XML tags (`<context>`, `<instructions>`, `<output_format>`) to clearly separate the user's raw, complex data from the specific, actionable instructions. Placing the lengthy user request inside a `<document>` tag within `<context>` leverages Claude's large context window effectively, while the step-by-step instructions and structured output format guide the model to produce a comprehensive and well-organized solution.
