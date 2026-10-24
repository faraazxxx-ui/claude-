# The Complete AI Platform Skills & Capabilities Master Reference

**Purpose:** Maximize your utilization of every AI subscription by knowing exactly what each platform can do, when to use it, and how to prompt it optimally.

**Research Methodology:** 6 parallel research lanes across GitHub (5,671 features cataloged from 90k+ star repos), Reddit community forums (35 power-user techniques), YouTube expert tutorials (18 video analyses), official documentation (62 API capabilities), verified skill repositories (81 skills), and cross-platform prompt optimization research. Integrated with your personal `faraazxxx-ui/claude-` repository context.

**Date:** July 2025 | **Author:** Manus AI

---

## FINAL ANSWER: The Decision Matrix

When you sit down with a task, use this matrix to instantly decide which platform to open:

| Task Type | Primary Platform | Secondary Platform | Why |
| :--- | :--- | :--- | :--- |
| **Deep research with citations** | Perplexity Pro | Gemini Deep Research | RAG-native architecture; citation-backed answers |
| **Complex code refactoring** | Claude (Code/Sonnet) | Cursor/Windsurf | 1M context window; strict instruction following |
| **Quick inline code completion** | GitHub Copilot | Cursor Tab | Deep IDE integration; context-aware suggestions |
| **Real-time news/social analysis** | Grok (DeepSearch) | Perplexity Pro | Live X/Twitter firehose; unfiltered reasoning |
| **Image/video generation** | Grok Imagine | ChatGPT (DALL-E) | Aurora engine; front-loaded prompt architecture |
| **Document analysis (PDFs, reports)** | Claude (Projects) | Gemini (NotebookLM) | Upload entire document sets; maintain context |
| **Spreadsheet/data tasks** | Gemini (Sheets) | ChatGPT (Code Interpreter) | Native Workspace integration |
| **Email drafting & management** | Gemini (Gmail) | Copilot (Outlook) | Summarize threads; contextual reply suggestions |
| **Building custom AI agents** | ChatGPT (Custom GPTs) | Copilot Studio | GPT Store distribution; plugin ecosystem |
| **End-to-end task automation** | Manus AI | Replit Agent | Sandbox execution; browser + shell + files |
| **Brainstorming & ideation** | ChatGPT (Canvas) | Claude (Projects) | Collaborative workspace; iterative refinement |
| **Fact-checking a draft** | Perplexity Pro | Grok DeepSearch | Source verification; contradiction detection |
| **Multi-file app development** | Cursor (Agent Mode) | Windsurf (Cascade) | Codebase-aware; auto-context filling |
| **Scheduled/recurring tasks** | Manus AI (Schedule) | Make.com + Copilot | Context retention; no-code triggers |
| **Voice-to-execution (verbal thinker)** | AudioPen/Superwhisper → Manus | Wispr Flow → Claude Code | Capture fuzzy thought → structure → execute |

---

## SECTION 0: Your Personalized "Verbal Thinker" AI OS Routing Card

