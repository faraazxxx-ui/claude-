[Skip to main content](https://docs.eigent.ai/get_started/quick_start#content-area)

[Eigent Documentation home page![light logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-light.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=6e834644e7f72b581b80517ded8bfd50)![dark logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-dark.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=c4746a53b606e7323688e61df33aff03)](https://www.eigent.ai/)

Search...

Ctrl K

Search...

Navigation

Get Started

Quick Start

[Documentation](https://docs.eigent.ai/get_started/welcome)

- [Download Here](https://www.eigent.ai/)

##### Get Started

- [Welcome](https://docs.eigent.ai/get_started/welcome)
- [Installation](https://docs.eigent.ai/get_started/installation)
- [Quick Start](https://docs.eigent.ai/get_started/quick_start)

##### Core

- [Concepts](https://docs.eigent.ai/core/concepts)
- [Workforce](https://docs.eigent.ai/core/workforce)
- Models

  - [Bring Your Own Key (BYOK)](https://docs.eigent.ai/core/models/byok)
  - [Models (Local Model)](https://docs.eigent.ai/core/models/local-model)
  - [Gemini](https://docs.eigent.ai/core/models/gemini)
  - [Ernie](https://docs.eigent.ai/core/models/ernie)
  - [MiniMax](https://docs.eigent.ai/core/models/minimax)
  - [Kimi](https://docs.eigent.ai/core/models/kimi)
  - [SambaNova](https://docs.eigent.ai/core/models/sambanova)
- [Tools](https://docs.eigent.ai/core/tools)
- [Workers](https://docs.eigent.ai/core/workers)
- [Agent Skills](https://docs.eigent.ai/core/agent-skills)

##### Troubleshooting

- [Support](https://docs.eigent.ai/troubleshooting/support)
- [Bug](https://docs.eigent.ai/troubleshooting/bug)

On this page

- [Create Your First Task](https://docs.eigent.ai/get_started/quick_start#create-your-first-task)
- [The Top Bar](https://docs.eigent.ai/get_started/quick_start#the-top-bar)
- [The Main View](https://docs.eigent.ai/get_started/quick_start#the-main-view)
- [Agent Folder](https://docs.eigent.ai/get_started/quick_start#agent-folder)
- [📌 Note on File Storage](https://docs.eigent.ai/get_started/quick_start#-note-on-file-storage)
- [Pre-built Agents](https://docs.eigent.ai/get_started/quick_start#pre-built-agents)
- [Add your own workers](https://docs.eigent.ai/get_started/quick_start#add-your-own-workers)
- [Start Your First Task](https://docs.eigent.ai/get_started/quick_start#start-your-first-task)
- [Step 1: Define Your Goal](https://docs.eigent.ai/get_started/quick_start#step-1-define-your-goal)
- [Step 2: Review Subtask Flow](https://docs.eigent.ai/get_started/quick_start#step-2-review-subtask-flow)
- [Step 3: Lauch the Task](https://docs.eigent.ai/get_started/quick_start#step-3-lauch-the-task)
- [Watch Agents Work](https://docs.eigent.ai/get_started/quick_start#watch-agents-work)
- [Human in the Loop](https://docs.eigent.ai/get_started/quick_start#human-in-the-loop)
- [A Quick Tour of Settings](https://docs.eigent.ai/get_started/quick_start#a-quick-tour-of-settings)
- [General](https://docs.eigent.ai/get_started/quick_start#general)
- [Models](https://docs.eigent.ai/get_started/quick_start#models)
- [MCP Servers](https://docs.eigent.ai/get_started/quick_start#mcp-servers)
- [Next Steps](https://docs.eigent.ai/get_started/quick_start#next-steps)

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