
# SKILL 3: PROMPT-OPTIMIZER (Comet, Claude Chrome, Gemini) + RED TEAM

This document contains the optimized prompts for three platforms and a detailed red team analysis of the original user prompt.

---

## Platform 1: Comet Agent

**Task:** Research and compare Shopify themes and apps for a natural skincare e-commerce store.

**Optimized Prompt:**

```
Okay, Comet. Let's find the perfect Shopify setup for Ghusoon, a natural, faith-based skincare brand.

First, I need you to research Shopify themes. Please open a new tab and go to the Shopify Theme Store.

In that tab, which we'll call @themes, I want you to search for themes that would fit a "sensory luxury" aesthetic with a dark, gold, olive, and cream color palette. Look for themes that emphasize high-quality product photography and storytelling. Please find the top 3 themes that meet this criteria. For each theme, extract the name, the price, the key features related to product display and branding, and a direct link to its demo page. 

Next, open another new tab and search for essential Shopify apps for a new e-commerce store focused on natural skincare. We'll call this tab @apps.

In the @apps tab, I need you to find apps for the following categories:
1.  **Inventory Management & Drop Shipping:** An app that can automate inventory tracking and connect with drop shipping suppliers.
2.  **Customer Reviews:** A popular app for collecting and displaying product reviews with photos.
3.  **Email Marketing:** An app to build an email list and send marketing campaigns.
4.  **Custom Product Options:** An app that allows customers to add customizations, like the $5 custom fragrance option Ghusoon offers.

For each of these four categories, find the most recommended app. Please extract the app's name, its primary function, and its pricing structure.

Finally, create a summary table for me. The completion criterion is a single markdown table that compares the top 3 themes from @themes and the top 4 apps from @apps. The table should have columns for "Item", "Category", "Price", and "Key Features/Function".

If you can't find a clear winner in any app category, just pause and ask me before you proceed. Thanks!
```

**Why This Works:**

This prompt is optimized for Comet Agent by using natural, conversational language, as if delegating to a human assistant. It breaks the complex research task into clear, sequential steps (research themes, then research apps, then summarize). The use of `@tab` references (`@themes`, `@apps`) provides precise context anchoring for the agent to work across multiple web pages, which is Comet's key architectural strength. Finally, it defines a clear completion criterion (a summary table) and includes a roadblock protocol ("pause and ask me"), ensuring the agent's autonomy is guided and verifiable.

---

## Platform 2: Claude on Chrome

**Task:** Set up a Shopify store for Ghusoon step by step.

**Optimized Prompt:**

```xml
<instructions>
  You will guide me through the initial setup of a Shopify store for the Ghusoon brand. We will do this step-by-step. Take a screenshot after you complete each numbered step to confirm the action was successful. Ask me for any information you need before proceeding.
</instructions>

<steps>
1.  Navigate to `https://www.shopify.com` and start a free trial. Use the email address provided when you ask for it.
2.  Once inside the Shopify admin panel, navigate to the "Online Store" > "Themes" section.
3.  Find and install the free theme called "Dawn". This will be our base theme.
4.  In the theme customizer, go to "Theme settings" and then "Colors". Adjust the color scheme to match the Ghusoon brand: a dark base with gold, olive, and cream accents. I will provide the hex codes when you ask.
5.  Go to "Theme settings" and then "Typography". Change the heading font to Playfair Display and the body font to Lato. Take a screenshot of the typography settings.
6.  Return to the main admin menu. Go to "Products" and click "Add product". We will create a placeholder for the bestseller, "Vanilla Body Butter". Enter the name, a placeholder description, and a price of $20.00. Take a screenshot of the new product page in the admin panel.
7.  Navigate to "Online Store" > "Pages". Create two new pages: one titled "Our Story" and another titled "Contact Us". Leave the content blank for now. Take a screenshot of the Pages list showing both new pages.
</steps>

<safety>
  You are operating on a live website. It is critical that you follow these safety rules without exception:
  - You must pause and ask for explicit confirmation before submitting any form, completing a purchase, or entering payment information.
  - You must never enter or ask for passwords. If a password is required, pause and notify me.
  - You must never attempt to bypass a CAPTCHA or Multi-Factor Authentication (MFA) challenge. Pause and ask for my help.
  - You must stop immediately and notify me if any action you take results in an unintended change or error.
  - You will take a screenshot after each step in the <steps> section to provide a clear audit trail of your actions.
