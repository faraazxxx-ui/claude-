[Skip to main content](https://docs.eigent.ai/core/workforce#content-area)

[Eigent Documentation home page![light logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-light.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=6e834644e7f72b581b80517ded8bfd50)![dark logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-dark.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=c4746a53b606e7323688e61df33aff03)](https://www.eigent.ai/)

Search...

Ctrl K

Search...

Navigation

Core

Workforce

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

- [Concept: What is a Workforce?](https://docs.eigent.ai/core/workforce#concept-what-is-a-workforce)
- [System Design](https://docs.eigent.ai/core/workforce#system-design)
- [Architecture: How Workforce Works](https://docs.eigent.ai/core/workforce#architecture-how-workforce-works)
- [Communication: A Shared Task Channel](https://docs.eigent.ai/core/workforce#communication-a-shared-task-channel)
- [Failure Handling: Built-In Robustness](https://docs.eigent.ai/core/workforce#failure-handling-built-in-robustness)
- [Worker Nodes](https://docs.eigent.ai/core/workforce#worker-nodes)
- [DeveloperAgent](https://docs.eigent.ai/core/workforce#developeragent)
- [BrowserAgent](https://docs.eigent.ai/core/workforce#browseragent)
- [DocumentAgent](https://docs.eigent.ai/core/workforce#documentagent)
- [Multi-ModalAgent](https://docs.eigent.ai/core/workforce#multi-modalagent)
- [Toolkit Reference](https://docs.eigent.ai/core/workforce#toolkit-reference)
- [AudioAnalysisToolkit](https://docs.eigent.ai/core/workforce#audioanalysistoolkit)
- [ExcelToolkit](https://docs.eigent.ai/core/workforce#exceltoolkit)
- [FileToolkit](https://docs.eigent.ai/core/workforce#filetoolkit)
- [GoogleDriveMCPToolkit](https://docs.eigent.ai/core/workforce#googledrivemcptoolkit)
- [HumanToolkit](https://docs.eigent.ai/core/workforce#humantoolkit)
- [HybridBrowserToolkit](https://docs.eigent.ai/core/workforce#hybridbrowsertoolkit)
- [ImageAnalysisToolkit](https://docs.eigent.ai/core/workforce#imageanalysistoolkit)
- [MarkItDownToolkit](https://docs.eigent.ai/core/workforce#markitdowntoolkit)
- [NoteTakingToolkit](https://docs.eigent.ai/core/workforce#notetakingtoolkit)
- [OpenAIImageToolkit](https://docs.eigent.ai/core/workforce#openaiimagetoolkit)
- [PPTXToolkit](https://docs.eigent.ai/core/workforce#pptxtoolkit)
- [SearchToolkit](https://docs.eigent.ai/core/workforce#searchtoolkit)
- [TerminalToolkit](https://docs.eigent.ai/core/workforce#terminaltoolkit)
- [VideoDownloaderToolkit](https://docs.eigent.ai/core/workforce#videodownloadertoolkit)
- [WebDeployToolkit](https://docs.eigent.ai/core/workforce#webdeploytoolkit)

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