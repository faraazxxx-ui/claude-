[Skip to main content](https://docs.eigent.ai/core/agent-skills#content-area)

[Eigent Documentation home page![light logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-light.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=6e834644e7f72b581b80517ded8bfd50)![dark logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-dark.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=c4746a53b606e7323688e61df33aff03)](https://www.eigent.ai/)

Search...

Ctrl K

Search...

Navigation

Core

Agent Skills

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

- [The Value of Using Skills](https://docs.eigent.ai/core/agent-skills#the-value-of-using-skills)
- [Using Skills in Eigent](https://docs.eigent.ai/core/agent-skills#using-skills-in-eigent)
- [Using Skills](https://docs.eigent.ai/core/agent-skills#using-skills)

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