Based on your existing stack from `faraazxxx-ui/claude-`, here is your optimized routing flow with all platforms integrated:

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPTURE (Voice-First)                                          │
│  Wispr Flow / AudioPen / Superwhisper / Talknotes               │
│  → Unstructured verbal thought → Structured text                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  ROUTE (Multi-Model Orchestration)                              │
│  TypingMind / Raycast AI → Select best model for task           │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Grok     │  │Perplexity│  │ Gemini   │  │ Claude   │      │
│  │DeepSearch│  │Pro Search│  │Deep Rsrch│  │ Sonnet   │      │
│  │(framing) │  │(sources) │  │(Workspace│  │(analysis)│      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  EXECUTE (Autonomous Agents)                                    │
│  Manus AI (full automation) / Claude Code (dev) / Genspark Claw │
│  → Terminal commands, file ops, browser automation, deployment   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  REMEMBER (Knowledge Management)                                │
│  Granola (meetings) / Notion (second brain) / Obsidian (graph)  │
│  → Persistent memory across sessions                            │
└─────────────────────────────────────────────────────────────────┘
```

### Your Missing Links (from Stack Audit)

| Gap | Recommended Tool | What It Solves |
| :--- | :--- | :--- |
| Ambient voice capture without context-switching | **Superwhisper** | Custom AI formatting modes; structures text before pasting. |
| Rambling → structured text | **AudioPen** | Translates fuzzy verbal thoughts into clear, coherent text. |
| System-wide AI access | **Elephas** | "Super Command" across OS; no app switching needed. |
| Multi-model comparison from one prompt | **TypingMind** | Dictate once, compare Claude/Gemini/Grok side-by-side. |
| Voice → mind maps/task lists | **Talknotes** | Brainstorm aloud → see logical structure instantly. |

---

## SECTION 1: Platform Capabilities — Complete Feature Lists

### 1.1 Claude (Anthropic)

#### Core API Features

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **1M Token Context** | Process entire codebases, long documents, or maintain extended conversations. | Feed entire repos via `repomix` for holistic refactoring. |
| **Extended Thinking** | Transparent step-by-step reasoning for complex tasks. | Use for math proofs, legal analysis, multi-step logic. |
| **Batch Processing** | Async processing at 50% cost reduction. | Queue overnight analysis jobs for cost savings. |
| **Prompt Caching** | 5-min and 1-hour cache durations reduce latency. | Cache system prompts and large context blocks. |
| **Citations** | Ground responses in source documents with exact sentence references. | Essential for RAG applications and research. |
| **Structured Outputs** | Guaranteed JSON schema conformance. | Use for API integrations requiring strict formats. |
| **Token Counting** | Pre-calculate token usage before sending. | Budget management for large-scale deployments. |
| **Context Editing** | Auto-manage conversation context with configurable strategies. | Prevent context overflow in long sessions. |
| **Effort Parameter** | Control thoroughness vs. token efficiency tradeoff. | Set low for quick tasks, high for deep analysis. |

#### Tool Use & Automation

| Tool | What It Does | When to Use |
| :--- | :--- | :--- |
| **Computer Use (Beta)** | Screenshot capture, mouse/keyboard control, desktop automation. | UI testing, form filling, visual verification. |
| **Bash Tool** | Execute shell commands and scripts. | System administration, file operations. |
| **Code Execution** | Run Python in sandboxed environment. | Data analysis, chart generation, calculations. |
| **Memory Tool** | Store/retrieve information across conversations. | Persistent preferences, project context. |
| **Text Editor Tool** | Create and edit files with built-in editor. | Code writing, document creation. |
| **Web Search Tool** | Augment with current web data. | Real-time information, recent events. |
| **Web Fetch Tool** | Retrieve full content from URLs/PDFs. | Document ingestion, source verification. |
| **Tool Search** | Dynamically discover tools via regex. | Large tool ecosystems, MCP servers. |
| **MCP Connector** | Connect to remote MCP servers directly from API. | External integrations without separate client. |

#### Claude Code CLI — Hidden Features (from Reddit r/ClaudeAI)

| Feature | Command/Method | What It Does |
| :--- | :--- | :--- |
| **Mobile Code Tab** | iOS/Android app | Write code and approve PRs from phone. |
| **Teleport** | `--teleport` | Pull a cloud session to local terminal. |
| **Remote Control** | `/remote-control` | Reverse teleport (local → cloud). |
| **Loop/Schedule** | `/loop`, `/schedule` | Run workflows on timer for up to a week. |
| **Hooks** | Lifecycle events | Inject custom logic before/after tool calls. |
| **Cowork Dispatch** | From anywhere | Delegate non-coding tasks (email, Slack). |
| **Chrome Extension** | Built-in browser | Claude visually inspects frontend builds. |
| **Branch/Fork** | `/branch`, `--fork-session` | Explore different paths without losing context. |
| **Git Worktrees** | `-w` flag | Dozens of parallel sessions in same repo. |
| **Batch Agents** | `/batch` | Fan out to hundreds of worktree agents. |
| **Side Questions** | `/btw` | Quick questions without derailing main task. |
| **Bare Mode** | `--bare` | Skip auto-loading configs for fast init. |
| **Add Directory** | `--add-dir` | Grant access to additional folders mid-session. |
| **Custom Agents** | `.claude/agents/` | Define custom agent personas. |
| **Voice Input** | `/voice` | Spoken input in CLI. |
| **Close Pattern** | `/close` skill | End-of-session: scan decisions, update memory, commit, log. |

#### Skills vs. Hooks (Critical Distinction)

**Skills** are for procedural knowledge — "how to do X right." They teach the agent workflows and best practices.

**Hooks** are for preventive rules — "never do Y." They fire deterministically before every tool call, making them ideal for strict enforcement (e.g., preventing duplicate emails, enforcing code style).

**Best Practice:** Make `AGENTS.md` the single source of truth. Have `CLAUDE.md` simply import it with `@AGENTS.md` to keep setup clean and portable.

#### Verified Skill Repositories

| Repository | Stars | Key Skills |
| :--- | :--- | :--- |
| **anthropics/skills** | Official | API integrations, code generation, system operations. |
| **obra/superpowers** | Community | Brainstorming, parallel agents, TDD, systematic debugging, git worktrees. |
| **vercel-labs/agent-skills** | Vercel | Deploy-to-Vercel, React best practices, web design guidelines. |
| **K-Dense-AI/claude-scientific-skills** | Scientific | Protein experiment design, time series ML, single-cell analysis. |
| **ComposioHQ/awesome-claude-skills** | 67k+ | Hundreds of automation skills via Rube MCP (Composio). |
| **compound-engineering-plugin** | New | Works across Claude Code, Codex, Cursor, and more. |

---

### 1.2 Gemini Ultra / Advanced (Google)

#### Core Features

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **Deep Research** | Multi-step research pulling from credible sources with cross-referencing. | Use for literature reviews; outputs structured layouts. |
| **Audio Overview** | Transforms documents into podcast-style audio between two AI hosts. | Listen to research summaries during commute. |
| **Canvas** | Real-time collaborative workspace for documents and code. | Generate and preview HTML/React prototypes live. |
| **Gems** | Custom AI personas with saved instructions and uploaded context files. | Build a "Gem maker" Gem to generate optimized instructions for other Gems. |
| **NotebookLM** | Anchor conversations in uploaded documents for grounded responses. | Upload entire textbooks; generate study guides. |
| **Video/Image Creation** | Veo 3 for video from text; Imagen for image generation/editing. | Combine with Deep Research for illustrated reports. |
| **Guided Learning** | Step-by-step educational mode adapting to the user. | Use for learning new technical concepts. |
| **Gemini CLI Extensions** | Command-line extensions for developers. | Access skills, databases, MCP, and context from terminal. |

#### Workspace Integration

| App | Gemini Capabilities |
| :--- | :--- |
| **Google Docs** | Content generation, refinement, summarization; pulls from Drive/Gmail. |
| **Google Sheets** | Create tables, write formulas, analyze data patterns. |
| **Google Slides** | Generate text, suggest layouts, provide images, create speaker notes. |
| **Gmail** | Summarize long threads, tailored reply suggestions, inbox search. |
| **Google Drive** | File search, organization, cross-document analysis. |

#### Community Power-User Techniques

The **"Dual-Brain" coding workflow** involves feeding Gemini Pro in AI Studio an entire repository's context using `repomix`, generating a comprehensive implementation plan, then executing that plan using a faster CLI tool like Claude Code or Cursor.

For controlling verbosity, place instructions near the **end** of the prompt and use the phrase `economy of expression -- with the highest information density possible` for concise yet detailed output.

To create advanced Gems, use a **"Deep Research" workflow**: prompt Gemini to research prompt engineering philosophies, generate comprehensive PDFs of findings, then feed those PDFs back to a "Gem maker" Gem as foundational instructions.

---

### 1.3 Copilot Enterprise Premium (Microsoft)

#### Core Capabilities

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **Agent Mode** | Real-time collaborator in VS Code consuming premium requests. | Use for complex multi-file changes. |
| **Coding Agent** | Directs work from issue to merge (uses Actions minutes). | Assign GitHub issues directly to Copilot. |
| **Custom Agents** | Built from scratch with knowledge, tools, prompts in Copilot Studio. | Create specialized agents for HR, Sales, Support. |
| **Declarative Agents** | Define runtime behaviors, personality, rules for M365 Copilot. | Equip with SharePoint knowledge and REST APIs. |
| **Parent-Child Orchestration** | Parent agent delegates to specialized child agents. | Build complex workflows with modular expertise. |
| **MCP Registry** | Integration with Model Context Protocol for external tools. | Connect internal databases and APIs. |
| **Graph API Access** | Secure grounding in Microsoft 365's knowledge index. | Respect existing permissions and sensitivity labels. |
| **Agent Evaluation** | Tools for testing agent accuracy and instruction quality. | Iterate on agent instructions with measurable feedback. |

#### M365 Copilot APIs

| Capability | What It Enables |
| :--- | :--- |
| **Information Retrieval** | Pull relevant info from M365 content with permission controls. |
| **Hybrid Search** | Semantic + lexical search across OneDrive. |
| **Meeting Extraction** | AI-generated meeting notes, action items, discussion topics. |
| **Compliance Solutions** | Capture and archive user interactions. |
| **Conversational Experiences** | Embed M365 Copilot in custom applications. |

---

### 1.4 Grok (xAI)

#### Core Capabilities

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **DeepSearch** | Multi-step research agent searching web + X + news. | Prefix prompts with "Use DeepSearch" for activation. |
| **Think Mode (Grok 3)** | Reinforcement-learning-based reasoning with backtracking. | Use for math, logic puzzles, complex analysis. |
| **256K Context Window** | Process large documents and codebases. | Feed entire project documentation. |
| **Grok Heavy ($300/mo)** | Maximum performance tier for complex reasoning. | Reserve for mission-critical deep analysis. |
| **Companions** | Customizable AI personas within Grok ecosystem. | Create specialized assistants for different workflows. |
| **Agentic Coding** | Refactor, debug, build tools with IDE integrations. | Connect to VS Code for code assistance. |
| **Real-time X Data** | Live access to Twitter/X posts and trends. | Unmatched for social sentiment and breaking news. |

#### Imagine API (Aurora Engine)

| Capability | Details | Power-User Tip |
| :--- | :--- | :--- |
| **Image Generation** | Text-to-image; configurable aspect ratio; up to 10 per request. | Front-load subject in first 20 words. |
| **Image Editing** | Natural language; up to 3 reference images for compositing. | Combine subjects and transfer styles. |
| **Image-to-Video** | Animate a still image with a text prompt. | Create looping video ads from static images. |
| **Video Generation** | Text-to-video up to 15 seconds. | Use spatial audio cues for soundscape design. |
| **Video Editing** | Modify existing videos with natural language. | Add overlays, change pacing, adjust mood. |

#### Grok Build Community Resources

The `awesome-grok-build` starter kit provides reusable `.grok/skills`, `AGENTS.md` templates, `.grokignore` defaults, and stack templates for Next.js, FastAPI, and Python.

---

### 1.5 ChatGPT / GPT-5 (OpenAI)

#### Core Capabilities

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **GPT-5 Core** | Multimodal with up to 256K memory context. | Use for long-running projects requiring memory. |
| **Custom GPTs** | Tailored versions with instructions, knowledge, capabilities. | Build and distribute via GPT Store. |
| **GPT Actions** | RESTful API calls via natural language using Function Calling. | Connect to any external API without code. |
| **Canvas** | Collaborative workspace for writing and coding. | Target specific sections for inline editing. |
| **Memory** | Remembers details and preferences across all chats. | Build up a persistent profile over time. |
| **Operator** | Browser automation agent (forms, shopping, tasks). | Automate repetitive web workflows. |
| **Deep Research** | Comprehensive multi-step information gathering. | Use for market analysis, competitive intelligence. |
| **Advanced Voice** | Natural conversational voice interaction. | Hands-free brainstorming and dictation. |
| **Assistants API** | Build AI assistants in custom applications. | Integrate into products with reasoning/planning. |
| **Code Interpreter** | Execute Python, analyze data, create visualizations. | Upload CSVs for instant analysis. |

#### Codex Skills for Mobile Development (from Reddit)

| Phase | Skill | Purpose |
| :--- | :--- | :--- |
| Scaffolding | `vibecode-cli` | Project setup, Expo config, directory structure. |
| UI/Design | `Frontend design` | Layout, spacing, component hierarchy, colors. |
| Backend | `supabase-mcp` | Auth, tables, row-level security, edge functions. |
| Store Metadata | `aso optimisation` | Title, subtitle, keywords, discoverability. |
| Submission | `app store preflight checklist` | Validation before TestFlight. |
| Publishing | `app store connect cli` | Version management, TestFlight, metadata uploads. |

#### The "Thinking Layer" Approach

Advanced users treat ChatGPT not as a search engine but as an **analytical filter**. Instead of "Write me an email response," use "Read this email. Identify any manipulative language, logical fallacies, or hidden assumptions. Then draft a response that addresses each one." This transforms the AI from a generator into a reasoning partner.

---

### 1.6 Perplexity Pro

#### Core Capabilities

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **Pro Search** | Multi-step research with clarifying questions and product comparisons. | Ask it to output comparison tables, not summaries. |
| **Spaces/Projects** | Collaborative environments for organized research. | Create per-project spaces for team research. |
| **Collections** | Save and categorize threads and sources. | Build a personal research library. |
| **Computer Mode** | Agentic interaction with computer interfaces. | Complex multi-step tasks beyond search. |
| **Multi-Model Switching** | One-click switch between 5 major AI models. | Use Deepseek R1 for complex reasoning within Perplexity. |
| **Sonar API** | Web-grounded responses with streaming and structured outputs. | Build citation-backed applications. |
| **Search API** | Real-time ranked results with domain/language/region filtering. | Programmatic research at scale (up to 5 queries per request). |

#### Community Power-User Workflows

The **"AI Sandwich"** is the most effective community-validated workflow:
1. **Perplexity** gathers sources and context with citation requirements.
2. **Claude** ingests the research and drafts a narrative or analysis.
3. **Perplexity** fact-checks the draft, finds contradictions, and fills gaps.

The **Confidence Forcing** technique: Add "Label each claim High/Medium/Low confidence and say what would change your mind" to force self-evaluation.

---

### 1.7 Manus AI

#### Core Capabilities

| Feature | Description | Power-User Tip |
| :--- | :--- | :--- |
| **Agent Skills** | Modular capabilities with progressive disclosure (3-stage loading). | Create custom skills with SKILL.md files. |
| **MCP Connectors** | Prebuilt: Gmail, Notion, Stripe, HubSpot, Slack, Google Calendar. | Build custom MCP servers for internal systems. |
| **Scheduled Tasks 2.0** | Periodic tasks with context retention across runs. | Automate monitoring, data extraction, reporting. |
| **Browser Operator** | Automate clicking, form filling, cross-platform data entry. | Replace manual repetitive web workflows. |
| **Sandbox Environment** | Secure cloud VM with Python, Node.js, shell access. | Execute complex multi-step workflows safely. |
| **Projects** | Organize work with shared instructions and files. | Maintain persistent context across tasks. |
| **API (v2)** | Programmatic task creation, structured output, webhooks. | Build integrations that trigger Manus autonomously. |
| **Web App Automation** | Add scheduled actions to Manus-built web apps. | Refresh data, run scripts, send reminders. |
| **Parallel Processing** | Fan out subtasks across multiple agents. | Wide research, bulk data processing. |
| **Google Workspace** | Full Drive access via `gws` CLI. | Read/write files, manage documents. |

#### Real-World Power Use Cases (from Community)
- Analyze 12 months of invoices to identify junk billing, then generate a script to call customer retention.
- Build full-stack monetized apps with Stripe integration in a single session.
- Conduct OSINT-driven geopolitical risk assessments with multi-source verification.
- Automate daily workflow optimization across Notion, Obsidian, and Google Calendar.

---

### 1.8 Other Notable Platforms

| Platform | Key Strength | Unique Feature |
| :--- | :--- | :--- |
| **Cursor** | AI-first code editor | Agent Mode (Composer): multi-file generation, auto-context, `@web` search, experimental bug finder. |
| **Windsurf** | AI IDE with Cascade | Real-time preview: AI writes to disk before approval; live dev server preview. Skills vs. Workflows distinction. |
| **Replit Agent** | Full-stack from description | Builds complete apps, sets up databases, deploys—all from natural language. |
| **Devin** | Autonomous AI engineer | Works independently for hours; opens PRs, runs tests, QAs with computer vision. Integrates with Windsurf. |
| **v0.dev** | UI component generation | Generates full React/Next.js components from text prompts (Vercel). |
| **OpenHands (OpenDevin)** | Open-source AI engineer | Free alternative to Devin for autonomous development. |
| **Framer AI** | AI website builder | Advanced design capabilities with AI-powered layout generation. |
| **Create.xyz** | AI app creation | Natural language to full application. |

---

## SECTION 2: Prompt Optimization Cheat Sheet

### The Format DNA Quick Reference

| Platform | Optimal Structure | Key Pattern |
| :--- | :--- | :--- |
| **Claude** | `<context>` → `<instructions>` → `<output_format>` | Wrap each content type in XML tags; nest hierarchically. |
| **Grok** | Subject → Style → Environment → Lighting → Mood → Technical | Front-load critical info in first 20-30 words. |
| **Gemini** | Draft → Critique → Refine (iterative) | Demand JSON with `confidence`, `checks`, `citations` fields. |
| **Perplexity** | Goal → Question → Context → Scope → Non-goals → Evidence Rules → Output | Write like a research spec, not a question. |
| **Copilot** | Goal → Context → Expectations → Source | Write like user stories with acceptance criteria. |
| **ChatGPT** | Role → Task → Format → Constraints | Conversational but structured; leverage memory. |
| **Manus** | Goal → Requirements → Deliverable → Verification | Specify file names and verification criteria. |

### Critical Anti-Patterns (Never Do This)

| Platform | Anti-Pattern | Do This Instead |
| :--- | :--- | :--- |
| **Claude** | Tell it what NOT to do; mix data with instructions. | Use positive framing; separate with XML tags. |
| **Grok** | Bury key actions at end; omit Sound: block for video. | Front-load subject; always include explicit audio cues. |
| **Gemini** | Ask for "thoughts"; accept first draft. | Demand concrete artifacts; iterate with changed constraints. |
| **Perplexity** | SEO keyword soup; multi-part questions. | Single focused question; specify timeframe and source types. |
| **Copilot** | Accept suggestions without reading; ignore architecture. | Review every line; maintain `.github/copilot-instructions.md`. |
| **ChatGPT** | One-shot queries without context. | Build up memory; use system prompts in Custom GPTs. |
| **Manus** | Vague outcomes without file names; tell it HOW to think. | Specify deliverables explicitly; let it choose methods. |

### Hidden Prompting Techniques

| Technique | Platform | How to Use |
| :--- | :--- | :--- |
| **Model Self-Knowledge** | Claude | Tell Claude its identity/version in system prompt for correct API strings. |
| **Spatial Audio Cues** | Grok | Use "muffled through glass" or "sea spray on mic" to design soundscapes. |
| **Terminology Locks** | Gemini | Pin terms: `CRITICAL TERMS: Use "X" exactly. Do not substitute synonyms.` |
| **Confidence Forcing** | Perplexity | "Label each claim High/Medium/Low confidence and say what would change your mind." |
| **Context Files** | Copilot | `.github/copilot-instructions.md` feeds architecture patterns into context. |
| **Economy of Expression** | Gemini | Use phrase "economy of expression -- with the highest information density possible." |
| **Adversarial Reviewer** | Gemini | Assign role: "You are an Adversarial Reviewer. Find concrete failure modes." |

---

## SECTION 3: Cross-Platform Workflow Patterns

### Pattern 1: The Research-to-Synthesis Pipeline
```
Perplexity Pro (gather sources, extract quotes)
    → Claude Projects (ingest research, synthesize report with XML prompts)
        → Manus AI (format, publish, deliver to Notion/Drive)
```

### Pattern 2: The Code Generation & Review Loop
```
Copilot/Cursor (generate initial code drafts)
    → Gemini Advanced (adversarial review: failure modes, edge cases)
        → Claude Sonnet (refactor based on critique, optimize)
```

### Pattern 3: The Multimodal Asset Creation Workflow
```
ChatGPT Canvas (brainstorm concepts, write detailed prompts)
    → Grok Imagine (generate visual assets with front-loaded prompts)
        → Manus AI (automate downloading, renaming, organization)
```

### Pattern 4: The "AI Sandwich" (Fact-Checking Loop)
```
Perplexity Pro (gather primary sources)
    → Claude/ChatGPT (draft narrative or analysis)
        → Perplexity Pro (fact-check draft, find contradictions, fill gaps)
```

### Pattern 5: The Multi-Model Vibe Coding Setup
```
Claude Opus (fast model in Windsurf for rapid implementation)
    → GPT-5.1 Codex (slow model in ChatGPT CLI for deep debugging)
        → Cursor Agent Mode (multi-file orchestration and deployment)
```

### Pattern 6: The Verbal Thinker Pipeline (Your Stack)
```
AudioPen/Superwhisper (capture fuzzy verbal thought)
    → TypingMind (route to best model, compare outputs)
        → Manus AI (execute structured output end-to-end)
            → Notion/Obsidian (persist in second brain)
```

---

## SECTION 4: GitHub Ecosystem & MCP Servers

### Top GitHub Repositories for AI Skills

| Repository | Stars | Platform | What It Contains |
| :--- | :--- | :--- | :--- |
| **awesome-mcp-servers** | 90,000+ | Multi-platform | Comprehensive MCP server directory. |
| **awesome-claude-skills** (Composio) | 67,000+ | Claude | Hundreds of automation integrations. |
| **awesome-chatgpt** | 45,000+ | ChatGPT | Prompts, tools, plugins, extensions. |
| **awesome-copilot** | 18,000+ | Copilot | Extensions, tips, integrations. |
| **litellm** | 46,000+ | Multi-platform | Unified API for all LLM providers. |
| **gpt-engineer** | 55,000+ | OpenAI | Specify and build entire projects. |
| **awesome-claude-prompts** | 5,100+ | Claude | Curated prompt library. |
| **awesome-gemini** | 955+ | Gemini | Protocol clients, servers, tools. |
| **compound-engineering-plugin** | New | Multi-platform | Works with Claude Code, Codex, Cursor. |
| **ccpocket** | 719 | Claude | Mobile client for Codex/Claude via WebSocket. |

### Essential MCP Servers to Install

| MCP Server | What It Connects | Use Case |
| :--- | :--- | :--- |
| **Notion MCP** | Notion databases & pages | Auto-save AI outputs to knowledge base. |
| **Gmail MCP** | Email management | Read, draft, send emails via AI. |
| **Google Calendar MCP** | Calendar events | Schedule, query, manage events. |
| **Firecrawl MCP** | Web scraping | Deep content extraction from any URL. |
| **Stripe MCP** | Payment processing | Manage charges, customers, subscriptions. |
| **Slack MCP** | Team communication | Send messages, read channels. |
| **GitHub MCP** | Repository management | Issues, PRs, code search. |
| **MongoDB Lens** | Database operations | Full-featured MongoDB management. |
| **Snowflake/BigQuery (Alkemi)** | Data warehouses | Natural language querying. |
| **Xcode MCP** | iOS development | Project management, builds, file ops. |
| **Google Tasks MCP** | Task management | Interface with Google Tasks API. |
| **ChatGPT Responses MCP** | Cross-model | Let Claude talk to ChatGPT with web search. |

---

## SECTION 5: Daily Workflow Integration Template

### Morning Routine (15 min)
1. **Perplexity Pro:** Quick scan of overnight news relevant to your projects.
2. **Gemini (Gmail):** Summarize email threads; draft priority responses.
3. **Manus AI (Schedule):** Review automated overnight task results.

### Deep Work Blocks
1. **Claude (Projects):** Load project context; execute complex analysis or writing.
2. **Cursor/Copilot:** Code with AI assistance; use Agent Mode for multi-file changes.
3. **Gemini (Canvas):** Iterate on documents with real-time collaboration.

### Research Sessions
1. **Perplexity Pro:** Gather sources with citation requirements.
2. **Claude:** Synthesize findings into structured reports.
3. **NotebookLM:** Generate audio summaries for review.

### End of Day
1. **Manus AI:** Automate file organization, data backups, report generation.
2. **Claude Code `/close` skill:** Scan for decisions, update memory files, commit, generate session log.

---

## SECTION 6: Automation & Scheduling Capabilities

| Platform | Automation Method | What You Can Automate |
| :--- | :--- | :--- |
| **Manus AI** | Scheduled Tasks 2.0 (cron-like) | Any task with context retention; monitoring, reporting, data extraction. |
| **Copilot Studio** | Event triggers + agents | M365 workflows, Teams notifications, document processing. |
| **ChatGPT** | Custom GPTs + Actions | API integrations triggered by conversation. |
| **Claude Code** | `/loop`, `/schedule` | Development workflows running up to a week. |
| **Make.com** | Visual workflow builder | Cross-platform automation with 1000+ integrations. |
| **Zapier + MCP** | Claude MCP integration | Trigger Zaps from Claude conversations. |

---

## Supporting Details: Research Sources & Methodology

| Research Lane | Method | Sources Accessed | Features Found |
| :--- | :--- | :--- | :--- |
| Lane 1: GitHub Repos | `gh` CLI + web scraping | awesome-mcp-servers (90k), awesome-claude-skills (67k), awesome-copilot (18k), awesome-gemini (955) | 5,671 |
| Lane 2: Verified Skill Repos | internet-skill-finder script | anthropics/skills, obra/superpowers, vercel-labs/agent-skills, K-Dense-AI, ComposioHQ | 81 |
| Lane 3: Reddit Communities | Firecrawl + search | r/ClaudeAI, r/Bard, r/ChatGPT, r/perplexity_ai, r/grok, r/windsurf | 35 |
| Lane 4: YouTube Tutorials | manus-analyze-video | 40 videos across all platforms | 18 |
| Lane 5: Official Documentation | Web extraction | Anthropic, Google, Microsoft, xAI, OpenAI, Perplexity docs | 62 |
| Lane 6: Prompt Optimization | Cross-platform research | Platform docs, community guides, prompt engineering articles | 25 |
| **TOTAL** | | | **5,892** |

### Key References

| # | Source | Type | URL/Location |
| :--- | :--- | :--- | :--- |
| 1 | Reddit r/perplexity_ai | Community | "My 'AI sandwich' workflow" |
| 2 | Anthropic Platform Docs | Official | https://platform.claude.com/docs/ |
| 3 | Reddit r/ClaudeAI | Community | "15 New Claude Code Hidden Features" |
| 4 | Anthropic Prompting Guide | Official | Claude Prompting Best Practices |
| 5 | Google Blog | Official | "New Gemini features: Canvas and Audio Overview" |
| 6 | Reddit r/Bard | Community | "My Guide/Workflow for Gems" |
| 7 | Reddit r/Bard | Community | "Gemini Studio is a beast for code planning" |
| 8 | Rephrase-it | Article | "Gemini AI Prompting: 5 Patterns That Hold Up" |
| 9 | Microsoft Learn | Official | "Extend M365 Copilot with agents" |
| 10 | YouTube | Tutorial | "Multi-agent Orchestration in Copilot Studio" |
| 11 | TechDebt.now | Article | "Copilot Anti-Patterns & Best Practices" |
| 12 | xAI News | Official | "Grok 3 Beta — The Age of Reasoning Agents" |
| 13 | GitHub | Community | "Grok Imagine 1.5 Prompt Guide" |
| 14 | Reddit r/grok | Community | "Practical Grok Build setup patterns" |
| 15 | OpenAI | Official | "Introducing Operator" |
| 16 | Reddit r/ChatGPT | Community | "Becoming a power user" |
| 17 | YouTube | Tutorial | "Perplexity Pro tips: Deepseek R1 Reasoning" |
| 18 | Rephrase-it | Article | "Perplexity AI: Search Prompts That Actually Pull" |
| 19 | Manus AI Docs | Official | "Scheduled Tasks 2.0" |
| 20 | Manus AI Docs | Official | "Build custom AI workflows with Agent Skills" |
| 21 | faraazxxx-ui/claude- | Personal | Verbal Thinker Stack Audit |

---

*This document is a living reference. AI platforms update features frequently. Last verified: July 2025.*
