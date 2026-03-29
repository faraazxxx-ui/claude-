[Skip to main content](https://docs.eigent.ai/core/workers#content-area)

[Eigent Documentation home page![light logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-light.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=6e834644e7f72b581b80517ded8bfd50)![dark logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-dark.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=c4746a53b606e7323688e61df33aff03)](https://www.eigent.ai/)

Search...

Ctrl K

Search...

Navigation

Core

Workers

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

- [Configuring a Custom MCP Server](https://docs.eigent.ai/core/workers#configuring-a-custom-mcp-server)
- [Creating and Equipping a Custom Worker](https://docs.eigent.ai/core/workers#creating-and-equipping-a-custom-worker)
- [What’s next?](https://docs.eigent.ai/core/workers#what%E2%80%99s-next)

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