</safety>
```

**Why This Works:**

This prompt is optimized for Claude on Chrome by using the platform's native XML structure: `<instructions>`, `<steps>`, and `<safety>`. The `<steps>` are broken down into a clear, numbered sequence, which is ideal for browser automation workflows. Crucially, it includes a mandatory and detailed `<safety>` section, which is a non-negotiable requirement for this agent to prevent unintended actions on a live website. The inclusion of screenshot checkpoints provides a verifiable audit trail, which is a best practice for this platform.

---

## Platform 3: Gemini Browser

**Task:** Deep research on building a faith-based natural skincare brand targeting Muslim women, competitive analysis, and marketing strategy.

**Optimized Prompt:**

```xml
<role>
  You are an expert brand strategist and market researcher specializing in faith-based consumer brands. Your analysis must be sharp, culturally nuanced, and grounded in verifiable data.
</role>

<constraints>
  - Your research must focus exclusively on the natural skincare and cosmetics market for Muslim women.
  - All claims must be supported by citations from credible sources (market research reports, academic articles, industry publications).
  - The marketing strategy must be sensitive to Islamic principles and values.
  - The temperature for this task must be set to 1.0.
</constraints>

<context>
  Here is the complete knowledge base for the Ghusoon project:

  **Project Name:** Ghusoon ("Natural Bark" in Arabic)
  **Slogan:** "Ignite your Senses"
  **Core Products:** 100% alcohol-free body butters, oils, and mists made from natural ingredients like olive oil, shea butter, and almond oil.
  **Key Differentiator:** Halal, alcohol-free formulations, inspired by Hadith.
  **Target Audience:** Primarily middle-aged, professional Muslim women in North America.
  **Client:** Mrs. Haq, an African American Muslim mother of 5, who started the business from her home.
  **Current State:** Small-scale sales via word-of-mouth and social media. No formal business structure or e-commerce presence.
  **Goal:** To develop Ghusoon into a sustainable, scalable e-commerce brand that can become a primary source of income.
</context>

<task>
  Perform a Deep Research analysis to create a comprehensive brand and marketing strategy for Ghusoon. Your research must cover three key areas:

  1.  **Competitive Landscape Analysis:** Identify the top 5-7 direct and indirect competitors for Ghusoon in the Halal/faith-based skincare market. For each competitor, analyze their:
      - Brand positioning and messaging.
      - Product range and pricing.
      - Marketing channels (social media, influencers, content marketing).
      - Visual identity and website design.
      - Strengths and weaknesses.

  2.  **Target Audience Psychographics:** Go beyond demographics. Create a detailed profile of the target customer, "Fatima," a 35-45 year old Muslim professional. Analyze her:
      - Values, beliefs, and lifestyle as they relate to consumer choices.
      - Media consumption habits.
      - Online communities and influencers she trusts.
      - Pain points and desires regarding skincare and beauty products (e.g., search for Halal-certified, ethical sourcing, representation).

  3.  **Phased Marketing & Growth Strategy:** Develop a 12-month, milestone-driven marketing plan. The plan should be broken down into four quarters and include specific, actionable tactics for:
      - **Q1 (Launch):** Brand launch, Shopify store go-live, initial social media campaign, and influencer outreach.
      - **Q2 (Build):** Content marketing strategy (blogging, video content around Islamic wellness), email list building, and customer review generation.
      - **Q3 (Scale):** Paid advertising campaigns (Instagram/Facebook), partnerships with Muslim lifestyle bloggers/publications, and exploring Ramadan/Eid campaigns.
      - **Q4 (Expand):** New product development, exploring subscription box models, and potential expansion into international markets.
</task>

<final_instruction>
  Synthesize all your findings from the Deep Research into a single, comprehensive report in markdown format. The report should be well-structured with clear headings for each section of the analysis. Ensure you provide a list of all cited sources at the end.
