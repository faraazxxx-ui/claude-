# Optimized Prompt: Manus AI Platform

This is the formalized, refined version of the user's original verbal request, restructured using platform-specific optimization patterns from the Prompt Optimizer skill. It is designed to be pasted directly into Manus AI for maximum execution quality.

---

## Optimized Prompt (Ready to Paste)

```
Conduct a comprehensive OSINT-driven geopolitical and economic risk assessment for a Dubai-based 
shipping company and its owner, then produce an actionable risk mitigation document.

## Subject Profile
- Owner: Haseeb Rahman, born February 25, 1962, Indian passport holder, Dubai resident
- Company: Minecore — raw materials export via Dubai ports (dry bulk carriers)
- Assets: Houses, apartments, and property in Dubai; assets in India
- Current Status: Ships held back in dock due to ongoing maritime crisis

## Requirements
1. OSINT Company Intelligence: Search for Minecore (also "Mincore FZE", "Mincore Shipping FZCO") 
   in UAE registries, maritime databases (MarineTraffic, Equasis, VesselFinder), and trade directories. 
   Identify vessels, corporate structure, and any publicly available financial data.
2. OSINT Person Intelligence: Search for Haseeb Rahman in connection with Dubai shipping, business 
   registrations, LinkedIn, and public records.
3. Maritime Crisis Analysis: Assess the current Strait of Hormuz crisis (commenced Feb 28, 2026), 
   Red Sea Houthi disruptions, insurance market collapse, and impact on raw material exporters.
4. Geopolitical Risk Forecast: Provide unbiased analysis (independent of government statements) of 
   the trajectory over 1 week, 1 month, 3 months, 6 months, and 1 year — covering cost of living, 
   quality of life, political reprisals, and loss of assets.
5. Indian Passport Holder Risks: Assess specific vulnerabilities including Indian ED scrutiny, 
   UAE inheritance law changes, capital control risks, and repatriation logistics.
6. Mitigation Strategy: Produce exact, numbered steps for corporate operations (route diversification, 
   insurance, force majeure) and personal assets (jurisdictional diversification, legal ring-fencing, 
   estate planning).

## Constraints
- Use only publicly verifiable information with source citations
- Maintain analytical independence from government narratives
- Frame the document persuasively for a skeptical audience who believes "nothing will go wrong"
- Include specific precedents and data points that counter complacency

## Deliverable
Save as `Dubai_Risk_Assessment_Minecore.md` with sections:
1. Executive Summary
2. Geopolitical Landscape and Maritime Crisis
3. Risk Trajectory Forecast (5 timeframes × 4 dimensions)
4. The "Illusion of Safety" — evidence-based counter-arguments
5. Urgent Mitigation Strategies (Corporate + Personal)
6. OSINT Appendix (tools, sources, information gaps)
7. References

## Verification
- Each major claim has at least one cited source
- Risk trajectory covers all 5 timeframes and all 4 dimensions
- Mitigation strategies are specific and actionable (not generic advice)
- Document is persuasive enough for a skeptical business leader
```

---

## Why This Works (Manus AI Platform Optimization)

This prompt applies the **Goal → Requirements → Deliverable → Verification** pattern native to Manus AI. The numbered requirements enable parallel research execution across independent tracks. The explicit deliverable with file name and section structure ensures Manus produces exactly the document needed. The verification criteria create a self-check loop. The constraint about "skeptical audience" shapes the tone without micromanaging the writing process, which is an anti-pattern on Manus.

---

## Cross-Platform Variants

### Grok Heavy (16 Agents)

```
You are a geopolitical risk analyst specializing in Gulf maritime trade. Your task is to produce 
a comprehensive risk assessment for a Dubai-based shipping company owner.

<data_sources>
Search across: Twitter/X (real-time Gulf shipping disruptions), Reddit (r/dubai, r/shipping, 
r/geopolitics), maritime news (Lloyd's List, TradeWinds), and the broader web.
Focus on: Strait of Hormuz crisis Feb-Mar 2026, maritime insurance cancellations, Dubai expat 
risk factors, Indian nationals UAE asset risks
Time range: Last 90 days
</data_sources>

<task>
1. Aggregate real-time sentiment on Dubai safety from expat communities
2. Track maritime insurance market status for Persian Gulf shipping
3. Identify specific vessel detentions or attacks affecting Dubai-based exporters
4. Assess Indian government actions affecting nationals with UAE assets
5. Compile risk mitigation strategies from maritime industry experts
</task>

<output_format>
## Executive Risk Summary (5 sentences)
## Maritime Crisis Status (table: event | date | impact | source)
## Risk Trajectory (table: timeframe | cost_of_living | quality_of_life | political_risk | asset_risk)
## Mitigation Actions (numbered, specific steps)
## Sources (with URLs)
</output_format>

<failure_policy>
If real-time data is unavailable for a specific metric, state "DATA UNAVAILABLE as of [date]" 
rather than estimating. If conflicting reports exist, present both with source attribution.
</failure_policy>
```

### Perplexity Pro Search

```
What are the specific impacts of the 2026 Strait of Hormuz crisis on Dubai-based raw material 
shipping companies, including maritime insurance availability, vessel detention rates, and 
alternative export routes being used as of March 2026?

Focus on: war risk insurance cancellations, premium increases, route diversions to Omani ports, 
and financial impact on small-to-medium shipping operators.
Prefer sources from: Reuters, Lloyd's List, Al Jazeera, TradeWinds, and official DP World statements.
If reliable data cannot be found for specific metrics, state that clearly rather than speculating.
```

### Gemini Browser (Deep Research)

```xml
<role>
You are a geopolitical risk analyst specializing in Gulf maritime trade and expatriate asset 
protection, with expertise in OSINT investigation techniques.
</role>

<constraints>
- Focus only on developments from January 2026 to present
- Distinguish between verified events and speculative forecasts
- Cite specific companies, dates, and data points
- If a claim cannot be verified from search results, state "unverified" explicitly
- Maintain analytical independence from government press releases
</constraints>

<context>
I am advising a Dubai-based Indian passport holder who owns a raw materials shipping company 
(Minecore). His ships are currently docked due to the maritime crisis. He has significant real 
estate and property assets in Dubai, plus assets in India. He is skeptical that the situation 
will worsen and needs evidence-based persuasion to take protective action.
</context>

<task>
Generate a comprehensive risk assessment covering:
1. Current status of the Strait of Hormuz for commercial shipping (insurance, attacks, route changes)
2. Specific risks for Indian nationals with assets in Dubai (regulatory, legal, financial)
3. Projected risk trajectory over 1 week, 1 month, 3 months, 6 months, and 1 year
4. Concrete mitigation steps for both corporate operations and personal asset protection
5. Evidence-based counter-arguments to the "nothing will happen" mindset
</task>

<final_instruction>
Think step-by-step before answering. For each claim, verify against your search results. 
If the information is not available, say so rather than speculating. Structure the output 
with the most critical findings first, followed by supporting analysis.
</final_instruction>
```
