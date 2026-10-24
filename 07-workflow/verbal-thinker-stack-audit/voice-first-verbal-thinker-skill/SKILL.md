---
name: voice-first-verbal-thinker
description: Route and process voice-captured input for verbal thinkers. Use when the user provides unstructured spoken thoughts, voice memos, audio files, or rambling text and needs it structured into actionable outputs (tasks, briefs, prompts, project plans). Also use when the user says "I was thinking about...", "here's a voice note", or provides fuzzy/unstructured input that needs clarification before execution.
---

# Voice-First Verbal Thinker

Transform unstructured verbal input into structured, executable output. Designed for users who think out loud and need a cognitive translation layer between fuzzy ideas and autonomous execution.

## Core Principle

**Speak first. Structure second. Execute last.** Never ask a verbal thinker to type a detailed prompt. Instead, accept messy input and progressively refine it.

## Workflow

### 1. Detect Input Type

| Input | Action |
|-------|--------|
| Audio file (.mp3, .wav, .m4a, .webm) | Transcribe with `manus-speech-to-text` |
| Rambling text / voice memo transcript | Proceed to Step 2 |
| Fuzzy one-liner ("something about Q2...") | Ask one clarifying question, then proceed |

### 2. Extract Intent

Parse the raw input into three components:

- **Core idea**: The single sentence that captures what the user actually wants
- **Implied tasks**: Actions the user expects but did not explicitly state
- **Missing context**: Information needed before execution (data sources, deadlines, audience)

Present these back to the user for confirmation. Use this template:

```
I heard: [core idea]
I think you also want: [implied tasks]
I still need: [missing context — ask only what blocks execution]
```

### 3. Structure the Output

Convert confirmed intent into one of these formats based on context:

| Context | Output Format |
|---------|---------------|
| Project or multi-step work | Task list with dependencies |
| Research or analysis request | Structured brief (audience, scope, deliverable) |
| Delegation to Manus/agent | Optimized execution prompt |
| Meeting follow-up | Action items + decisions + open questions |
| Creative/brainstorm | Mind map outline (hierarchical bullets) |

### 4. Route to Execution

Use the user's preferred routing card:

| Need | Route to |
|------|----------|
| Sharp framing / prediction | Grok |
| Sourced research | Perplexity |
| Deep synthesis | Gemini Deep Research |
| Docs / slides / output | Genspark |
| Autonomous local execution | Manus (My Computer) |
| Code changes | Claude Code |
| Meeting memory | Granola |

### 5. Archive

Save the structured output to a persistent location (file, Notion, Google Drive) so the verbal thinker never loses a processed thought.

## Voice-to-Execution Quick Patterns

**Pattern A: Voice memo to project folder**
Audio → transcribe → extract tasks → create folder structure → delegate file creation to Manus

**Pattern B: Fuzzy idea to research brief**
One-liner → clarify scope → generate brief → route to Perplexity/Gemini → compile findings

**Pattern C: Rambling to polished prompt**
Raw text → extract core intent → rewrite as structured prompt → route to target model

## Anti-Patterns

- Do NOT ask verbal thinkers to "be more specific" — infer intent and confirm
- Do NOT present more than one clarifying question at a time
- Do NOT skip the confirmation step — verbal thinkers often discover what they mean while reviewing the structure
- Do NOT output raw transcriptions as final deliverables — always structure
