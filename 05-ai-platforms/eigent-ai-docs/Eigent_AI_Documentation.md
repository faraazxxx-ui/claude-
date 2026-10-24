# Eigent AI Complete Documentation

This document contains the complete, compiled documentation from the Eigent AI website (https://docs.eigent.ai). It is structured to provide an AI agent with comprehensive knowledge of Eigent AI, its concepts, features, installation, and usage.

---

## Source: https://docs.eigent.ai/get_started/welcome

Welcome

- Models

On this page

**Eigent** is the world’s first **Multi-agent Workforce** desktop application, empowering you to build, manage, and deploy a custom AI workforce that can turn your most complex workflows into automated tasks.Built on CAMEL-AI’s acclaimed open-source project (CAMEL with 13k⭐ on GitHub, #1 on GitHub Daily Trending), our system introduces a **Multi-Agent Workforce** that **boosts productivity** through parallel execution, customization, and privacy protection. Previously #1 opensource project on GAIA.![Dynamic Workforce](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/thumbnail.png)

## [​](https://docs.eigent.ai/get_started/welcome\#core-features-and-capabilities)  Core Features and Capabilities

## Build Your Own Workforce

Customize your AI “workers” (agents) according to your industry or personal workflow needs. You have full control to create specialized Worker nodes with domain-specific skills and toolkits, assembling a workforce tailored to you.

## Dynamic Multi-Agent Collaboration

Eigent dynamically breaks down tasks and activates multiple agents to work **in parallel**, automating complex tasks much faster than traditional single-agent sequential workflows. This parallelism accelerates execution and handles flexible, multi-step scenarios with ease.

## Human-in-the-Loop

If a task gets stuck or encounters uncertainty, Eigent will automatically request human input. This safety net ensures critical decisions or errors are handled with human oversight, improving reliability.

## MCP Tools Integration (MCP)

Eigent comes with over 200 built-in **Model Context Protocol (MCP)** tools (for web browsing, code execution, etc.), and also lets you **install your own tools**. Equip agents with exactly the right tools for your scenarios – even integrate internal APIs or custom functions – to enhance their capabilities.

## 100% Open Source

Eigent is completely open-sourced. You can download, inspect, and modify the code, ensuring transparency and fostering a community-driven ecosystem for multi-agent innovation.

## Local Model Support

Deploy Eigent locally with your preferred models. Your data stays on **your own device**, addressing privacy and security concerns. You can use personal API keys or local LLMs so that sensitive information never leaves your environment.

[Installation\\
\\
Next](https://docs.eigent.ai/get_started/installation)

Ctrl+I

![Dynamic Workforce](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/thumbnail.png)

---

## Source: https://docs.eigent.ai/get_started/installation

Installation

- Models

On this page

1

[Navigate to header](https://docs.eigent.ai/get_started/installation#)

Download Eigent

Head to our official website to download the latest version.

- Download for macOS
- Download for Windows

```
<Warning>
  **macOS Prerequisite**
  Please ensure you are running macOS 11 (Big Sur) or a newer version to install Eigent.
</Warning>
```

2

[Navigate to header](https://docs.eigent.ai/get_started/installation#)

Install the Application

- **On macOS:** Open the downloaded `.dmg` file and drag the Eigent icon into your Applications folder.
- **On Windows:** Run the downloaded `.exe` installer and follow the on-screen instructions.

Once installed, launch Eigent and log in to get started!

## [​](https://docs.eigent.ai/get_started/installation\#next-steps)  Next Steps

You’re all set! Now that Eigent is installed, here are a few places you can go to learn more:

[**Quick Start** \\
\\
Jump right in and learn how to launch your first task.](https://docs.eigent.ai/get_started/quick_start)

[**Key Concepts** \\
\\
Understand the core terms and features that make Eigent unique.](https://docs.eigent.ai/core/concepts)

[**Support** \\
\\
Find answers to frequently asked questions.](https://docs.eigent.ai/troubleshooting/support)

[Welcome\\
\\
Previous](https://docs.eigent.ai/get_started/welcome) [Quick Start\\
\\
Next](https://docs.eigent.ai/get_started/quick_start)

Ctrl+I

---

## Source: https://docs.eigent.ai/get_started/quick_start

Quick Start

- Models

On this page

This guide will walk you through building your first multi-agent workforce using Eigent.

## [​](https://docs.eigent.ai/get_started/quick_start\#create-your-first-task)  Create Your First Task

Once opened, you’ll land on the **Task** page. It’s a clean space designed to turn your ideas into action. Let’s break down what you see.![Layout](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_firsttask.png)

### [​](https://docs.eigent.ai/get_started/quick_start\#the-top-bar)  The Top Bar

At the very top of the window is your main navigation bar. You’ll access:

- **Dashboard**: your home base for creating and viewing History and Ongoing tasks.

  - Project Archives: a detailed log of all your past tasks, including the token usage.
  - Ongoing Tasks
- **Settings:** where you can configure the app to your liking.

![Task Hub](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_thetopbar.png)

### [​](https://docs.eigent.ai/get_started/quick_start\#the-main-view)  The Main View

Your workspace is split into two panels:**Message Box (Left):** where you’ll chat with your AI workforce to start a job.

- Before running the task, you can Add, Edit, or Delete any subtask or Back to Edit your request, then resume. When tasks complete, you can use Replay to re-run the flow.![Message](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_themainview.gif)
- You can pause anytime—hit **Pause**, edit via **Back to Edit**, then resume. When tasks complete, use **Replay** to re-run the flow.![Message 2](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_pause.gif)

**Canvas (Right):** where your AI agents get to work.

- **Before a Task:** You’ll see your pre-built agents and and their tools. You can also click **\+ New Worker** to add your own. These workers will always be on standby for your task.
- **During a Task:** The Canvas shows the live status of all subtasks (`Done / In Progress / Unfinished`). Click any subtask to view detailed logs (reasoning steps, tool calls, results). More on this below.
![Task in Progress](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_canvas_inprogress.png)
- **Canvas Toolbar:** At the bottom of the Canvas, you’ll see a toolbar. This is where you manage your views of agents. You can switch between different task views, such as **Home**, **Agent Folder**, or a specific worker’s **Workspace**.
![Add Worker](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_canvas_bottom.png)

### [​](https://docs.eigent.ai/get_started/quick_start\#agent-folder)  Agent Folder

This is the filing cabinet for your workforce. Any files your agents create or use (like documents, spreadsheets, code, pictures, or presentations) are automatically saved here. These files are also stored locally on your computer and/or in your cloud for easy access.![Agent Folder](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_agentfolder.png)

#### [​](https://docs.eigent.ai/get_started/quick_start\#-note-on-file-storage)  📌 Note on File Storage

You can always find your task files in a dedicated folder on your machine.

- **Windows:**`C:\Users\[YourUsername]\eigent\[YourEmailPrefix]\task_[TaskID]`
- **Mac:**`/Users/[YourUsername]/eigent/[YourEmailPrefix]/task_[TaskID]`

Cloud version users: outputs are also saved in your cloud workspace according to your subscription tier. Visit the Support page for more details.

### [​](https://docs.eigent.ai/get_started/quick_start\#pre-built-agents)  Pre-built Agents

Eigent comes with four ready-to-work agents. Each is equipped with a specific set of tools and shines at specific tasks—click to explore:

1. **Developer Agent** – writes, debugs and executes code
2. **Browser Agent** – fetches and gathers info from the web
3. **Multimodal Agent** – ideals with images, videos and more
4. **Document Agent** – reads, writes and manages files (Markdown, PDF, Word, etc.)

![Pre-build Agents](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_prebuiltagents.gif)

### [​](https://docs.eigent.ai/get_started/quick_start\#add-your-own-workers)  Add your own workers

Click **“\+ Add Workers”**, provide:

- **Name** (required)
- **Description** (optional): the role of your customized agent
- **Agent Tool**: install any tool available from our MCP Servers to give your agent the exact skills it needs.

![Add Your Own Workers](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_addworker.gif)

## [​](https://docs.eigent.ai/get_started/quick_start\#start-your-first-task)  Start Your First Task

Now that you have a workforce, let’s put it to work.

### [​](https://docs.eigent.ai/get_started/quick_start\#step-1-define-your-goal)  Step 1: Define Your Goal

Type your task in the top Message Box. Be as descriptive as you like. For example, ask Eigent to conduct an UK healthcare market research . You can attach files (like docs, data, images) by clicking the **paperclip icon** in the Message Box.Then, hit **Send**.

### [​](https://docs.eigent.ai/get_started/quick_start\#step-2-review-subtask-flow)  Step 2: Review Subtask Flow

Once you send your task, our **Coordinator Agent** and **Task Agent** kick in to break it into subtasks. You’ll see:

- **Workforce CoT Box**: shows agent’s “Chain-of-Thought.” This tells you _how_ the AI interpreted your request and its reasoning path.
- **Task Status Box**: displays subtasks with controls. You can **add**, **edit**, or **delete** any subtask to make sure the plan is perfect. If you’re not happy with the plan, just click **“Back to edit”** to refine your initial request.

### [​](https://docs.eigent.ai/get_started/quick_start\#step-3-lauch-the-task)  Step 3: Lauch the Task

Once you’re happy with the plan, hit **Start Task.** Eigent will automatically assign each subtask to the best agent for the job based on the tools they have.![Launch the Task](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_lauchtask.gif)

## [​](https://docs.eigent.ai/get_started/quick_start\#watch-agents-work)  Watch Agents Work

Once the task starts, your agents will run in parallel on the Canvas:

- Click a subtask to view logs:
  - **Reasoning Steps:** The agent’s logic for how it’s approaching the subtask.
  - **Tool Calls:** Which specific tool the agent is using (e.g., `search_google`, `load_files`).
  - **Task Results:** The output or conclusion of the subtask.
- Hover over tasks to see status details

![Watch Agents Work](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_subtasklog.gif)Click on an agent icon to open its **Workspace**:

- Example 1: open **Browser Agent**, launch embedded browser

  - Use **“Take Control”** to take over browsing (e.g., accept cookies), then return control to the agent

![Browser Agent](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_takecontrol.gif)

- Example 2: open **Developer Agent**, lauch **Terminal**

![Developer Agent](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_terminal.gif)

### [​](https://docs.eigent.ai/get_started/quick_start\#human-in-the-loop)  **Human in the Loop**

Sometimes, an agent may needs your input to proceed with the subtask (e.g., confirmation or extra data). In this case, a request will pop up in the **Message Box**. Simply type your response and send it.

## [​](https://docs.eigent.ai/get_started/quick_start\#a-quick-tour-of-settings)  A Quick Tour of Settings

Click the gear icon in the top-right corner to open Settings. Here’s a brief overview.

### [​](https://docs.eigent.ai/get_started/quick_start\#general)  **General**

- **Account:** Manage your subscription or log out.
- **Language:** Choose between English, Simplified Chinese, or your System Default.
- **Appearance:** Switch between Light mode. On macOS, a Transparent mode is also available.

![General](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_general.png)

### [​](https://docs.eigent.ai/get_started/quick_start\#models)  **Models**

![Models](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_localmodel.png)

- **Cloud Version:** We provide pre-configured, state-of-the-art models, including GPT-4.1, GPT-4.1 mini and Gemini 2.5 Pro. Using these models is the easiest way to get started and will be billed to your account based on usage (credits).
- **Self-hosted Version:**You can connect your own models.

  - **Cloud Models:** Connect your personal accounts from providers like OpenAI, Anthropic, Qwen, Deepseek and Azure by entering your own API key.
  - **Local Models:** For advanced users, you can run models locally using Ollama, vLLM, SGLang, LM Studio, or LLaMA.cpp server.

### [​](https://docs.eigent.ai/get_started/quick_start\#mcp-servers)  **MCP Servers**

MCPs are the **tools** that give your agents their skills. We’ve pre-configured popular tools like Slack, Notion, Google Calendar, GitHub, and more in **MCP Market**, which you can install for your agents with a single click.![MCP Markets](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_mcp.png)For advanced users, you can click **Add MCP Server** to configure and install custom tools from third-party sources.![MCP Servers](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_addmcp.png)

## [​](https://docs.eigent.ai/get_started/quick_start\#next-steps)  Next Steps

Congratulations on running your first task! Here are a few recommended reads to deepen your understanding:

[**Key Concepts** \\
\\
Get familiar with the terms we use, like Workforce, MCP, and more.](https://docs.eigent.ai/core/concepts)

[**Your Workforce** \\
\\
Learn how to build and manage highly specialized custom agents.](https://docs.eigent.ai/core/workforce)

[**Models** \\
\\
Discover how to connect your own local or cloud-based AI models.](https://docs.eigent.ai/core/models/byok)

[Installation\\
\\
Previous](https://docs.eigent.ai/get_started/installation) [Concepts\\
\\
Next](https://docs.eigent.ai/core/concepts)

Ctrl+I

![Layout](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_firsttask.png)

![Task Hub](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_thetopbar.png)

![Message](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_themainview.gif)

![Task in Progress](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_canvas_inprogress.png)

![Add Worker](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_canvas_bottom.png)

![Agent Folder](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_agentfolder.png)

![Pre-build Agents](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_prebuiltagents.gif)

![Add Your Own Workers](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_addworker.gif)

![Launch the Task](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_lauchtask.gif)

![Watch Agents Work](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_subtasklog.gif)

![Browser Agent](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_takecontrol.gif)

![Developer Agent](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_terminal.gif)

![General](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_general.png)

![Models](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_localmodel.png)

![MCP Markets](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_mcp.png)

![MCP Servers](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/quickstart_settings_addmcp.png)

---

## Source: https://docs.eigent.ai/core/concepts

Concepts

- Models

On this page

## [​](https://docs.eigent.ai/core/concepts\#workers)  Workers

Autonomous agents tailored to specific roles that run tasks independently or together. Think of them as individual members of your team, like a “Researcher,” a “Programmer,” or a “Writer.”Each Worker is designed with specific capabilities and can be customized to handle particular types of tasks efficiently.![Workers concept illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_worker.png)

## [​](https://docs.eigent.ai/core/concepts\#workforce)  Workforce

A coordinated team of Workers that collaborate to complete complex workflows. Think of it as your AI project team.The Workforce orchestrates multiple Workers, ensuring they work together seamlessly to achieve your goals.![Workforce collaboration illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_workforce.gif)

## [​](https://docs.eigent.ai/core/concepts\#workspace)  Workspace

A live window into a Worker’s process where you can watch or take control. For example, a terminal, a browser, or a file viewer.Workspaces provide real-time visibility into what your Workers are doing, allowing you to monitor progress and intervene when needed.![Workspace interface illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_workspace.gif)

## [​](https://docs.eigent.ai/core/concepts\#tasks-&-subtasks)  Tasks & Subtasks

You define a mission (task), the Workforce breaks it into components (subtasks), and assigns them to the appropriate Workers.This hierarchical approach ensures complex projects are broken down into manageable pieces and executed efficiently.![Tasks and subtasks breakdown illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_tasks_subtasks.gif)

## [​](https://docs.eigent.ai/core/concepts\#chat)  Chat

Your primary interface for communicating with your Workforce. You use it to define your main Task, sharing files and interacting with agents in real time.The Chat interface serves as your command center, where you can give instructions, ask questions, and receive updates from your AI team.![Chat interface illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_chat.png)

## [​](https://docs.eigent.ai/core/concepts\#mcp)  MCP

Model Context Protocol that allows Workers to use external tools. It connects your agents to databases, APIs, and documentation sources, empowering them to act across platforms.MCP extends your Workers’ capabilities by providing access to real-world data and tools, making them more powerful and versatile.![MCP protocol illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_mcp.png)

## [​](https://docs.eigent.ai/core/concepts\#models)  Models

Different AI “brains” that power your Workers. Eigent allows you to choose from various models (like GPT-4.1 or Gemini 2.5 Pro), each with different strengths in speed, reasoning, and cost.Choose the right model for each task based on your specific needs for performance, accuracy, or cost efficiency.![AI models illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_models.png)

[Quick Start\\
\\
Previous](https://docs.eigent.ai/get_started/quick_start) [Workforce\\
\\
Next](https://docs.eigent.ai/core/workforce)

Ctrl+I

![Workers concept illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_worker.png)

![Workforce collaboration illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_workforce.gif)

![Workspace interface illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_workspace.gif)

![Tasks and subtasks breakdown illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_tasks_subtasks.gif)

![Chat interface illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_chat.png)

![MCP protocol illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_mcp.png)

![AI models illustration](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/concepts_models.png)

---

## Source: https://docs.eigent.ai/core/workforce

Workforce

- Models

On this page

## [​](https://docs.eigent.ai/core/workforce\#concept-what-is-a-workforce)  Concept: What is a Workforce?

Workforce is CAMEL-AI’s multi-agent teamwork engine.Instead of relying on a single agent, Workforce lets you organize a _team_ of specialized agents—each with its own strengths—under a single, coordinated system. You can quickly assemble, configure, and launch collaborative agent “workforces” for any task that needs parallelization, diverse expertise, or complex workflows.With Workforce, agents plan, solve, and verify work together—like a project team in an organization, but fully automated.

## [​](https://docs.eigent.ai/core/workforce\#system-design)  System Design

### [​](https://docs.eigent.ai/core/workforce\#architecture-how-workforce-works)  **Architecture: How Workforce Works**

Workforce uses a **hierarchical, modular design** for real-world team problem-solving.![Workforce](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/workforce.jpg)See how the coordinator and task planner agents orchestrate a multi-agent workflow:

- **Workforce:** The “team” as a whole.
- **Worker nodes:** Individual contributors—each node can contain one or more agents, each with their own capabilities.
- **Coordinator agent:** The “project manager”—routes tasks to worker nodes based on their role and skills.
- **Task planner agent:** The “strategy lead”—breaks down big jobs into smaller, doable subtasks and organizes the workflow.

### [​](https://docs.eigent.ai/core/workforce\#communication-a-shared-task-channel)  **Communication: A Shared Task Channel**

Every Workforce gets a **shared task channel** when it’s created.
**How it works:**

- All tasks are posted into this channel.
- Worker nodes “listen” and accept their assigned tasks.
- Results are posted back to the channel, where they’re available as dependencies for the next steps.

_This design lets agents build on each other’s work and ensures no knowledge is lost between steps._

### [​](https://docs.eigent.ai/core/workforce\#failure-handling-built-in-robustness)  **Failure Handling: Built-In Robustness**

Workforce is designed to handle failures and recover gracefully.If a worker fails a task, the coordinator agent will:

- **Decompose and retry:** Break the task into even smaller pieces and reassign.
- **Escalate:** If the task keeps failing, create a new worker designed for that problem.
To prevent infinite loops, if a task has failed or been decomposed more than a set number of times (default: 3), Workforce will automatically halt that workflow.

## [​](https://docs.eigent.ai/core/workforce\#worker-nodes)  Worker Nodes

Eigent comes with a set of pre-configured agents, each designed for a specific domain of expertise. These agents are equipped with a curated set of toolkits to make them effective right out of the box.

### [​](https://docs.eigent.ai/core/workforce\#developeragent)  DeveloperAgent

_A skilled coding assistant that can write and execute code, run terminal commands, and verify solutions to complete tasks._**Equipped Toolkits:**

- HumanToolkit
- TerminalToolkit
- NoteTakingToolkit
- WebDeployToolkit

### [​](https://docs.eigent.ai/core/workforce\#browseragent)  BrowserAgent

_Can search the web, extract webpage content, simulate browser actions, and provide relevant information to solve the given task._**Equipped Toolkits:**

- SearchToolkit
- HybridBrowserToolkit
- HumanToolkit
- NoteTakingToolkit
- TerminalToolkit

### [​](https://docs.eigent.ai/core/workforce\#documentagent)  DocumentAgent

_A document processing assistant for creating, modifying, and managing various document formats, including presentations._**Equipped Toolkits:**

- FileToolkit
- PPTXToolkit
- HumanToolkit
- MarkItDownToolkit
- ExcelToolkit
- NoteTakingToolkit
- TerminalToolkit
- GoogleDriveMCPToolkit
- SearchToolkit

### [​](https://docs.eigent.ai/core/workforce\#multi-modalagent)  Multi-ModalAgent

_A multi-modal processing assistant for analyzing and generating media content like audio and images._**Equipped Toolkits:**

- VideoDownloaderToolkit
- AudioAnalysisToolkit
- ImageAnalysisToolkit
- OpenAIImageToolkit
- HumanToolkit
- TerminalToolkit
- NoteTakingToolkit
- SearchToolkit

## [​](https://docs.eigent.ai/core/workforce\#toolkit-reference)  Toolkit Reference

Toolkits are the collections of functions that give your agents their powers. Here is a reference for the toolkits used by the pre-configured agents._(in alphabetical order)_

### [​](https://docs.eigent.ai/core/workforce\#audioanalysistoolkit)  [AudioAnalysisToolkit](https://docs.camel-ai.org/reference/camel.toolkits.audio_analysis_toolkit)

_Provides tools for audio processing and analysis._This toolkit allows an agent to process audio files. It can take an audio file (from a local path or URL) and transcribe the speech into text. It can also answer specific questions about the content of an audio file, enabling agents to extract information from podcasts, meetings, or voice notes.

### [​](https://docs.eigent.ai/core/workforce\#exceltoolkit)  [ExcelToolkit](https://docs.camel-ai.org/reference/camel.toolkits.excel_toolkit)

_Enables agents to create, read, and manipulate Excel spreadsheets._This toolkit provides comprehensive functions for interacting with Excel files (`.xlsx/.xls/. csv`). Agents can create new workbooks, add or delete worksheets, read data from specific cells or ranges, write data to the spreadsheet, and convert data into Markdown formatted table.

### [​](https://docs.eigent.ai/core/workforce\#filetoolkit)  [FileToolkit](https://docs.camel-ai.org/reference/camel.toolkits.file_write_toolkit)

_A toolkit for creating, writing, and modifying text in files._This toolkit gives an agent the ability to create and write to files on the local file system (macOS, Linux, Windows). It provides support for writing to various file formats (Markdown, DOCX, PDF, and plaintext), replacing text in existing files, automatic filename uniquification to prevent overwrites, custom encoding and enhanced formatting options for specialized formats.

### [​](https://docs.eigent.ai/core/workforce\#googledrivemcptoolkit)  [GoogleDriveMCPToolkit](https://docs.camel-ai.org/reference/camel.toolkits.google_drive_mcp_toolkit)

_Connects to Google Drive to manage files and folders._This toolkit allows agents to interact with a user’s Google Drive. It can read files and folders from Google Drive. It acts as a bridge between the agent’s local environment and cloud storage.

### [​](https://docs.eigent.ai/core/workforce\#humantoolkit)  [HumanToolkit](https://docs.camel-ai.org/reference/camel.toolkits.human_toolkit)

_Allows an agent to pause its task and ask the user for help._This is a critical toolkit for handling situations that require human intervention. When an agent is stuck, needs credentials, or requires a subjective decision, it can use this toolkit to send a prompt to the user and wait for a response before continuing its task.

### [​](https://docs.eigent.ai/core/workforce\#hybridbrowsertoolkit)  [HybridBrowserToolkit](https://docs.camel-ai.org/reference/camel.toolkits.hybrid_browser_toolkit.ws_wrapper)

_Provides a powerful, stateful browser for web navigation and interaction._This toolkit gives an agent a fully-featured web browser that it can control programmatically. Unlike simple web scraping, this toolkit maintains a session, allowing the agent to click, type, hover, screenshot, and live _Take Control_ from the UI.

### [​](https://docs.eigent.ai/core/workforce\#imageanalysistoolkit)  [ImageAnalysisToolkit](https://docs.camel-ai.org/reference/camel.toolkits.image_analysis_toolkit)

_Provides tools for understanding the content of images._This toolkit enables an agent to “see” and interpret images. It can generate a detailed text description of an image or answer specific questions about what an image contains. This is crucial for tasks that involve visual data, such as describing products, analyzing charts, or identifying objects in a photo.

### [​](https://docs.eigent.ai/core/workforce\#markitdowntoolkit)  [MarkItDownToolkit](https://docs.camel-ai.org/reference/camel.toolkits.markitdown_toolkit)

_A specialized toolkit for converting content into clean Markdown._This toolkit is designed to scrape content from a list of local files and convert each into a structured Markdown format. The conversion is performed in parallel for efficiency. Supported file formats include: PDF, Office, EPUB, HTML, Images (ORC), Audio, Text, ZIP.

### [​](https://docs.eigent.ai/core/workforce\#notetakingtoolkit)  [NoteTakingToolkit](https://docs.camel-ai.org/reference/camel.toolkits.note_taking_toolkit)

_A toolkit for managing and interacting with Markdown note files._This toolkit provides tools for creating, reading, appending to, and listing notes. All notes are stored as **`.md`** files in a dedicated working directory and are tracked in a registry. An agent can use it to write down any important information. Other agents can then read these notes to get context and build upon previous work, facilitating effective collaboration.

### [​](https://docs.eigent.ai/core/workforce\#openaiimagetoolkit)  [OpenAIImageToolkit](https://docs.camel-ai.org/reference/camel.toolkits.openai_image_toolkit)

_Generates images from text prompts using OpenAI’s DALL-E models._This toolkit allows an agent to create new images based on a descriptive text prompt. It leverages models like DALL-E 3 to generate high-quality visuals, which can then be saved locally. This is essential for creative tasks, generating illustrations for documents, or any workflow requiring original image content.

### [​](https://docs.eigent.ai/core/workforce\#pptxtoolkit)  [PPTXToolkit](https://docs.camel-ai.org/reference/camel.toolkits.pptx_toolkit)

_Enables agents to create and write Microsoft PowerPoint presentations._This toolkit provides a suite of functions for building PowerPoint (`.pptx`) files. An agent can create a new presentation, add title and content slides, format text, create lists, and insert tables and images. It allows for the automated creation of professional-looking presentations.

### [​](https://docs.eigent.ai/core/workforce\#searchtoolkit)  [SearchToolkit](https://docs.camel-ai.org/reference/camel.toolkits.search_toolkit)

_Provides access to various web search engines._This toolkit is the primary tool for web research. It allows an agent to search information on engines like Google, Wikipedia, Bing, and Baidu. The agent can submit a query and receive a list of relevant URLs and snippets, which it can then use as a starting point for deeper investigation with the `HybridBrowserToolkit`.

### [​](https://docs.eigent.ai/core/workforce\#terminaltoolkit)  [TerminalToolkit](https://docs.camel-ai.org/reference/camel.toolkits.terminal_toolkit)

_A toolkit for terminal operations across multiple operating systems._This toolkit gives an agent access to a command-line interface. It supports terminal operations such as searching for files by name or content, executing shell commands, and managing terminal sessions.

### [​](https://docs.eigent.ai/core/workforce\#videodownloadertoolkit)  [VideoDownloaderToolkit](https://docs.camel-ai.org/reference/camel.toolkits.video_download_toolkit)

_Allows an agent to download and process videos from popular platforms._This toolkit enables an agent to download video content from URLs (e.g., from YouTube) and optionally split them into chunks. The saved video can then be analyzed by other toolkits, such as the `AudioAnalysisToolkit` for transcription, or `ImageAnalysisToolkit` for object detection.

### [​](https://docs.eigent.ai/core/workforce\#webdeploytoolkit)  [WebDeployToolkit](https://docs.camel-ai.org/reference/camel.toolkits.web_deploy_toolkit)

_Provides tools to deploy web content on a local server._This toolkit allows the `DeveloperAgent` to instantly host web applications or static files. It can serve a single HTML file or an entire folder (like a built React app) on a local port, making it easy to preview and test web development work.

[Concepts\\
\\
Previous](https://docs.eigent.ai/core/concepts) [Bring Your Own Key (BYOK)\\
\\
Next](https://docs.eigent.ai/core/models/byok)

Ctrl+I

![Workforce](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/workforce.jpg)

---

## Source: https://docs.eigent.ai/core/workers

Workers

- Models

On this page

Eigent is designed to be extensible. Beyond the pre-configured agents, you can significantly expand your workforce’s capabilities by connecting to external tools via custom MCP Servers and creating specialized workers to use them.This guide will walk you through how to integrate a new tool and build a custom worker step-by-step.

## [​](https://docs.eigent.ai/core/workers\#configuring-a-custom-mcp-server)  Configuring a Custom MCP Server

The Model Context Protocol (MCP) is the framework that allows Eigent to connect to external tools and services like GitHub, Notion, or any other API. By adding a custom MCP server, you are essentially teaching your workforce a new skill.

- Step 1: Click the **Settings** gear icon → Select the **MCP and Tools** tab.
- Step 2: Click the **\+ Add MCP Server** button to open the configuration dialog.
- Step 3: Provide the Server Configuration
  - **Paste the JSON configuration** for the server. This JSON file acts as a manifest, telling Eigent what the tool is, what functions it has, and how to call them. You can typically find this configuration file in the documentation of the third-party tool you wish to integrate.
  - **Add required credentials**. Many tools require authentication. For example, to connect to GitHub, you will need to generate a Personal Access Token from your GitHub account settings and paste it into the appropriate field.

![add mcp servers.gif](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/add_mcp_servers.gif)

## [​](https://docs.eigent.ai/core/workers\#creating-and-equipping-a-custom-worker)  Creating and Equipping a Custom Worker

Once you’ve configured a new MCP server, you need to create a worker that knows how to use it. A worker is your specialized agent, and you can equip it with any combination of tools.

- Step 1: On the **Canvas**, click the **\+ Add Worker** button located in the bottom toolbar.
- Step 2: Enter a clear Worker **Name** (e.g., “GitHub Specialist”) and provide an optional **Description** of its duties (e.g., “Manages pull requests and repository issues”).
- Step 3: Equip your Worker with the new tool (most important!)
  - Click on the **Agent Tool** dropdown menu.
  - Select the custom MCP server you just configured (e.g., Github MCP). You can also add any other tools you want this worker to have.
  - Click **Save**.

![add worker.gif](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/add_worker.gif)

## [​](https://docs.eigent.ai/core/workers\#what%E2%80%99s-next)  What’s next?

That’s it! You have successfully extended your AI workforce. You can now assign tasks that leverage your new integration.

[Tools\\
\\
Previous](https://docs.eigent.ai/core/tools) [Agent Skills\\
\\
Next](https://docs.eigent.ai/core/agent-skills)

Ctrl+I

![add mcp servers.gif](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/add_mcp_servers.gif)

![add worker.gif](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/add_worker.gif)

---

## Source: https://docs.eigent.ai/core/tools

Tools

- Models

**Add your MCP server****You can follow the steps below to set up your model**

1. Click Settings

![click_settings](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_settings.png)

2. Click Add MCP Server

![add_mcp](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/tools_add_mcp.png)

3. Configure Your MCP Server and install

![configure_mcp](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/tools_configure_mcp.png)4.Add external servers to your own Agent

- You can check the installed mcp server in the Added external servers column

![check_mcp](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/tools_check.png)

- After configuring your mcp server, you can add it to a Custom Agent.

[SambaNova\\
\\
Previous](https://docs.eigent.ai/core/models/sambanova) [Workers\\
\\
Next](https://docs.eigent.ai/core/workers)

Ctrl+I

![click_settings](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_settings.png)

![add_mcp](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/tools_add_mcp.png)

![configure_mcp](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/tools_configure_mcp.png)

![check_mcp](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/tools_check.png)

---

## Source: https://docs.eigent.ai/core/agent-skills

Agent Skills

- Models

On this page

Agent Skills, a concept originally introduced by Anthropic, are modular capabilities designed to expand Eigent’s core capabilities.Each Skill acts as a specialized package containing instructions, metadata, and optional tools (such as scripts or templates) that Eigent automatically triggers whenever relevant to a task.

## [​](https://docs.eigent.ai/core/agent-skills\#the-value-of-using-skills)  The Value of Using Skills

While traditional prompts act as one-off instructions for a single conversation, Skills are persistent, file-based assets that provide Eigent with deep, domain-specific expertise.By supplying tailored workflows, context, and best practices, Skills transform a general-purpose AI into a dedicated specialist.Because they load seamlessly on demand, you never have to waste time copy-pasting the same instructions across multiple chats.**Key benefits**:

- **Specialize Eigent**: Tailor capabilities for domain-specific tasks
- **Reduce repetition**: Create once, use automatically
- **Compose capabilities**: Combine Skills to build complex workflows

## [​](https://docs.eigent.ai/core/agent-skills\#using-skills-in-eigent)  Using Skills in Eigent

Eigent provides pre-built Agent Skills for common tasks, and you can create or upload your own custom Skills. Eigent automatically uses them when relevant to your request.

- **Example Skills:** These are pre-built Agent Skills available to all users on Eigent. They operate seamlessly behind the scenes, and Eigent utilizes them without requiring any manual setup. You have the option to manually enable or disable it.
- **Custom Skills:** These allow you to package your specific domain expertise and organizational knowledge. They are available across your Eigent workforce, and you can assign them to specific agents. You can create them directly within the Skill interface or add them via Eigent’s settings.![Screenshot 2026-02-24 at 21.58.11.png](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/agent_skills_settings_screenshot.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=b800f570e53d9a59e271cd7c05054450)

Upload your own Skills as zip files through Homepage > Agents > Skills. Custom Skills are individual to each user and saved locally.You can upload a standalone `SKILL.md` file or a complete `.zip` skill package. If uploading a package, it must contain a `SKILL.md` file in its root directory. In either case, the `SKILL.md` file must define the Skill’s name and description using YAML formatting.Every Skill requires a `SKILL.md` file with YAML frontmatter:

```
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Eigent to follow]

## Examples
[Concrete examples of using this Skill]
```

Eigent supports uploading multiple skills within one zip file, but please ensure the contents of each skill folder are complete.

## [​](https://docs.eigent.ai/core/agent-skills\#using-skills)  Using Skills

To test your Skill file immediately, click the **Try in chat** button.Use Skills only from trusted sources. Malicious Skills can misuse tools or execute unintended actions, potentially causing data leaks or unauthorized access—so carefully audit any untrusted Skill before use.

[Workers\\
\\
Previous](https://docs.eigent.ai/core/workers) [Support\\
\\
Next](https://docs.eigent.ai/troubleshooting/support)

Ctrl+I

![Screenshot 2026-02-24 at 21.58.11.png](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/agent_skills_settings_screenshot.png?w=840&fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=1824472c4fc76a9635df64bdc01a4d42)

---

## Source: https://docs.eigent.ai/core/models/byok

Bring Your Own Key (BYOK)

- Models

On this page

## [​](https://docs.eigent.ai/core/models/byok\#what-is-byok)  What is BYOK?

**Bring Your Own Key (BYOK)** allows you to use your own API keys from various AI model providers with Eigent. Instead of relying on a shared service, you connect directly to providers like OpenAI, Anthropic, or Google using your personal API credentials. This gives you:

- **Full control** over your API usage and billing
- **Direct access** to the latest models from each provider
- **Privacy** \- your requests go directly to the provider

## [​](https://docs.eigent.ai/core/models/byok\#openai-configuration-example)  OpenAI Configuration (Example)

### [​](https://docs.eigent.ai/core/models/byok\#step-1-get-your-api-key)  Step 1: Get Your API Key

1. Visit the [OpenAI API Keys page](https://platform.openai.com/api-keys)
2. Click **“Create new secret key”**
3. Copy the generated key (you won’t be able to see it again)

### [​](https://docs.eigent.ai/core/models/byok\#step-2-configure-in-eigent)  Step 2: Configure in Eigent

1. Launch Eigent and go to **Agent** \> **Models**
2. Find the **OpenAI** card in the Custom Model section

![byok_1](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/byok_1.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=3c62c294c4271b1e7064fbaca6deccfe)

1. Fill in the following fields:

| Field | Value | Example |
| --- | --- | --- |
| **API Key** | Your OpenAI secret key | `sk-proj-xxxx...` |
| **API Host** | OpenAI API endpoint | `https://api.openai.com/v1` |
| **Model Type** | The model you want to use | `gpt-4o`, `gpt-4o-mini` |

4. Click **Save** to validate and store your configuration
5. Click **Set as Default** to use this provider for your agents

## [​](https://docs.eigent.ai/core/models/byok\#configuration-fields)  Configuration Fields

| Field | Description | Required |
| --- | --- | --- |
| **API Key** | Your authentication key from the provider | Yes |
| **API Host** | The API endpoint URL | Yes (pre-filled for most providers) |
| **Model Type** | The specific model variant to use | Yes |
| **External Config** | Provider-specific settings (e.g., Azure deployment name) | Only for certain providers |

### [​](https://docs.eigent.ai/core/models/byok\#azure-specific-fields)  Azure-Specific Fields

| Field | Description | Example |
| --- | --- | --- |
| **API Version** | Azure OpenAI API version | `2024-02-15-preview` |
| **Deployment Name** | Your Azure deployment name | `my-gpt4-deployment` |

## [​](https://docs.eigent.ai/core/models/byok\#common-errors)  Common Errors

When saving your configuration, Eigent validates your API key and model. Here are the errors you may encounter:

| Error | Cause | Solution |
| --- | --- | --- |
| **Invalid key. Validation failed.** | API key is incorrect, expired, or malformed | Double-check your API key. Regenerate a new key if needed. |
| **Invalid model name. Validation failed.** | The specified model does not exist or is not available for your account | Verify the model name is correct. Check if you have access to that model. |
| **You exceeded your current quota** | API quota exhausted or billing issue | Check your provider’s billing dashboard. Add credits or upgrade your plan. |

## [​](https://docs.eigent.ai/core/models/byok\#supported-providers)  Supported Providers

Eigent supports the following BYOK providers:

| Provider | Default API Host | Official Documentation |
| --- | --- | --- |
| **OpenAI** | `https://api.openai.com/v1` | [OpenAI API Docs](https://platform.openai.com/docs/api-reference) |
| **Anthropic** | `https://api.anthropic.com/` | [Anthropic API Docs](https://docs.anthropic.com/en/api/getting-started) |
| **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai/` | [Gemini API Docs](https://ai.google.dev/gemini-api/docs) |
| **OpenRouter** | `https://openrouter.ai/api/v1` | [OpenRouter Docs](https://openrouter.ai/docs) |
| **Qwen (Alibaba)** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | [Qwen API Docs](https://help.aliyun.com/zh/dashscope/developer-reference/api-details) |
| **DeepSeek** | `https://api.deepseek.com` | [DeepSeek API Docs](https://platform.deepseek.com/api-docs) |
| **Minimax** | `https://api.minimax.io/v1` | [Minimax API Docs](https://platform.minimaxi.com/document/Announcement) |
| **Z.ai** | `https://api.z.ai/api/coding/paas/v4/` | [Z.ai Platform](https://z.ai/) |
| **Azure OpenAI** | _(user-provided)_ | [Azure OpenAI Docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) |
| **AWS Bedrock** | _(user-provided)_ | [AWS Bedrock Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) |
| **OpenAI Compatible** | _(user-provided)_ | For custom endpoints (e.g., xAI, local servers) |

## [​](https://docs.eigent.ai/core/models/byok\#tips)  Tips

- **Keep your API key secure** \- Never share or expose your API key publicly
- **Monitor usage** \- Check your provider’s dashboard regularly to track costs
- **Use appropriate models** \- Different models have different capabilities and pricing

[Workforce\\
\\
Previous](https://docs.eigent.ai/core/workforce) [Models (Local Model)\\
\\
Next](https://docs.eigent.ai/core/models/local-model)

Ctrl+I

![byok_1](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/byok_1.png?w=840&fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=fcf97f257fb8a33761c9ac91a5007215)

---

## Source: https://docs.eigent.ai/core/models/local-model

Models (Local Model)

- Models

On this page

## [​](https://docs.eigent.ai/core/models/local-model\#self-host-model)  **Self-Host Model**

1. Configure your self-host model

First, you need to set up your local models and expose them as an **OpenAI-Compatible Server.**

```
#Vllm https://docs.vllm.ai/en/latest/getting_started/quickstart.html#openai-compatible-server
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

```
#SGLang https://docs.sglang.ai/backend/openai_api_completions.html
from sglang.test.test_utils import is_in_ci

if is_in_ci():
    from patch import launch_server_cmd
else:
    from sglang.utils import launch_server_cmd

from sglang.utils import wait_for_server, print_highlight, terminate_process

server_process, port = launch_server_cmd(
    "python3 -m sglang.launch_server --model-path qwen/qwen2.5-0.5b-instruct --host 0.0.0.0 --mem-fraction-static 0.8"
)

wait_for_server(f"http://localhost:{port}")
print(f"Server started on http://localhost:{port}")
```

```
#Ollama https://github.com/ollama/ollama
ollama pull qwen2.5:7b
```

```
# LLaMA.cpp server https://github.com/ggml-org/llama.cpp/tree/master/tools/server
./llama-server -m /path/to/model.gguf --host 0.0.0.0 --port 8080
```

2. Setting your model

![set_local_model](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_local_model.png)

3. Configure the Google Search toolkit

![configure_searchtools](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_configure_tools.png)![configure_searchtoolsapi](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_configure_tools_key.png) You can refer to the following document for detailed information on how to configure **GOOGLE\_API\_KEY** and **SEARCH\_ENGINE\_ID :** [https://developers.google.com/custom-search/v1/overview](https://developers.google.com/custom-search/v1/overview)

## [​](https://docs.eigent.ai/core/models/local-model\#api-key-reference)  **API KEY Reference**

Gemini: [https://ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key)OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)Anthropic: [https://console.anthropic.com/](https://console.anthropic.com/)Qwen: [https://www.alibabacloud.com/help/en/model-studio/get-api-key](https://www.alibabacloud.com/help/en/model-studio/get-api-key)Deepseek: [https://platform.deepseek.com/api\_keys](https://platform.deepseek.com/api_keys)AWS Bedrock: [https://github.com/aws-samples/bedrock-access-gateway/blob/main/README.md](https://github.com/aws-samples/bedrock-access-gateway/blob/main/README.md)Azure: [https://azure.microsoft.com/products/cognitive-services/openai-service/](https://azure.microsoft.com/products/cognitive-services/openai-service/)

[Bring Your Own Key (BYOK)\\
\\
Previous](https://docs.eigent.ai/core/models/byok) [Gemini\\
\\
Next](https://docs.eigent.ai/core/models/gemini)

Ctrl+I

![set_local_model](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_local_model.png)

![configure_searchtools](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_configure_tools.png)

---

## Source: https://docs.eigent.ai/core/models/gemini

Gemini

- Models

On this page

### [​](https://docs.eigent.ai/core/models/gemini\#prerequisites)  Prerequisites

- **Get your API Key:** If you haven’t already, generate a key at
[Google AI Studio](https://aistudio.google.com/).
- **Copy the Key:** Keep your API key ready to paste.

### [​](https://docs.eigent.ai/core/models/gemini\#configuration-steps)  Configuration Steps

#### [​](https://docs.eigent.ai/core/models/gemini\#1-access-application-settings)  1\. Access Application Settings

- Launch Eigent and navigate to the **Home Page**.
- Click on the **Agent** tab, then click on the **Models** button.

![Gemini 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=04fe5892a7e54a3a03185afcf7daad78)

#### [​](https://docs.eigent.ai/core/models/gemini\#2-locate-model-configuration)  2\. Locate Model Configuration

- Scroll down to the **Custom Model** area.
- Look for the **Gemini Config** card.

#### [​](https://docs.eigent.ai/core/models/gemini\#3-enter-api-details)  3\. Enter API Details

Click on the Gemini Config card and fill in the following fields:

- **API Key:** Paste the key you generated from Google AI Studio.
- **API Host:** Enter the appropriate API endpoint host (for example,
`generativelanguage.googleapis.com`).
- **Model Type:**Enter the specific model version you wish to use.

  - _Example:_`gemini-3-pro-preview`
- **Save:** Click the **Save** button to apply your changes.

![Gemini 3 Pn](https://mintcdn.com/eigentai-0b34069f/iBuLSy_KBs4H4f7J/images/gemini.png?fit=max&auto=format&n=iBuLSy_KBs4H4f7J&q=85&s=93a479dadfff3f2995c33072bdc0d3be)

#### [​](https://docs.eigent.ai/core/models/gemini\#4-set-as-default-&-verify)  4\. Set as Default & Verify

- Once saved, the **“Set as Default”** button on the Gemini Config card will be
selected/active.
- **You are ready to go.** Your Eigent agents can now utilize the Gemini model.

* * *

> **Video Tutorial:** Prefer a visual guide? Watch the full configuration video
> here.

[Models (Local Model)\\
\\
Previous](https://docs.eigent.ai/core/models/local-model) [Ernie\\
\\
Next](https://docs.eigent.ai/core/models/ernie)

Ctrl+I

![Gemini 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?w=840&fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=beeddde306c2430fc545c727c9b267c1)

![Gemini 3 Pn](https://mintcdn.com/eigentai-0b34069f/iBuLSy_KBs4H4f7J/images/gemini.png?w=840&fit=max&auto=format&n=iBuLSy_KBs4H4f7J&q=85&s=8b16c9bc33c22968d8a2f80033e3100c)

---

## Source: https://docs.eigent.ai/core/models/sambanova

SambaNova

- Models

On this page

### [​](https://docs.eigent.ai/core/models/sambanova\#prerequisites)  Prerequisites

- **Get your API Key:** If you haven’t already, generate a key in the
[SambaNova developer platform](https://cloud.sambanova.ai/).
- **Copy the Key:** Keep your API key ready to paste.

### [​](https://docs.eigent.ai/core/models/sambanova\#configuration-steps)  Configuration Steps

#### [​](https://docs.eigent.ai/core/models/sambanova\#1-access-application-settings)  1\. Access Application Settings

- Launch Eigent and navigate to the **Home Page**.
- Click on the **Agent** tab，then click on the **Models** button.

![SambaNova 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=04fe5892a7e54a3a03185afcf7daad78)

#### [​](https://docs.eigent.ai/core/models/sambanova\#2-locate-model-configuration)  2\. Locate Model Configuration

- Scroll down to the **Custom Model** area.
- Look for the **SambaNova** card.

#### [​](https://docs.eigent.ai/core/models/sambanova\#3-enter-api-details)  3\. Enter API Details

Click on the SambaNova card and fill in the following fields:

- **API Key:** Paste the key you generated from the SambaNova platform.
- **API Host:**Enter the API endpoint host.

  - _Default:_`https://api.sambanova.ai/v1`
- **Model Type:**Enter the specific model version you wish to use.

  - _Example:_`DeepSeek-V3.1`
- **Save:** Click the **Save** button to apply your changes.

![SambaNova 2 Pn](https://mintcdn.com/eigentai-0b34069f/iBuLSy_KBs4H4f7J/images/sambanova.png?fit=max&auto=format&n=iBuLSy_KBs4H4f7J&q=85&s=02b2f5fb1a4bf72a330449aa995ecb2a)

#### [​](https://docs.eigent.ai/core/models/sambanova\#4-set-as-default-&-verify)  4\. Set as Default & Verify

- Once saved, the **“Set as Default”** button on the SambaNova card will be
selected/active.
- **You are ready to go.** Your Eigent agents can now utilize the SambaNova
model.

* * *

[Kimi\\
\\
Previous](https://docs.eigent.ai/core/models/kimi) [Tools\\
\\
Next](https://docs.eigent.ai/core/tools)

Ctrl+I

![SambaNova 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?w=840&fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=beeddde306c2430fc545c727c9b267c1)

![SambaNova 2 Pn](https://mintcdn.com/eigentai-0b34069f/iBuLSy_KBs4H4f7J/images/sambanova.png?w=840&fit=max&auto=format&n=iBuLSy_KBs4H4f7J&q=85&s=4751e0500896650741846f1a70935ee3)

---

## Source: https://docs.eigent.ai/core/models/ernie

Ernie

- Models

On this page

### [​](https://docs.eigent.ai/core/models/ernie\#prerequisites)  Prerequisites

- **Get your API Key:** If you haven’t already, generate a key in the
[Baidu AI Cloud Qianfan console](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application).
- **Copy the Key:** Keep your API key ready to paste.

### [​](https://docs.eigent.ai/core/models/ernie\#configuration-steps)  Configuration Steps

#### [​](https://docs.eigent.ai/core/models/ernie\#1-access-application-settings)  1\. Access Application Settings

- Launch Eigent and navigate to the **Home Page**.
- Click on the **Agent** tab, then click on the **Models** button.

![Ernie 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=04fe5892a7e54a3a03185afcf7daad78)

#### [​](https://docs.eigent.ai/core/models/ernie\#2-locate-model-configuration)  2\. Locate Model Configuration

- Scroll down to the **Custom Model** area.
- Look for the **Ernie** card.

#### [​](https://docs.eigent.ai/core/models/ernie\#3-enter-api-details)  3\. Enter API Details

Click on the Ernie card and fill in the following fields:

- **API Key:** Paste the key you generated from Baidu AI Cloud Qianfan.
- **API Host:**Enter the API endpoint host.

  - _Example:_`https://qianfan.baidubce.com/v2`
- **Model Type:**Enter the specific model version you wish to use.

  - _Example:_`ernie-5.0`
- **Save:** Click the **Save** button to apply your changes.

![Ernie 2 Pn](https://mintcdn.com/eigentai-0b34069f/SEfvVYEPyfpIim6s/images/ernie.png?fit=max&auto=format&n=SEfvVYEPyfpIim6s&q=85&s=84c865a80acb40c62448a2eef93141c6)

#### [​](https://docs.eigent.ai/core/models/ernie\#4-set-as-default-&-verify)  4\. Set as Default & Verify

- Once saved, the **“Set as Default”** button on the Ernie card will be
selected/active.
- **You are ready to go.** Your Eigent agents can now utilize the Ernie model.

* * *

[Gemini\\
\\
Previous](https://docs.eigent.ai/core/models/gemini) [MiniMax\\
\\
Next](https://docs.eigent.ai/core/models/minimax)

Ctrl+I

![Ernie 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?w=840&fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=beeddde306c2430fc545c727c9b267c1)

![Ernie 2 Pn](https://mintcdn.com/eigentai-0b34069f/SEfvVYEPyfpIim6s/images/ernie.png?w=840&fit=max&auto=format&n=SEfvVYEPyfpIim6s&q=85&s=d7521afc1a346f31306241f3c7ec9956)

---

## Source: https://docs.eigent.ai/core/models/kimi

Kimi

- Models

On this page

### [​](https://docs.eigent.ai/core/models/kimi\#prerequisites)  Prerequisites

- **Get your API Key:** If you haven’t already, generate a key in the Kimi
( [Moonshot AI](https://platform.moonshot.ai/)) developer console.
- **Copy the Key:** Keep your API key ready to paste.

### [​](https://docs.eigent.ai/core/models/kimi\#configuration-steps)  Configuration Steps

#### [​](https://docs.eigent.ai/core/models/kimi\#1-access-application-settings)  1\. Access Application Settings

- Launch Eigent and navigate to the **Home Page**.
- Click on the **Agent** tab, then click on the **Models** button.

![Kimi 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=04fe5892a7e54a3a03185afcf7daad78)

#### [​](https://docs.eigent.ai/core/models/kimi\#2-locate-model-configuration)  2\. Locate Model Configuration

- Scroll down to the **Custom Model** area.
- Look for the **Moonshot** card.

#### [​](https://docs.eigent.ai/core/models/kimi\#3-enter-api-details)  3\. Enter API Details

Click on the Moonshot card and fill in the following fields:

- **API Key:** Paste the key you generated from the Kimi console.
- **API Host:** Enter the appropriate API endpoint host (for example,
`https://api.moonshot.ai/v1`).
- **Model Type:**Enter the specific model version you wish to use.

  - _Example:_`kimi-k2.5`
- **Save:** Click the **Save** button to apply your changes.

![Kimi 3 Pn](https://mintcdn.com/eigentai-0b34069f/iBuLSy_KBs4H4f7J/images/kimi.png?fit=max&auto=format&n=iBuLSy_KBs4H4f7J&q=85&s=9aace4e2548a902f4c79013a689b8e6b)

#### [​](https://docs.eigent.ai/core/models/kimi\#4-set-as-default-&-verify)  4\. Set as Default & Verify

- Once saved, the **“Set as Default”** button on the Moonshot card will be
selected/active.
- **You are ready to go.** Your Eigent agents can now utilize the Kimi model.

* * *

[MiniMax\\
\\
Previous](https://docs.eigent.ai/core/models/minimax) [SambaNova\\
\\
Next](https://docs.eigent.ai/core/models/sambanova)

Ctrl+I

![Kimi 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?w=840&fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=beeddde306c2430fc545c727c9b267c1)

![Kimi 3 Pn](https://mintcdn.com/eigentai-0b34069f/iBuLSy_KBs4H4f7J/images/kimi.png?w=840&fit=max&auto=format&n=iBuLSy_KBs4H4f7J&q=85&s=cb1673dd516dc734292c4c70ef6c1444)

---

## Source: https://docs.eigent.ai/core/models/minimax

MiniMax

- Models

On this page

### [​](https://docs.eigent.ai/core/models/minimax\#prerequisites)  Prerequisites

- **Get your API Key:** If you haven’t already, generate a key at
[Minimax Platform](https://www.minimax.io/).
- **Copy the Key:** Keep your API key ready to paste.

### [​](https://docs.eigent.ai/core/models/minimax\#configuration-steps)  Configuration Steps

#### [​](https://docs.eigent.ai/core/models/minimax\#1-access-application-settings)  1\. Access Application Settings

- Launch Eigent and navigate to the **Home Page**.
- Click on the **Settings** tab (usually located in the sidebar or top
navigation).

![Minimax 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=04fe5892a7e54a3a03185afcf7daad78)

#### [​](https://docs.eigent.ai/core/models/minimax\#2-locate-model-configuration)  2\. Locate Model Configuration

- In the Settings menu, find and select the **Models** section.
- Scroll down to the **Custom Model** area.
- Look for the **Minimax Config** card.

![Minimax 2 Pn](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/minimax_1.png)

#### [​](https://docs.eigent.ai/core/models/minimax\#3-enter-api-details)  3\. Enter API Details

Click on the Minimax Config card and fill in the following fields:

- **API Key:** Paste the key you generated from Minimax Platform.
- **API Host:** Enter the appropriate API endpoint host.
- **Model Type:**Enter the specific model version you wish to use.

  - _Example:_`MiniMax-M2.1`
- **Save:** Click the **Save** button to apply your changes.

![Minimax 3 Pn](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/minimax_2.png)

#### [​](https://docs.eigent.ai/core/models/minimax\#4-set-as-default-&-verify)  4\. Set as Default & Verify

- Once saved, the **“Set as Default”** button on the Minimax Config card will be
selected/active.
- **You are ready to go.** Your Eigent agents can now utilize the Minimax model.

![Minimax 4 Pn](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/minimax_3.png)

* * *

[Ernie\\
\\
Previous](https://docs.eigent.ai/core/models/ernie) [Kimi\\
\\
Next](https://docs.eigent.ai/core/models/kimi)

Ctrl+I

![Minimax 1 Pn](https://mintcdn.com/eigentai-0b34069f/_GpxIx_W_ZtChA6B/images/model_setting.png?w=840&fit=max&auto=format&n=_GpxIx_W_ZtChA6B&q=85&s=beeddde306c2430fc545c727c9b267c1)

![Minimax 2 Pn](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/minimax_1.png)

![Minimax 3 Pn](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/minimax_2.png)

![Minimax 4 Pn](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/minimax_3.png)

---

## Source: https://docs.eigent.ai/troubleshooting/support

Support

- Models

On this page

For account and billing questions, email our support team at [info@eigent.ai](mailto:info@eigent.ai).Eigent offers flexible plans for every type of user, from individuals to large enterprises. Our services are divided into two main categories: Cloud and Self-Hosted.

### [​](https://docs.eigent.ai/troubleshooting/support\#cloud-service)  Cloud Service

Our Cloud Service is a subscription-based offering that gives you access to Eigent’s powerful AI models and infrastructure without any setup.

- **Free:** Perfect for getting started. Includes **500 Credits** per month.
- **Plus:** For more frequent users. Includes **2,000 Credits** per month.
- **Pro:** For power users who need advanced capabilities. Includes **10,000 Credits** per month.
- **Add-On Packs:** If you run out of Credits, you can purchase an Add-On Pack at any time to top up your account.

> _Credits never expire within the billing cycle and you can top‑up at any time.__Unused Credits from your monthly plan allowance do not roll over to the next month._ _Credits from Add-On Packages will carry over to subsequent billing cycles.__See your Credits Usage directly in Settings → Account → [Manage](https://www.eigent.ai/dashboard)._

### [​](https://docs.eigent.ai/troubleshooting/support\#self-hosted-service)  Self-Hosted Service

For users who require more control, privacy, and customization, we offer self-hosted solutions. To view more open-source information, please visit [GitHub](https://github.com/eigent-ai/eigent).

- **Free:** Designed for individual users, open-source developers, small teams, or non-commercial projects. This plan requires you to host your own models and provide your own API keys.
- **Scalable:** Ideal for teams requiring enhanced reliability and support. This plan also allows for logo and brand customization.
- **Custom:** A bespoke solution for enterprise clients with specific needs for features, support, security and control.

For inquiries about our Scalable and Custom plans, please please refer to our [**License**](https://github.com/eigent-ai/eigent) or email us at **[info@eigent.ai](mailto:info@eigent.ai)**.

## [​](https://docs.eigent.ai/troubleshooting/support\#credits-&-billing)  Credits & Billing

### [​](https://docs.eigent.ai/troubleshooting/support\#how-credits-work)  How Credits work?

- 1 USD = 100 Credits for top‑ups.
- Credits are the currency you use to power your tasks in Eigent’s Cloud Service. Every action that uses our cloud service consumes Credits.

### [​](https://docs.eigent.ai/troubleshooting/support\#free-credits-and-trials)  Free Credits and Trials

- New sign‑ups get **1000** bonus Credits.
- To reward active users, we grant **200** Credits every day you use the app. Unused amounts don’t roll over to the next day.
- All paid subscription plans (Plus and Pro) come with a **7-day free trial**. You can cancel anytime within this period at no charge.

### [​](https://docs.eigent.ai/troubleshooting/support\#upgrading-or-topping%E2%80%91up)  **Upgrading or Topping‑up**

- Click **User** icon in the Eigent webpage.
- Click **Account Settings** to open your personal account page.
- Click **Upgrade** to move to a higher tier with more monthly Credits.
- Click **\+ Add Credits** to purchase an Add-On Pack when you’ve used up your monthly allowance.

![Support Dashboard](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/support_dashboard.png)

### [​](https://docs.eigent.ai/troubleshooting/support\#invitation-code)  Invitation Code

Just below your plan card you’ll see your exclusive invitation code. Share it with a friend! Both of you automatically receive **500 Credits** once they register.

### [​](https://docs.eigent.ai/troubleshooting/support\#credits-usage)  Credits Usage

Scroll to credits usage dashboard to view:

- **Total Credits**: Your current available balance.
- **Daily Refreshed Credits:** Your 200‑Credit daily bonus countdown. These daily credits are used first before your main balance is touched.
- **Credits History:** This is a log of all transactions on your account. You can see how Credits were added (e.g., `monthly`, `invite`, `register`) and how they were spent (`consume`).

**Note on Balance**Your balance is calculated based on the total credits added minus the total consumed within your current billing cycle.If your balance becomes negative, it will be displayed as **0**. This means your service may be restricted until new Credits are added to your account.

### [​](https://docs.eigent.ai/troubleshooting/support\#billing-cycle-and-cancellations)  Billing Cycle and Cancellations

- For free users, your monthly cycle starts on the date you registered. For subscribers, it starts on the date of your first successful subscription.
- Daily active credits are used first (no rollover), followed by monthly pack credits (no rollover to next month), and finally, top-up pack credits (which don’t expire).
- You can cancel any subscription or Add-On Pack purchase within 7 days for a full refund.
  - Plan resets to Free and billing cycle resets to registration date.
  - Credits balance re‑computed according to Free‑tier rules.
- How do I cancel my subscription? Please contact **[info@eigent.ai](mailto:info@eigent.ai).**
- You can download invoices from the payment confirmation email sent to your registered email address.

For any questions about your bill or account status, email us anytime at [info@eigent.ai](mailto:info@eigent.ai).

[Agent Skills\\
\\
Previous](https://docs.eigent.ai/core/agent-skills) [Bug\\
\\
Next](https://docs.eigent.ai/troubleshooting/bug)

Ctrl+I

![Support Dashboard](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/support_dashboard.png)

---

## Source: https://docs.eigent.ai/troubleshooting/bug

Bug

- Models

On this page

![Bug Report](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/bug_report.gif)

### [​](https://docs.eigent.ai/troubleshooting/bug\#step-1-access-the-bug-report-feature)  Step 1: Access the Bug Report Feature

1. Locate the **Bug Report** button in the top section of the desktop interface, positioned to the right of your project name
2. Click the **Bug Report** button to initiate the reporting process

### [​](https://docs.eigent.ai/troubleshooting/bug\#step-2-download-log-files)  Step 2: Download Log Files

- Upon clicking the Bug Report button, log files will be automatically downloaded to your device
- These log files contain technical information that helps our development team diagnose issues more effectively

### [​](https://docs.eigent.ai/troubleshooting/bug\#step-3-complete-the-bug-report-form)  Step 3: Complete the Bug Report Form

- A bug report web form will automatically open in your default browser
- Please provide the following information:
  - **Bug Description**: Write a clear description of the issue you encountered
  - **Screenshot Upload**: Attach relevant screenshots that demonstrate the problem
  - **Log File Upload**: Upload the log files that were downloaded in Step 2

### [​](https://docs.eigent.ai/troubleshooting/bug\#step-4-join-our-community-for-real-time-support)  Step 4: Join Our Community for Real-time Support

### [​](https://docs.eigent.ai/troubleshooting/bug\#for-english-speaking-users)  For English-speaking Users:

- Join our **CAMEL-AI Discord** **🤖｜eigent** channel : [https://discord.com/invite/CNcNpquyDc](https://discord.com/invite/CNcNpquyDc) for bug discussions and community support
- Get direct assistance from our team and community members

### [​](https://docs.eigent.ai/troubleshooting/bug\#for-chinese-speaking-users)  For Chinese-speaking Users:

- Add our WeChat assistant: **CamelAIOrg** to join the **bug fix group** for Chinese community support
- Communicate with our Chinese-speaking support team

### [​](https://docs.eigent.ai/troubleshooting/bug\#alternative-github-issues)  Alternative: GitHub Issues

Developers and technical users are welcome to report issues directly through our GitHub issues:

- **Repository URL**: [https://github.com/eigent-ai/eigent](https://github.com/eigent-ai/eigent)
- Submit detailed issues with reproduction steps

## [​](https://docs.eigent.ai/troubleshooting/bug\#important-notes)  Important Notes

- Always include log files when reporting bugs for faster resolution
- Provide as much detail as possible in your bug description
- Screenshots help our team understand visual issues more quickly
- Our community channels provide the fastest response times for urgent issues

Thank you for helping us improve our product through your feedback and bug reports!

[Support\\
\\
Previous](https://docs.eigent.ai/troubleshooting/support)

Ctrl+I

![Bug Report](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/bug_report.gif)

---

