export interface PromptData {
  id: number;
  platform: string;
  shortName: string;
  category: "anthropic" | "xai" | "perplexity" | "google";
  description: string;
  prompt: string;
  whyItWorks: string;
  redTeamFixes: string[];
  severity: "critical" | "high" | "medium";
  icon: string;
}

export const nodalNetwork = [
  { node: "Company", details: 'Ghusoon ("Natural Bark") \u2014 natural body care, alcohol-free oils and body butters' },
  { node: "Founder", details: "Mrs. Haq \u2014 middle-aged African American Muslim woman, 5 children, Binghamton NY" },
  { node: "Origin", details: "Inspired by Hadith on olive oil benefits for skin; 6 years in operation" },
  { node: "Products", details: "Body butters/Shea butter, body oils, mists, hair/beard care, medicinal; flagship = Vanilla" },
  { node: "USP", details: "Alcohol-free, olive oil base, faith-inspired, handcrafted, medically-informed (via contractor)" },
  { node: "Slogan", details: '"Ignite Your Senses"' },
  { node: "Target Market", details: "Middle-aged, Muslim, African American women" },
  { node: "Current Sales", details: "Word of mouth, Instagram, direct shipping to known customers" },
  { node: "Contractor", details: "User (physician/MD) \u2014 offering services and covering startup costs under Rahman Foundation" },
  { node: "Legal Structure", details: "Ghusoon LLC to be formed under Rahman Corporation umbrella" },
  { node: "Rahman Foundation", details: "User\u2019s personal business foundation; healthcare system based on zakat/altruism principles" },
  { node: "Critical Constraints", details: "Mrs. Haq works a county job and has severe back pain \u2014 maximum automation is mandatory" },
  { node: "Urgent Needs", details: "(1) E-commerce website, (2) Online marketplace, (3) Sales/accounting/tax, (4) Drop shipping" },
  { node: "Design Direction", details: '"Sensory Luxury" \u2014 charcoal #1A1A1A, gold #D4A017, olive #556B2F, cream #FDF5E6' },
  { node: "Typography", details: "Playfair Display (headings), Lato (body)" },
  { node: "Platform", details: "Shopify (confirmed from previous analysis)" },
];

export const redTeamSummary = [
  { platform: "Manus AI", failureMode: "Vague outcomes without file names", mitigation: "Every deliverable has an exact filename and path" },
  { platform: "Claude Chat", failureMode: "Data mixed with instructions", mitigation: "XML tags cleanly separate context, instructions, output format" },
  { platform: "Claude Co-work", failureMode: "Micromanaged steps", mitigation: "Outcome-only description with quality criteria for self-assessment" },
  { platform: "Claude Code", failureMode: "Skipped verification", mitigation: "TDD pattern with specific price calculations as test cases" },
  { platform: "Grok Heavy", failureMode: "Procedural task list (CRITICAL)", mitigation: "Single high-level research directive for 16 parallel agents" },
  { platform: "Perplexity Pro", failureMode: "Wrong task assignment", mitigation: "Reassigned to real-time regulatory compliance search" },
  { platform: "Perplexity Computer", failureMode: "Under-scoped project", mitigation: "6 workstreams with specific data sources and modeling assumptions" },
  { platform: "Comet Agent", failureMode: "No retry limit on roadblocks", mitigation: "Capped at 3 alternate search terms before reporting gap" },
  { platform: "Claude Chrome", failureMode: "Legal risk on gov portals", mitigation: "Reassigned to Shopify Help Center with full safety guardrails" },
  { platform: "Gemini Browser", failureMode: "Mixed-syntax instructions", mitigation: "Clean XML-consistent language, flexible competitor count" },
];