</final_instruction>
```

**Why This Works:**

This prompt is optimized for Gemini Browser by using its required XML tag structure (`<role>`, `<constraints>`, `<context>`, `<task>`, `<final_instruction>`). It strictly follows the critical "data-before-instructions" pattern by placing the `<context>` block before the `<task>`. The task itself is framed as a "Deep Research" question with a clearly defined scope, which activates Gemini's autonomous research capabilities. The prompt also specifies constraints and a detailed final output format, guiding the model to produce a high-quality, structured report while adhering to the platform's best practices, such as keeping the temperature at 1.0.

---

## Red Team Analysis of Original User Prompt

This analysis evaluates the original user prompt from `pasted_content.txt` to identify weaknesses and explain how the optimized prompts provide a more effective solution.

**Overall Rating of Original Prompt:** 3/10

### 1. Ambiguities and Vague Language

-   **"Improve his prompt" / "process the verbal prompt I have then created"**: This is extremely meta and confusing. The user is asking the AI to improve a prompt that is itself a request to do work. It creates a recursive loop of intent that is hard for an AI to parse. Is the goal to *do the work* or to *fix the prompt*?
-   **"create a notal network of it"**: The user means "nodal network," but the typo and the abstract nature of the request are ambiguous. What does this network represent? What are the nodes and edges? The AI is forced to guess the user's mental model.
-   **"Skillshare text-to-output formulation"**: This appears to be a neologism from the user. It's unclear what "Skillshare" refers to in this context, and "text-to-output formulation" is a verbose way of saying "prompt" or "plan". This jargon introduces significant ambiguity.

### 2. Missing Critical Information

-   **No Clear Deliverable:** The prompt asks for a "finalized product," a "competent business plan," and an "established enterprise," but it doesn't define what these deliverables actually look like. Is it a document? A website? A series of reports? The AI has no clear target.
-   **No Platform Context:** The original prompt is a generic wall of text. It doesn't specify which AI platform it's intended for, making it impossible to tailor the instructions to a specific model's strengths or formatting requirements (e.g., XML tags for Claude, sequential steps for Comet).
-   **Implicit vs. Explicit Tasks:** The user embeds requests inside long, narrative paragraphs (e.g., "search the LC of the company"). These are easily missed and lack the clarity of a direct instruction.

### 3. Structural Weaknesses

-   **Stream of Consciousness:** The prompt is a classic example of a "stream of consciousness" dump. It mixes personal philosophy, business goals, technical requirements, and meta-instructions without any clear structure, hierarchy, or separation of concerns.
-   **Instructions Mixed with Data:** The user intersperses instructions throughout long narrative blocks and quotes. This is a direct violation of the "data-before-instructions" pattern that is critical for long-context models like Gemini and Claude.
-   **Lack of Formatting:** The use of inconsistent markdown, random backticks, and long, unbroken paragraphs makes the prompt difficult for both humans and AIs to read and parse reliably.

### 4. Anti-Patterns Being Used

-   **Telling the AI *How* to Think:** The prompt is filled with instructions like "analyze it, understand it," "think step-by-step," and "critique your reasoning." This is a common anti-pattern; modern AIs don't need to be told how to reason. Instead, they need clear goals and constraints.
-   **Monolithic Instructions:** The entire request is a single, monolithic block of text. This is an anti-pattern for virtually every platform, especially agentic ones that thrive on broken-down, sequential steps.
-   **Vague, Unscoped Goals:** A request to "expand the business exponentially" is not an actionable instruction. It's a high-level desire. Effective prompts translate these desires into concrete, scoped, and verifiable tasks.

### 5. What Would Confuse an AI

-   **The Meta-Request:** The core confusion is the prompt's self-referential nature. An AI would struggle to determine if its primary task is to *execute the business plan for Ghusoon* or to *rewrite the prompt about the business plan for Ghusoon*.
-   **Conflicting Instructions:** The prompt asks the AI to "output the final answer first" but then provides a long, rambling set of instructions that don't lead to a single "answer."
-   **User-Specific Jargon:** Terms like "notal network" and "Skillshare text-to-output formulation" are undefined and specific to the user's mental model, forcing the AI to hallucinate their meaning.

### How the Optimized Prompts Fix These Issues

-   **Platform-Specific Formatting:** Each optimized prompt uses the precise formatting (XML tags, natural language steps) that its target platform is designed to understand. This eliminates structural ambiguity.
-   **Clear, Scoped Tasks:** Instead of a vague request to "build a business," the optimized prompts define concrete, achievable tasks: "research Shopify themes," "set up a Shopify store," and "perform a deep research analysis."
-   **Separation of Concerns:** The optimized prompts cleanly separate context, instructions, and safety/constraints. This follows best practices like data-before-instructions and makes the AI's job easier.
-   **Actionable & Verifiable Steps:** The prompts use numbered steps and clear completion criteria (e.g., "create a summary table," "take a screenshot"), making the AI's work verifiable and its process transparent.
-   **Elimination of Meta-Instruction:** The optimized prompts focus on the *what* (the deliverable) and not the *how* (the AI's internal reasoning process), removing the confusing and unnecessary meta-commentary.
