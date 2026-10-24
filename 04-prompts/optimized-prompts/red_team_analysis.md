# Red Team Analysis: Ghusoon Optimized Prompts v1.0

## Methodology
Each prompt was tested against 5 adversarial dimensions derived from the platform reference docs and the prior red-team CSV methodology used in this repo. Severity: CRITICAL (breaks platform DNA), HIGH (degrades output quality), MEDIUM (suboptimal but functional).

---

## Dimension 1: Structural Integrity (Platform DNA Compliance)

| # | Platform | Severity | Weakness | Fix |
|---|----------|----------|----------|-----|
| 1 | Manus AI | HIGH | Requirements section uses a numbered list (1-8), which implicitly dictates execution sequence. Manus should determine its own optimal path. The numbered list is procedural scripting, not goal specification. | Rephrase as declarative deliverable goals grouped by workstream, not a numbered procedure. |
| 2 | Manus AI | MEDIUM | "Analyze the Ghusoon natural body care business" is a thinking instruction. Manus DNA says: specify WHAT to produce, never HOW to think. "Analyze" is a cognitive verb. | Replace with a concrete outcome statement: "Produce a complete business launch package for Ghusoon..." |
| 3 | Grok Heavy | CRITICAL | The `<task>` block contains a numbered list of 6 steps. This is a major anti-pattern — Grok Heavy expects a single high-level directive, not procedural steps. Numbered steps force it into sequential mode, undermining the 16-agent parallel architecture. | Consolidate into a single research directive with scope parameters. |
| 4 | Grok Heavy | HIGH | The `<context>` section is too sparse. Grok's 256K-2M context window can handle more, but the key issue is that "minimum authoritative context" should be rich enough to prevent agent drift. Missing: pricing data, target market specifics, Mrs. Haq's constraints. | Enrich context with the full nodal network relevant to market research. |
| 5 | Perplexity Pro | MEDIUM | The prompt is good (single question), but it's narrowly scoped to LLC formation only. The user's actual need spans 7 workstreams. A single Perplexity Pro query should be the BEST single question for the user's most urgent need. | Reframe to target the highest-priority unknown: the regulatory/legal landscape for selling body care products, which is the true blocker. |
| 6 | Gemini Browser | HIGH | The `<final_instruction>` mixes natural language with a meta-instruction ("Think step-by-step") and a self-referential question ("Did I answer intent, not just literal words?"). This is mixed-syntax — Gemini's anti-pattern. | Rewrite as clean, direct XML-consistent language without meta-commentary. |
| 7 | Claude Co-work | MEDIUM | Output specifies `~/ghusoon/master_business_plan.pdf` — but Co-work needs to know whether to CREATE a PDF or write markdown that gets converted. The format instruction is ambiguous. | Specify: "Write as markdown. Export final version as PDF." |
| 8 | Claude Code | MEDIUM | "Port the Gemini prototype logic from the attached HTML" — but no file path is given. Claude Code needs exact file references. | Add the specific file path or state "the HTML file in the project root." |

---

## Dimension 2: Anti-Hallucination and Verification

| # | Platform | Severity | Weakness | Fix |
|---|----------|----------|----------|-----|
| 9 | Manus AI | HIGH | Verification criteria are present but lack a failure protocol. What should Manus do if a deliverable can't be completed (e.g., LLC requirements vary by state and the research is inconclusive)? | Add: "If any requirement cannot be fully resolved, document what was found, what remains unknown, and what the user needs to provide." |
| 10 | Claude Chat | MEDIUM | No anti-hallucination instruction. Claude Chat will confidently generate legal and financial information that may be inaccurate. The prompt asks for "estimated cost" without requiring source attribution. | Add: "For all legal requirements and cost estimates, cite the specific source. If a figure cannot be verified, state 'ESTIMATED' with your reasoning." |
| 11 | Claude Co-work | HIGH | Quality criteria say "at least 40 discrete tasks" — this is an arbitrary number that incentivizes padding. Co-work will generate filler tasks to hit the target. | Replace with: "Include all tasks necessary for a complete launch — no padding, no omissions." |
| 12 | Perplexity Computer | MEDIUM | Financial projection requirement says "clearly label all assumptions" but doesn't specify what assumptions to model. This leaves too much to the AI. | Add: "Model assumptions: monthly order volume (conservative: 50, moderate: 150, optimistic: 300), average order value ($15), customer acquisition cost, and repeat purchase rate." |
| 13 | Gemini Browser | MEDIUM | Asks for "top 10 direct competitors" but the halal body care niche may not have 10 well-known competitors. Forcing 10 will produce hallucinated entries. | Change to: "Identify all significant direct competitors (aim for 5-10, but report only those with verifiable information)." |