export const prompts: PromptData[] = [
  {
    id: 1,
    platform: "Manus AI",
    shortName: "Manus",
    category: "anthropic",
    description: "Master orchestrator \u2014 produces the complete business launch package with 8 deliverable files",
    icon: "\u2699\uFE0F",
    severity: "high",
    prompt: `Produce a complete business launch package for Ghusoon, a natural body care business owned by Mrs. Haq, an African American Muslim woman in Binghamton, NY. The business is transitioning from 6 years of word-of-mouth sales to a fully operational e-commerce enterprise under the Rahman Corporation umbrella.

## Requirements
- Create a \`ghusoon_nodal_network.md\` that synthesizes all attached files (previous Claude, Grok, and Gemini conversations; verbal write-up; business context)
- Design a Shopify e-commerce specification (\`ghusoon_shopify_spec.md\`) following the "Sensory Luxury" aesthetic (charcoal #1A1A1A, gold #D4A017, olive #556B2F, cream #FDF5E6; Playfair Display + Lato fonts)
- Draft LLC formation documents (\`ghusoon_llc_formation.md\`) for "Ghusoon LLC" under Rahman Corporation in New York State
- Produce a tax and bookkeeping setup guide (\`ghusoon_accounting_setup.md\`) with Shopify integration
- Develop a 12-month marketing strategy (\`ghusoon_marketing_plan.md\`) with 2-week, 1-month, 2-month, 3-month, and quarterly milestones
- Architect a drop shipping automation workflow (\`ghusoon_dropship_automation.md\`) for label printing, pickup scheduling, and delivery tracking
- Outline a brand expansion roadmap (\`ghusoon_brand_expansion.md\`)
- Compile a master business plan (\`ghusoon_master_business_plan.md\`) linking all components

## Constraints
- All products are alcohol-free; this is a core brand value tied to Islamic faith
- Target market: middle-aged Muslim African American women (primary), broader natural skincare market (secondary)
- Flagship product: Vanilla body butter
- Pricing: body butters $8-$15 by size; imported fragrances add $4 surcharge; customization adds $5
- CRITICAL: Mrs. Haq works a county job and has severe back pain. The automation workflow MUST minimize her physical workload (e.g., scheduled pickups instead of post office drop-offs).
- CRITICAL: The business model must be consistent with Islamic business ethics (zakat principles, fair pricing, no interest-based financing).
- Pause and ask before any purchases, domain registrations, or irreversible actions
- Do not store personal information (SSN, EIN, home address) in any deliverable files. Use placeholders like [MRS_HAQ_ADDRESS].
- Use MCP integrations (Notion, Google Drive) for progress tracking

## Deliverable
Save all files to \`/home/ubuntu/ghusoon_project/\` directory. Create a \`todo.md\` tracking execution status.

## Verification
- Each deliverable file exists and contains substantive content (not placeholders)
- The nodal network references at least 15 distinct requirements from the source materials
- The marketing plan has specific, dated milestones for each time period
- The master business plan cross-references all component documents
- Failure Protocol: If any requirement cannot be fully resolved (e.g., state-specific legal nuances), document what was found, what remains unknown, and what the user needs to provide.`,
    whyItWorks: "Removed the numbered list in the Requirements section to prevent procedural scripting; Manus will now determine its own optimal execution path. Replaced the cognitive verb \u201CAnalyze\u201D with the concrete outcome \u201CProduce.\u201D Added critical physical constraints for Mrs. Haq and ethical constraints for the Rahman Foundation. Added data privacy guardrails and a failure protocol for unresolved requirements.",
    redTeamFixes: [
      "Removed procedural numbered list \u2192 declarative deliverable goals",
      "Replaced cognitive verb \u201CAnalyze\u201D with outcome verb \u201CProduce\u201D",
      "Added Mrs. Haq\u2019s physical constraints (back pain, county job)",
      "Added Islamic business ethics constraint",
      "Added data privacy guardrails (no SSN/EIN in files)",
      "Added failure protocol for unresolvable requirements",
    ],
  },
  {
    id: 2,
    platform: "Claude Chat",
    shortName: "Chat",
    category: "anthropic",
    description: "Strategic analysis engine \u2014 builds the nodal network, delta analysis, and unified execution plan",
    icon: "\uD83D\uDCAC",
    severity: "medium",
    prompt: `<context>
<document>
<source>Business Overview</source>
Ghusoon ("Natural Bark") is a natural body care company owned by Mrs. Haq, a middle-aged African American Muslim woman with 5 children in Binghamton, NY. She started 6 years ago after discovering Hadith references to olive oil's skin benefits. Products include alcohol-free body butters (Shea butter base), body oils, mists, hair/beard care, and medicinal products. Flagship product: Vanilla body butter. Slogan: "Ignite Your Senses." Current sales: word-of-mouth and Instagram only. Target market: middle-aged Muslim African American women.
</document>

<document>
<source>Business Structure</source>
The user is a physician (MD) operating the Rahman Foundation \u2014 a healthcare-focused entity based on zakat and altruistic principles. Ghusoon LLC will be formed under Rahman Corporation as a subsidiary. The user is acting as contractor, covering overhead expenses for setup and expansion. The medical background provides a "medically-informed" differentiator for the natural products.
</document>

<document>
<source>Operational Constraints</source>
Mrs. Haq works a county job and suffers from severe back pain. Automation of shipping, labeling, and order management is mandatory to minimize physical labor. The business model must align with Islamic business ethics (no interest-based financing, fair pricing, community benefit).
</document>

<document>
<source>Previous AI Work Summary</source>
Claude previously produced: a full website blueprint with "Sensory Luxury" aesthetic (charcoal #1A1A1A, gold #D4A017, olive #556B2F, cream #FDF5E6), Playfair Display + Lato typography, Shopify recommendation, two customer personas (Fatima and Aisha), sitemap with product-type navigation, and a page-by-page content outline. Grok produced: a step-by-step Shopify setup guide with pricing structure. Gemini produced: a working HTML prototype with a scent-finder quiz using the Gemini API.
</document>

<document>
<source>Urgent Requirements</source>
1. E-commerce website on Shopify
2. Online marketplace for purchasing
3. Sales, accounting, tax, invoicing, bookkeeping
4. Drop shipping automation (label printing, pickup, delivery)
5. LLC formation under Rahman Corporation
6. Marketing strategy with quarterly milestones
7. Brand expansion roadmap
</document>

<document>
<source>Product Pricing</source>
Body butters: 2oz $8, 4oz $10, 8oz $15. Imported fragrances: +$4 surcharge. Customization: +$5. 50+ fragrance varieties including Vanilla, Golden Sand, Amber White, Lavender, Rose, Oud, and imported options. Categories: Softer, Masculine, Imported.
</document>
</context>

<instructions>
You are a senior business strategist and e-commerce consultant. Using all the context above, perform the following:

1. Build a comprehensive nodal network that maps every requirement, dependency, and decision point across the business launch. Identify the delta between what has been asked and what still needs to be achieved.

2. Synthesize the previous AI outputs (Claude blueprint, Grok Shopify guide, Gemini prototype) into a unified execution plan that eliminates redundancy and fills gaps.

3. Create a phased business plan with these components:
   - Phase 1 (Weeks 1-2): LLC formation, Shopify account setup, domain registration
   - Phase 2 (Month 1): Website build, product catalog, payment integration
   - Phase 3 (Month 2): Marketing launch, social media strategy, SEO
   - Phase 4 (Month 3): Drop shipping automation, accounting integration
   - Quarterly milestones for Q1-Q4 of the first year

4. For each phase, specify: deliverables, responsible party (Mrs. Haq vs. user/contractor), estimated cost, and dependencies.

5. Identify the top 5 risks to this business launch and propose mitigation strategies.

Think step-by-step through each component. Cross-reference the previous AI work to avoid duplicating effort. For all legal requirements and cost estimates, cite the specific source. If a figure cannot be verified, state 'ESTIMATED' with your reasoning. This analysis is for planning purposes only; recommend consultation with licensed professionals for final execution.
</instructions>

<output_format>
## Nodal Network Analysis
[Visual map using indented lists showing requirements, dependencies, and gaps]

## Delta Analysis
[Table: What Was Asked | What Was Delivered | What Remains]

## Unified Execution Plan
[Phased timeline with deliverables, owners, costs, dependencies]

## Risk Assessment
[Table: Risk | Probability | Impact | Mitigation]

## Immediate Next Actions
[Numbered list of the 5 most urgent actions to take this week]
</output_format>`,
    whyItWorks: "Added explicit anti-hallucination instructions requiring source citations for legal/cost data and clear labeling of estimates. Added a safety disclaimer regarding legal/financial advice. Injected the missing constraints (Mrs. Haq\u2019s back pain, the Rahman Foundation\u2019s ethical principles, the physician/contractor role, and the three fragrance categories) into the <context> blocks.",
    redTeamFixes: [
      "Added anti-hallucination: source citations required for all cost/legal data",
      "Added \u201CESTIMATED\u201D labeling requirement for unverified figures",
      "Added legal/financial advice disclaimer",
      "Injected Mrs. Haq\u2019s physical constraints into context",
      "Added physician/contractor role and fragrance categories",
    ],
  },
  {
    id: 3,
    platform: "Claude Co-work",
    shortName: "Co-work",
    category: "anthropic",
    description: "Autonomous delegation engine \u2014 produces the master business plan and project tracker",
    icon: "\uD83D\uDCCB",
    severity: "medium",
    prompt: `## Goal
Transform the Ghusoon natural body care business from a word-of-mouth operation into a fully operational e-commerce enterprise. Produce a master business plan document and a project tracker that serves as a persistent second brain for ongoing execution. Write all outputs as markdown files, then export the final business plan as a PDF.

## Inputs
- Business context: Ghusoon, owned by Mrs. Haq (African American Muslim woman, Binghamton NY), 6 years old, alcohol-free olive-oil-based body care products, 50+ fragrances, flagship Vanilla body butter
- Legal structure: Ghusoon LLC under Rahman Corporation (user's foundation based on zakat/altruistic principles)
- Design system: "Sensory Luxury" aesthetic \u2014 charcoal #1A1A1A, gold #D4A017, olive #556B2F, cream #FDF5E6; Playfair Display + Lato
- Platform: Shopify (confirmed from previous analysis)
- Pricing: 2oz $8, 4oz $10, 8oz $15; imported fragrance surcharge $4; customization $5
- Constraints: Mrs. Haq works a county job and has severe back pain \u2014 automation of shipping/fulfillment is mandatory. Contractor is a physician (MD) covering startup costs.
- Previous work: Claude website blueprint, Grok Shopify guide, Gemini HTML prototype with scent finder

## Output
~/ghusoon/master_business_plan.md (and .pdf export) \u2014 comprehensive business plan covering LLC formation, Shopify setup, marketing (quarterly milestones), drop shipping automation, accounting, and brand expansion
~/ghusoon/project_tracker.xlsx \u2014 execution tracker with phases, tasks, owners, deadlines, status, and dependencies

## Quality Criteria
- Business plan covers all 7 workstreams: legal, website, marketing, accounting, shipping, automation, expansion
- Each workstream has specific deliverables with estimated costs and timelines
- Marketing plan includes 2-week, 1-month, 2-month, 3-month, and quarterly milestones
- Project tracker includes all tasks necessary for a complete launch \u2014 no arbitrary padding, no omissions. Every task must have an assigned owner (Mrs. Haq or Contractor).
- Risk assessment identifies at least 5 business risks with mitigation strategies
- The automation plan explicitly addresses Mrs. Haq\u2019s physical limitations`,
    whyItWorks: "Resolved the ambiguous file format instruction by explicitly requesting markdown generation followed by PDF export. Removed the arbitrary \u201C40 discrete tasks\u201D metric which incentivizes AI padding, replacing it with a completeness requirement. Added the missing physical and ethical constraints to the Inputs section.",
    redTeamFixes: [
      "Clarified file format: markdown first, then PDF export",
      "Removed arbitrary \u201C40 tasks\u201D metric \u2192 completeness requirement",
      "Added Mrs. Haq\u2019s physical constraints to Inputs",
      "Added ethical/zakat constraints to Inputs",
    ],
  },
  {
    id: 4,
    platform: "Claude Code",
    shortName: "Code",
    category: "anthropic",
    description: "Terminal-based coding agent \u2014 builds the Shopify theme with pricing calculator and scent finder",
    icon: "\uD83D\uDCBB",
    severity: "medium",
    prompt: `Build a Shopify theme customization package for the Ghusoon natural body care store.

Design system: charcoal #1A1A1A, gold #D4A017, olive #556B2F, cream #FDF5E6. Fonts: Playfair Display (headings), Lato (body).

Key features to implement:
1. Product page with size selector (2oz/4oz/8oz) and fragrance dropdown (50+ options) that auto-calculates price including $4 imported fragrance surcharge and $5 customization fee
2. Scent finder quiz (port the Gemini prototype logic from the \`scent_finder_prototype.html\` file in the project root)
3. Fragrance Library page with A-Z listing and category filters (Softer, Masculine, Imported)

Check src/sections/ and src/snippets/ for Shopify Liquid template structure.

Write tests for the pricing calculator logic first, then implement.

Verify: All tests pass. Price for 8oz Vanilla = $15. Price for 8oz imported Oud = $19. Price for 8oz custom imported = $24. The scent finder returns valid recommendations from the three fragrance categories.`,
    whyItWorks: "Added the specific file reference (scent_finder_prototype.html in the project root) so Claude Code isn\u2019t guessing where the logic lives. Added the three specific fragrance categories (Softer, Masculine, Imported) to the verification criteria to ensure the quiz logic ports correctly.",
    redTeamFixes: [
      "Added specific file path for scent finder prototype",
      "Added three fragrance categories to verification criteria",
      "TDD pattern: write tests first, then implement",
      "Specific price verification test cases included",
    ],
  },
  {
    id: 5,
    platform: "Grok Heavy",
    shortName: "Grok",
    category: "xai",
    description: "16-agent deep research \u2014 market intelligence with Twitter/X firehose and Reddit OSINT",
    icon: "\uD83D\uDD2C",
    severity: "critical",
    prompt: `You are a market intelligence and competitive analysis agent. Your objective is to produce a comprehensive market landscape report for Ghusoon, a natural, alcohol-free body care brand targeting middle-aged Muslim African American women, based in Binghamton, NY.

<context>
Ghusoon has been operating for 6 years via word-of-mouth. Products include olive-oil-based body butters, body oils, mists, and hair/beard care. All products are alcohol-free (faith-based requirement). Flagship: Vanilla body butter. Pricing: $8-$15 based on size, with surcharges for imported fragrances. Slogan: "Ignite Your Senses." 

The business is transitioning to Shopify e-commerce under the Rahman Corporation umbrella (a foundation based on zakat principles). The contractor funding the startup is a physician (MD), providing a "medically-informed" angle to the natural products. The owner, Mrs. Haq, has physical constraints requiring high automation.
</context>

<data_sources>
Search across: Twitter/X (full firehose), Reddit (r/SkincareAddiction, r/NaturalBeauty, r/Entrepreneur, r/shopify, r/smallbusiness, r/Hijabis), and the broader web.
Focus on: (1) Consumer sentiment toward alcohol-free/halal body care products, (2) Competitor landscape for faith-based natural skincare brands, (3) Shopify success stories for similar small businesses, (4) Marketing strategies that work for niche body care brands on social media
Time range: Last 12 months
</data_sources>

<task>
Conduct deep OSINT research across the specified data sources to identify top competitors, aggregate consumer sentiment, analyze unmet market needs, and extract proven marketing strategies for faith-based natural body care brands. Synthesize these findings into a strategic SWOT analysis and local market assessment for the Binghamton, NY region.
</task>

<output_format>
## Executive Summary (5 sentences max)
## Competitor Landscape (table: Brand | Products | Price Range | Channels | Social Following | Estimated Revenue | Key Differentiator)
## Twitter/X Sentiment Analysis (table: Theme | Sentiment | Volume | Representative Quote)
## Reddit Insights by Subreddit (table: Subreddit | Dominant Sentiment | Key Unmet Needs | Opportunity for Ghusoon)
## Top 5 Marketing Strategies (numbered list with evidence from successful brands)
## Local Market Assessment (Binghamton + regional expansion potential)
## SWOT Analysis (2x2 table)
## Strategic Recommendations (top 3 actions ranked by impact)
</output_format>

<failure_policy>
If a subreddit has insufficient data (<10 relevant posts), state "INSUFFICIENT DATA for [subreddit]" rather than extrapolating.
If Twitter/X returns no results for a specific theme, state "NOT FOUND" for that theme.
If competitor revenue data is not publicly available, state "ESTIMATED: [range]" or "NOT AVAILABLE" \u2014 never fabricate figures.
</failure_policy>`,
    whyItWorks: "CRITICAL FIX: Replaced the numbered procedural list in the <task> block with a single, high-level research directive. This prevents Grok from falling into sequential execution and allows its 16 parallel agents to deploy optimally. Enriched the <context> block with the missing pricing data, the physician/contractor dynamic, and the ethical/physical constraints.",
    redTeamFixes: [
      "CRITICAL: Replaced procedural numbered list with single research directive",
      "Enriched context with pricing data and physician/contractor role",
      "Added physical constraints for Mrs. Haq",
      "Added ethical/zakat business principles",
      "Explicit failure policy for each data source type",
    ],
  },
  {
    id: 6,
    platform: "Perplexity Pro Search",
    shortName: "Perplexity",
    category: "perplexity",
    description: "Real-time search engine \u2014 FDA regulatory compliance and cosmetic labeling requirements",
    icon: "\uD83D\uDD0D",
    severity: "high",
    prompt: `What are the specific FDA regulations, New York State labeling requirements, and interstate commerce compliance rules for a home-based business manufacturing and selling natural, olive-oil-based body butters and cosmetic oils directly to consumers via e-commerce?

Focus on: FDA Voluntary Cosmetic Registration Program (VCRP) vs. MoCRA requirements, ingredient declaration rules for essential oils and imported fragrances, and any specific New York State Department of Health manufacturing facility requirements for home-based cosmetics.
Prefer sources from: FDA.gov, New York State Department of Health, and established cosmetic regulatory compliance organizations.
If reliable sources cannot be found for any specific requirement, state that clearly rather than speculating.`,
    whyItWorks: "Reassigned the task from generic LLC formation (which doesn\u2019t require real-time search) to the highly complex, frequently changing domain of cosmetic regulatory compliance (MoCRA). This perfectly aligns with Perplexity Pro\u2019s real-time search DNA. Maintained the single-question structure and anti-hallucination directives.",
    redTeamFixes: [
      "HIGH: Reassigned from static LLC research to real-time regulatory search",
      "Single focused question (no multi-part anti-pattern)",
      "Expert terminology: VCRP, MoCRA, ingredient declaration",
      "Preferred source types specified",
      "Anti-hallucination: \u201Cstate that clearly rather than speculating\u201D",
    ],
  },
  {
    id: 7,
    platform: "Perplexity Computer",
    shortName: "Computer",
    category: "perplexity",
    description: "Project execution engine \u2014 comprehensive launch package with 6 workstreams",
    icon: "\uD83D\uDE80",
    severity: "medium",
    prompt: `Build a comprehensive launch package for Ghusoon, a natural, alcohol-free body care brand owned by Mrs. Haq, an African American Muslim woman in Binghamton, NY. The business has operated for 6 years via word-of-mouth and is now transitioning to a full e-commerce operation on Shopify under the Rahman Corporation umbrella.

## Requirements
- Research and compile New York State LLC formation requirements, filing fees, and timeline for forming "Ghusoon LLC" as a subsidiary of Rahman Corporation
- Create a complete Shopify store setup checklist with specific apps for: inventory management, tax calculation (TaxJar or Avalara), shipping label automation (ShipStation or Pirate Ship), and accounting integration (QuickBooks or Xero)
- Develop a 12-month marketing strategy targeting middle-aged Muslim African American women, with specific milestones at 2 weeks, 1 month, 2 months, 3 months, and each quarter
- Research drop shipping and fulfillment automation options suitable for a home-based business with 50+ product variants. CRITICAL: The owner has severe back pain, so solutions MUST emphasize scheduled carrier pickups and zero-lift workflows.
- Identify the top 5 competitor brands in the halal/alcohol-free natural body care space with pricing and distribution analysis
- Create a financial projection for Year 1 based on comparable small body care businesses. Model assumptions: monthly order volume (conservative: 50, moderate: 150, optimistic: 300), average order value ($15), customer acquisition cost, and repeat purchase rate.

## Data Sources
- New York Department of State (LLC filing)
- Shopify App Store and documentation
- IRS.gov (EIN, tax requirements)
- Industry reports on natural/halal beauty market size and growth
- Competitor websites and social media profiles
- Small Business Administration resources

## Final Deliverable
A structured business launch document with: (1) Legal Formation Guide, (2) Shopify Setup Playbook, (3) Marketing Calendar, (4) Automation Architecture, (5) Competitive Analysis, (6) Financial Projections. Export as a downloadable document.

If any data source is unavailable or behind a paywall, state what could not be accessed rather than estimating. Label all financial projections as 'ILLUSTRATIVE \u2014 NOT FINANCIAL ADVICE' and recommend consultation with a CPA.`,
    whyItWorks: "Added explicit modeling assumptions (order volumes, AOV, CAC) to the financial projection requirement to prevent hallucinated baseline metrics. Added a safety disclaimer for the financial outputs. Injected Mrs. Haq\u2019s physical constraints directly into the fulfillment research requirement to ensure the proposed solutions are actually viable for her.",
    redTeamFixes: [
      "Added explicit financial modeling assumptions (50/150/300 orders)",
      "Added \u201CILLUSTRATIVE \u2014 NOT FINANCIAL ADVICE\u201D disclaimer",
      "Injected Mrs. Haq\u2019s back pain into fulfillment research",
      "Specified zero-lift workflow requirement",
      "Added CPA consultation recommendation",
    ],
  },
  {
    id: 8,
    platform: "Comet Agent",
    shortName: "Comet",
    category: "perplexity",
    description: "Browser automation agent \u2014 Shopify App Store research and comparison",
    icon: "\u2604\uFE0F",
    severity: "medium",
    prompt: `I need to research and compare Shopify apps for setting up the Ghusoon natural body care store. The store sells alcohol-free body butters, oils, and mists with 50+ fragrance variants, and needs: tax calculation, shipping label automation, inventory management, and accounting integration.

Steps:
1. Go to the Shopify App Store (apps.shopify.com) and search for "tax calculation" \u2014 compare TaxJar and Avalara. Note pricing, ratings, and key features for each. Screenshot the comparison.
2. Search for "shipping labels" \u2014 compare ShipStation and Pirate Ship. Note pricing, ratings, USPS/UPS integration, and whether they support scheduled home pickups (critical for the owner's back pain). Screenshot the comparison.
3. Search for "inventory management" \u2014 find the top 3 rated apps that handle product variants (50+ fragrance options per product type). Screenshot the top results.
4. Search for "QuickBooks integration" \u2014 find the best-rated app for syncing Shopify sales with QuickBooks. Screenshot the listing.
5. On @tab with the Shopify pricing page (shopify.com/pricing), confirm the Basic plan features and monthly cost.

When done: Create a comparison table with all apps, their monthly costs, ratings, and which Ghusoon needs they address. Calculate the total monthly software cost for the full stack.

If any app page requires login or payment to view details, pause and tell me. If a search returns no relevant results, try up to 3 alternate search terms. If still no results, report the gap and move to the next step.`,
    whyItWorks: "Fixed the indefinite looping risk in the roadblock protocol by capping alternate search attempts at 3. Added the physical constraint (scheduled home pickups) to the shipping label app comparison step, ensuring the agent evaluates the apps against Mrs. Haq\u2019s specific medical need.",
    redTeamFixes: [
      "Capped retry limit at 3 alternate search terms",
      "Added scheduled home pickup requirement to shipping comparison",
      "Added @tab cross-tab context anchor for pricing page",
      "Natural conversational language (Comet\u2019s DNA)",
    ],
  },
  {
    id: 9,
    platform: "Claude on Chrome",
    shortName: "Chrome",
    category: "anthropic",
    description: "Browser extension agent \u2014 Shopify Help Center documentation with screenshots",
    icon: "\uD83C\uDF10",
    severity: "high",
    prompt: `<instructions>
Navigate the Shopify admin interface to document the exact setup process for the Ghusoon natural body care store. Create a visual, step-by-step setup guide with screenshots for Mrs. Haq.
</instructions>

<steps>
1. Navigate to Shopify.com and locate the pricing/signup page (do NOT create an account)
2. Search the Shopify Help Center for "adding product variants" (Ghusoon has 50+ fragrance variants) \u2014 screenshot the instructional steps
3. Search the Help Center for "setting up shipping zones" and "scheduling carrier pickups" \u2014 screenshot the workflows
4. Search the Help Center for "integrating a custom domain" \u2014 screenshot the requirements
5. Compile all findings into a structured setup guide: Account Creation, Product Catalog (with variants), Shipping Configuration (zero-lift pickup focus), and Domain Setup.
</steps>

<safety>
- Do NOT submit any forms, applications, or registrations
- Do NOT enter any personal information, names, or addresses
- Do NOT create any accounts on Shopify or any other website
- If any page requires login or payment, pause and notify me immediately
- Screenshot every key page for my verification before moving to the next step
- If you encounter a CAPTCHA, pause and ask me to complete it
</safety>`,
    whyItWorks: "Reassigned the task from generic LLC research to a highly visual, platform-specific task: documenting the Shopify setup process via the Help Center. This leverages Claude on Chrome\u2019s ability to navigate and screenshot real web interfaces without risking the legal liabilities of interacting with government portals. Maintained all strict safety guardrails against form submission.",
    redTeamFixes: [
      "HIGH: Reassigned from gov portal browsing (legal risk) to Shopify Help Center",
      "Comprehensive safety guardrails: no forms, no accounts, no personal info",
      "Screenshot verification at every checkpoint",
      "CAPTCHA pause protocol included",
    ],
  },
  {
    id: 10,
    platform: "Gemini Browser",
    shortName: "Gemini",
    category: "google",
    description: "Deep research agent \u2014 comprehensive market opportunity and business strategy report",
    icon: "\uD83D\uDC8E",
    severity: "high",
    prompt: `<role>
You are a senior business consultant specializing in e-commerce launches for niche consumer product brands, with deep expertise in the halal/faith-based beauty market and small business operations.
</role>

<constraints>
- Focus only on information from 2024-2026
- Distinguish between verified market data and estimates \u2014 label all estimates clearly
- Cite specific sources for all market size figures, growth rates, and competitor data
- If a claim cannot be verified from search results, state "unverified" explicitly
- Do NOT recommend actions that require significant capital investment (>$5,000) without flagging the cost
</constraints>

<context>
Ghusoon ("Natural Bark") is a 6-year-old natural body care brand owned by Mrs. Haq, an African American Muslim woman in Binghamton, NY. Products include alcohol-free, olive-oil-based body butters, body oils, mists, hair/beard care, and medicinal products with 50+ fragrance options. The flagship product is Vanilla body butter. Current sales are word-of-mouth only via Instagram and personal networks. The business is transitioning to Shopify e-commerce under the Rahman Corporation umbrella (a physician\u2019s foundation based on zakat and altruistic principles). Target market: middle-aged Muslim African American women. Slogan: "Ignite Your Senses."

Key business constraints: Mrs. Haq works a county job and has severe back pain, so automation of shipping, labeling, and order management is critical. The contractor (physician/MD) is covering startup costs. The brand must maintain its alcohol-free, faith-inspired identity while expanding to a broader natural skincare audience.
</context>

<task>
Generate a comprehensive market opportunity and business strategy report covering:

1. What is the current size and projected growth of the halal beauty/personal care market in the United States as of 2025-2026? What percentage of this market is body care specifically?

2. Identify all significant direct competitors in the alcohol-free/halal natural body care space (aim for 5-10, but report only those with verifiable information). For each: product range, price points, distribution channels, social media following, and estimated annual revenue.

3. What marketing strategies have proven most effective for small, faith-based beauty brands targeting Muslim women in the US? Include specific case studies with measurable results.

4. What is the optimal Shopify technology stack (apps, integrations, automation tools) for a home-based body care business with 50+ product variants and a single operator with physical limitations?

5. What are the regulatory requirements for selling body care products (body butters, oils, mists) in New York State and interstate? Include FDA classification, labeling requirements, and any state-specific regulations.

6. Based on comparable businesses, what is a realistic Year 1 revenue projection for Ghusoon\u2019s e-commerce launch? Model three scenarios: conservative, moderate, and optimistic.
</task>

<final_instruction>
Validate your response against the constraints above before finalizing. Structure the output as a professional report with an executive summary, detailed sections for each question, and a strategic recommendations appendix.
</final_instruction>`,
    whyItWorks: "CRITICAL FIX: Removed the mixed-syntax meta-instructions (\u201CThink step-by-step\u201D and \u201CDid I answer intent...\u201D) from the <final_instruction> block. Gemini requires clean, direct XML-consistent language. Modified the competitor requirement from a hard \u201Ctop 10\u201D to \u201Call significant direct competitors (aim for 5-10)\u201D to prevent hallucination in a niche market.",
    redTeamFixes: [
      "CRITICAL: Removed mixed-syntax meta-instructions from <final_instruction>",
      "Changed \u201Ctop 10\u201D to flexible \u201Caim for 5-10, report only verifiable\u201D",
      "Clean XML-consistent language throughout",
      "Data-before-instructions pattern maintained",
      "Constraints at the top per Gemini\u2019s attention architecture",
    ],
  },
];
