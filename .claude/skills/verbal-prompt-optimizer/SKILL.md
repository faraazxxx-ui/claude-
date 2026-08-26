---
name: verbal-prompt-optimizer
description: >
  Convert verbose, verbal-thinker prompts into perfected, platform-optimized prompts for 10 AI agents.
  Use when the user provides a rambling verbal prompt, business context, or previous AI conversations
  and needs them transformed into precise, platform-specific prompts. Also use when user says
  "optimize my prompt", "fix this for Claude/Grok/Gemini", or provides voice-to-text transcripts
  that need structuring for AI consumption.
---

# Verbal Prompt Optimizer

Transform verbose verbal inputs, business contexts, and previous AI conversations into perfected, platform-optimized prompts for 10 AI agents. Designed for verbal thinkers who communicate in streams of consciousness.

## Workflow

### Step 1: Extract the Nodal Network

Read all attached files, transcripts, and previous conversations. Build a nodal network:

| Node Type | Extract |
|-----------|---------|
| Entities | People, companies, products, locations |
| Requirements | Explicit needs stated by the user |
| Inferred needs | Unstated but logically necessary requirements |
| Constraints | Budget, time, values, physical limitations |
| Dependencies | What must happen before what |
| Delta gaps | Difference between what was asked and what was delivered |

Save as `nodal_network.md` for reference.

### Step 2: Run the Prompt Optimizer

```bash
python3 /home/ubuntu/skills/prompt-optimizer/scripts/optimize.py \
  --input "DISTILLED_REQUEST" \
  --platforms SELECTED_KEYS \
  --json
```

Use the output as the optimization blueprint. For deeper platform knowledge, consult:
- `prompt-optimizer/references/platforms-anthropic.md`
- `prompt-optimizer/references/platforms-other.md`
- `prompt-optimizer/references/examples.md`

### Step 3: Enrich with Context

The optimizer produces templates. Inject the nodal network context into each template:

1. Replace placeholders with actual business data
2. Add platform-specific context sections with the extracted entities
3. Include verification criteria derived from the requirements
4. Add failure policies and safety guardrails appropriate to the task

### Step 4: Red Team Each Prompt

Test every prompt against its platform's anti-patterns:

| Platform | Check For |
|----------|-----------|
| Manus | Vague outcomes? Missing file names? Telling it HOW to think? |
| Claude Chat | Data mixed with instructions? Negative framing? |
| Claude Co-work | Micromanaged steps? Missing quality criteria? |
| Claude Code | No verification? Verbose instead of concise? |
| Grok Heavy | No failure policy? No output schema? |
| Perplexity Pro | Multi-part question? Few-shot examples? URL requests? |
| Perplexity Computer | Under-scoped? Micromanaged? |
| Comet Agent | No roadblock handling? Missing @tab? |
| Claude Chrome | Missing safety section? |
| Gemini Browser | Instructions before data? Mixed XML + Markdown? |

### Step 5: Deliver

Output each prompt in a code block, ready to paste. Include a "Why This Works" annotation explaining which platform-specific patterns were applied.

## Key Principle

Verbal thinkers communicate intent through volume and repetition. The optimizer's job is to:
1. Extract the signal from the noise
2. Identify what was said vs. what was meant vs. what was missed
3. Structure it in each platform's native format
4. Verify it against each platform's failure modes