---

## Dimension 3: Task-Platform Alignment (Right Tool for Right Job)

| # | Platform | Severity | Weakness | Fix |
|---|----------|----------|----------|-----|
| 14 | Perplexity Pro | HIGH | Currently assigned to LLC formation research. But LLC formation is a well-documented, static process — it doesn't need real-time search. Perplexity Pro's unique value is REAL-TIME search. It should be used for something that changes frequently: market trends, competitor pricing, or regulatory updates. | Reassign to: real-time market intelligence on halal beauty trends and competitor activity. |
| 15 | Claude on Chrome | MEDIUM | Currently assigned to LLC research on government websites. This is a reasonable use case but overlaps with Perplexity Pro's assignment. Each platform should have a UNIQUE task that leverages its specific strengths. | Reassign to: Shopify store setup walkthrough — navigating the actual Shopify admin to document the setup process with screenshots. |
| 16 | Comet Agent | MEDIUM | Currently assigned to Shopify App Store research. This is good but could be more ambitious — Comet can do multi-tab comparison shopping across competitor websites too. | Expand scope to include competitor website analysis alongside app comparison. |

---

## Dimension 4: Context Completeness (Nodal Network Coverage)

| # | Platform | Severity | Weakness | Fix |
|---|----------|----------|----------|-----|
| 17 | ALL | HIGH | Mrs. Haq's physical constraint (severe back pain, county job) is mentioned only in Claude Co-work and Gemini Browser. This is a CRITICAL business constraint that should inform every prompt — especially Manus (master plan), Grok (marketing strategy), and Perplexity Computer (automation). | Add Mrs. Haq's physical and time constraints to every prompt where automation or workload is discussed. |
| 18 | ALL | MEDIUM | The Rahman Foundation's zakat/altruistic principles are mentioned but never operationalized. How does this affect pricing strategy? Marketing messaging? Brand positioning? | Add a constraint: "The business model must be consistent with Islamic business ethics (no interest-based financing, fair pricing, community benefit)." |
| 19 | Grok Heavy | HIGH | Missing the user's identity as a physician/MD acting as contractor. This is relevant for market intelligence — the contractor's medical expertise could be a brand differentiator (medically-informed formulations). | Add to context: the contractor is a physician covering startup costs, which informs the "medically-informed" angle. |
| 20 | Claude Code | MEDIUM | Missing the fragrance categories (Softer, Masculine, Imported) that were established in previous AI work. The scent finder quiz needs these categories. | Add the three fragrance categories with example fragrances for each. |

---

## Dimension 5: Safety and Guardrails

| # | Platform | Severity | Weakness | Fix |
|---|----------|----------|----------|-----|
| 21 | Manus AI | MEDIUM | Safety guardrails mention "pause and ask before purchases" but don't address data privacy. Mrs. Haq's personal information (name, address, EIN) should not be stored in plain text files. | Add: "Do not store personal information (SSN, EIN, home address) in any deliverable files. Use placeholders like [MRS_HAQ_ADDRESS]." |
| 22 | Claude Chat | LOW | No safety section at all. While Claude Chat doesn't execute actions, it may generate legal advice that the user acts on. | Add: "This analysis is for planning purposes only. Consult a licensed attorney for legal filings and a CPA for tax setup." |
| 23 | Comet Agent | MEDIUM | The roadblock protocol says "try alternate search terms before reporting" but doesn't set a limit. The agent could loop indefinitely. | Add: "Try up to 3 alternate search terms. If still no results, report the gap and move to the next step." |
| 24 | Perplexity Computer | MEDIUM | No safety guardrail for the financial projection section. The AI may produce projections that the user treats as reliable forecasts. | Add: "Label all financial projections as 'ILLUSTRATIVE — NOT FINANCIAL ADVICE' and recommend consultation with a CPA." |

---

## Summary: 24 Weaknesses Found

| Severity | Count |
|----------|-------|
| CRITICAL | 1 |
| HIGH | 9 |
| MEDIUM | 13 |
| LOW | 1 |
| **Total** | **24** |

All 24 weaknesses will be remediated in the v2.0 rewrite.
