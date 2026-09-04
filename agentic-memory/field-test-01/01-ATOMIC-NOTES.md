# Phase R — Atomic Notes (Field Test #1)

**Schema:** one idea per note • title = the claim • body ≤150 words • source conversation named • confidence band + why • gap flag where evidence is thin.
**Sources:** C1–C5 defined in `00-INVENTORY.md`. **Zero orphan claims** — every note cites a conversation.
**Type:** *Process* = a claim about how he works/thinks. *Content* = a substantive claim inside a conversation.

---

### N01 — He re-issues a near-identical "perfect output / red-team / cognitive wish" prompt until satisfied, with no stated stop condition
- **Type:** Process
- **Source:** C1 (pp. 16 & 21 — the sentence "Redo your output to the perfect output, by performing a red team analysis… equating it closest to the user's inherent cognitive wish" appears verbatim twice, after an initial "redo").
- **Body:** The same meta-instruction fires at least three times in one thread. Each firing makes the AI rebuild from scratch. Because "perfect" and "cognitive wish" are never given an observable test, the loop has no exit — it can recurse indefinitely. This is the exact failure LOOP OS's "done-when" and anti-resonation rules are built to stop.
- **Confidence:** High — identical prompt text is visible on two pages.
- **Gap:** None.

---

### N02 — "Audiovisuals" is his shorthand for "make it a visual/interactive artifact, not prose"; the AI needed 2–3 rounds to operationalize it
- **Type:** Process
- **Source:** C1 (p. 2 "make sure the audiovisuals are always there" → p. 16 "Add audiovisuals too" → p. 21 "Always use Audiovisuals in the output").
- **Body:** The word escalates across turns as the AI keeps returning text. The AI eventually decodes it as "build a React dashboard," which ends the escalation. The intent (a living dashboard) was stable from turn 1; only the AI's interpretation lagged. A one-word gloss ("audiovisual = interactive dashboard") in his standing instructions would collapse this to one round.
- **Confidence:** High for the phrase recurrence; Medium for the intended meaning (inferred from the dashboard being accepted, p. 19).
- **Gap:** No explicit user line confirming "a dashboard is what I meant."

---

### N03 — "Help me visualize this data" is his reflexive second move after any analytical report — verbatim across three separate conversations
- **Type:** Process
- **Source:** C2 (p. 10), C4 (p. 21), C5 (p. 26) — identical string in all three.
- **Body:** The sequence is stable: request analysis → receive report → immediately ask for a visualization. It is predictable enough to pre-empt: delivering the report *and* the dashboard in the first pass would remove an entire round of latency in ~60% of the sampled threads.
- **Confidence:** High — identical string, three independent exports.
- **Gap:** None.

---

### N04 — He front-loads heavy prompt scaffolding — exact schemas, exact formulas, anti-fabrication rules — to constrain the AI before it runs
- **Type:** Process
- **Source:** C2 (pp. 2–4), C4 (pp. 2–15).
- **Body:** Prompts specify CSV column names, parse code, a 5-node scoring formula, tiered alert thresholds, a contraindicated-drug list, and rules ("NEVER fabricate," "cite file + column," "no hedging"). He engineers the guardrails himself rather than trusting defaults. This buys precision but is high-effort and brittle (see N09).
- **Confidence:** High — the scaffolding is the bulk of C2/C4.
- **Gap:** None.

---

### N05 — He versions his master-prompts; the medication-nonadherence prompt is explicitly "v2.0 (Red-Team Validated)," a refinement of the earlier Brugada prompt
- **Type:** Process
- **Source:** C4 (p. 2 title block) vs C2 (p. 2).
- **Body:** C4 restates C2's patient context, data schemas and Loop Score formula in a cleaner, numbered, more defensive form and labels itself v2.0. He treats prompts as maintained software artifacts, not one-off messages — a reuse pattern that the BigQuery/RAG plan is meant to institutionalize.
- **Confidence:** High — version label and near-duplicate structure are both visible.
- **Gap:** None.

---

### N06 — When asked clarifying questions, he delegates the decision back to the AI rather than specifying
- **Type:** Process
- **Source:** C3 (p. 6 — answers: "co0st no matter," "as often as I can," "I want you to recommend the correct answer based upon recomendations").
- **Body:** Faced with three clarifying questions (budget, use pattern, coverage), he removes two constraints ("cost no object," "max wear") and hands the third back ("you recommend"). Implication: clarifying questions are often friction for him; he wants the AI to make the call from evidence. Design consequence — prefer "propose-then-confirm" over "ask-then-wait."
- **Confidence:** High — answers are quoted verbatim.
- **Gap:** Single conversation; may not generalize.

---

### N07 — His corrections target form and depth ("perfect it," "red-team it," "add audiovisuals"), not factual errors — he rarely disputes a specific claim
- **Type:** Process
- **Source:** C1 (pp. 16, 21).
- **Body:** Across the visible correction turns, none says "that number is wrong" or "that citation is off." Every correction pushes for a better *rendering* or a deeper *pass*. Suggests his dissatisfaction signal is about presentation/thoroughness, and that factual verification is currently *not* where he spends his correction budget — a latent risk given content notes below are unverified.
- **Confidence:** Medium — inferred from absence of factual disputes in a small visible set.
- **Gap:** Only C1 contains explicit correction turns.

---

### N08 — He frames the AI as a cognitive *layer* for a self-described "verbal thinker," not merely a tool
- **Type:** Process
- **Source:** C3 (p. 2 — "the expert executor of prompts which forms an additional layer or transformer… aiding a verbal thinker to maximize AI use"). Reinforced by LOOP OS.
- **Body:** The stated self-model is consistent: language in, finished cognition out; the AI does the translation to the technical layer. This is the same premise as the LOOP OS standing instructions — the operating system is his own compensatory response to how he thinks.
- **Confidence:** High — quoted, and echoed by the session's own preamble.
- **Gap:** None.

---

### N09 — The same patient data, date, and formula produced two different Loop Scores (6.7/10 vs 5.7/10) across two conversations — the answer flips on how missing same-day inputs are handled
- **Type:** Process (fragility) / Content
- **Source:** C2 (p. 8 — LS 6.7, notes IN=0 "only because today's Visible entries are incomplete") vs C4 (p. 20 — LS 5.7 WARNING).
- **Body:** Both target 2026-03-15, the same person, the same 5-node formula. The scores diverge mainly on the Inflammatory/PEM node, which depends on same-day symptom logging that was partially absent. A headline metric that swings ~1 point on data completeness is fragile; it needs an explicit "data-completeness" flag beside the score.
- **Confidence:** High for the two numbers; Medium for pinning the delta to the IN node (both reports flag incomplete same-day data).
- **Gap:** Raw CSVs not in session — cannot recompute.

---

### N10 — Across both clinical reports the AI independently ranks propranolol non-adherence as the #1 intervention
- **Type:** Content (AI-output observation, not clinical advice)
- **Source:** C2 (p. 9 — "Propranolol today and daily… drops PN 2.0→0.0"), C4 (p. 20 — "Priority #1: propranolol adherence recovery to ≥90%").
- **Body:** Independently of my judgment, both reports surface the same dominant real-world lever: adherence (reported 38% / 20% / "8 consecutive missed doses"). It is the most stable finding the data produces. Recorded here as a *recurring signal in his corpus*, not as a medical recommendation.
- **Confidence:** High that both reports ranked it #1.
- **Gap:** Adherence % are AI-reported from CSVs not present; unverified.

---

### N11 — He is building a meta-system ("Biological AI Second Brain," CNN→RNN→RL) whose purpose is to automate the very n-of-1 analysis he keeps requesting by hand
- **Type:** Process / Content
- **Source:** C1 (pp. 3–4, 9–15).
- **Body:** CNN = feature extraction from raw wearable inputs; RNN = longitudinal memory; RL = experiment selection. He maps each layer to real research systems (GluFormer, Apple's foundation model, PHIA, Thompson-sampling bandits). The through-line across all five conversations: turn personal biometric data into a self-improving retrieval/decision system — the same ambition as this Agentic-Memory field test.
- **Confidence:** High — architecture is spelled out.
- **Gap:** Aspirational design; no evidence any of it is deployed.

---

### N12 — Substrate: the "5-node Loop Score" is his custom composite health metric, defined by explicit formula
- **Type:** Content
- **Source:** C4 (pp. 5–6), C2 (p. 3).
- **Body:** LS = (Autonomic + Sleep + Inflammatory/PEM + Pharmacologic + Deconditioning) / 15 × 10, each node 0–3. Bands: 0–3 stable, 3–5 monitoring, 5–7 warning, 7–10 critical. This is his invented instrument for compressing multi-stream data into one number — the kind of durable definition worth persisting to the wiki/RAG.
- **Confidence:** High — formula quoted.
- **Gap:** None (definition); validity of the instrument is out of scope.

---

### N13 — Substrate: self-reported clinical profile stated in-prompt
- **Type:** Content
- **Source:** C2 (p. 2), C4 (p. 2).
- **Body:** Age 32; Boston Scientific ICD (Feb 2023, follow-up overdue); Long COVID, POTS, Brugada (SCN5A suspected), DM2, active VZV (3rd recurrence), ME-CFS overlap; baseline (n=166 days) HRV ~20 ms, RHR ~84 bpm, Recovery 36%, Sleep ~5 h. This is user-supplied context, not a verified record.
- **Confidence:** High that it is *stated*.
- **Gap:** Unverified medical history; treat as declared, not confirmed.

---

### N14 — Substrate: behavioral/dietary identity surfaced from his own data
- **Type:** Content
- **Source:** C1 (pp. 23–25).
- **Body:** From his files the AI reports: Halal 100%, intermittent fasting ~35% of days, magnesium + L-theanine supplementation, ~0% alcohol, ~12% caffeine; corpus size WHOOP 277 days, Oura 62 days, 1,399 journal entries with 47 unique questions. These journal entries are named as the RL "training signal" for the second-brain system.
- **Confidence:** High that the AI reported them; Medium that the figures are exact (CSVs not in session).
- **Gap:** Underlying files unverified.

---

### N15 — Substrate: meal decode headline (C1)
- **Type:** Content
- **Source:** C1 (pp. 4–6).
- **Body:** Bread + Nutella + peanut butter ≈ 525 kcal at ~49/41/10 fat/carb/protein; Nutella ~57% sugar by weight; peanut butter blunts the glucose spike ~30% (attributed to Niederhoffer 2018, PMID 30395790). Optimal protocol offered: morning, peanut-butter-first, whole-wheat.
- **Confidence:** Medium — AI synthesis with PMIDs, not independently verified here.
- **Gap:** Citations unverified in this session.

---

### N16 — Substrate: POTS pharmacotherapy ranking (C5)
- **Type:** Content
- **Source:** C5 (pp. 5–7, 16).
- **Body:** Synthesis ranks ivabradine and low-dose (20 mg) propranolol as strongest heart-rate-control evidence; guanfacine as the best *dual* POTS+ADHD agent (reported 85% response in hyperadrenergic POTS, Okamoto 2024). Fludrocortisone weak; midodrine/salt/compression complementary.
- **Confidence:** Medium — peer-reviewed-tagged, unverified here.
- **Gap:** Citations unverified.

---

### N17 — Substrate: GLP-1 risk thesis (C5)
- **Type:** Content
- **Source:** C5 (pp. 11–12, 22–24).
- **Body:** GLP-1 agonists flagged as high-risk *for him*: they raise heart rate via a sinus-node mechanism that ivabradine cannot block, and suppress HRV ~6 ms (Grosicki 2025) — dangerous from his already-low baseline. Net recommendation: defer pending LoCITT-T / RECOVER-TLC trials.
- **Confidence:** Medium — mechanistic claims tagged peer-reviewed, unverified here.
- **Gap:** Citations unverified.

---

### N18 — Substrate: MCAS-as-driver thesis + empiric antihistamine trial (C5)
- **Type:** Content
- **Source:** C5 (pp. 18–20).
- **Body:** Mast Cell Activation Syndrome (an over-reactive-mast-cell condition) is framed as a likely under-diagnosed driver of his POTS via a mast-cell↔sympathetic feedback loop; an empiric H1/H2 antihistamine trial (e.g., cetirizine + famotidine) is presented as low-risk/high-reward.
- **Confidence:** Medium — tagged peer-reviewed, unverified here.
- **Gap:** Citations unverified; diagnostic hypothesis, not a diagnosis.

---

### N19 — Gap-note: C3's actual deliverable is absent from the export
- **Type:** Process (data integrity)
- **Source:** C3 (p. 6 — thread ends at "Tool: launch_extended_search_task").
- **Body:** The compression-wrap conversation is captured only up to the moment research launches; no product list, no recommendation, no pressures/sizing appear. Any downstream claim about "what he was told about compression" must come from C5's corroborating evidence (abdominal > leg-only, 20–30 mmHg; C5 p. 8), not from C3 itself.
- **Confidence:** High — the truncation point is visible.
- **Gap:** The deliverable itself is the gap.

---

# Round 2 additions — C6–C8 (ChatGPT, legal, Oct 2025) and cross-corpus notes

---

### N20 — All three ChatGPT threads open with him re-priming a standing instruction set ("Living Notebook mode")
- **Type:** Process
- **Source:** C6, C7, C8 — the first assistant turn in each is "✅ Living Notebook mode resumed," listing the same five processing rules (parse → analyse → structure → tag/index → triage).
- **Body:** The operating instructions do not persist, so every session begins with a re-priming tax before any work happens. Three sessions, three re-primes, identical mode. This is the same problem LOOP OS and this repository exist to solve: the instruction set has to live in a file, not in a chat window.
- **Confidence:** High that re-priming occurred in all three — the acknowledgment is explicit and identical.
- **Gap:** His actual priming text is not captured (see N21); only the AI's readback of it.

---

### N21 — The ChatGPT exports contain only assistant turns; his own messages are absent
- **Type:** Process (data integrity)
- **Source:** C6, C7, C8 — every block is headed "## Response:". No user turns anywhere.
- **Body:** What he asked has to be reconstructed from what the AI answered. Some is recoverable with high confidence (the AI quotes or paraphrases his instruction), but every behavioural claim drawn from C6–C8 is one inference-step removed from the Claude notes, where his prompts are visible verbatim.
- **Confidence:** High — structural and plainly visible.
- **Gap:** This *is* the gap. Re-export with user messages included (G10).

---

### N22 — He applies the same architecture metaphor to a second, unrelated domain: a "Convolutional Narrative Network" map of his litigation
- **Type:** Process
- **Source:** C6 (CNN Map v2, then v3 — nodes N1–N18, edges, legal axes A1–A6, "Network Flow," "corrective back-propagation") vs C1 (biological CNN→RNN→RL second brain).
- **Body:** Health data and legal causation get the same treatment: entities as nodes, relationships as edges, a layered flow from input to output, and a feedback loop. The metaphor engine is domain-independent. This is the single finding that most changes the map — the scaffolding pattern is not a health-analysis habit, it is how he structures any complex problem.
- **Confidence:** High — both maps are explicit and labelled.
- **Gap:** None for the observation. Whether the metaphor helps or misleads is out of scope.

---

### N23 — He versions artefacts in the legal domain exactly as he does in the health domain
- **Type:** Process
- **Source:** C6 (CNN Map **v2** → **v3**; "Affidavit A" / "Affidavit B") vs C4 (master-prompt **v2.0, Red-Team Validated**).
- **Body:** Same behaviour, different subject: produce, label a version, then merge and strengthen into the next. C6's v3 is explicitly described as merging the earlier map with new material. Confirms N05 across platform and domain.
- **Confidence:** High — version labels visible in both.
- **Gap:** None.

---

### N24 — The reflexive second move is "render it as a deliverable" — a dashboard for data, a court-ready PDF for law
- **Type:** Process
- **Source:** Health — "Help me visualize this data" (C2 p.10, C4 p.21, C5 p.26). Legal — every C6/C7/C8 thread pivots from a markdown/YAML node to a generated PDF (C6: 4 PDFs; C7: 5 PDFs; C8: 2 PDFs).
- **Body:** P3 generalises. The constant is not "charts" — it is that a structured answer is only finished once it becomes an artefact. The medium is domain-dependent. Practical consequence: the artefact should ship in the first pass, whatever the domain.
- **Confidence:** High for the pattern (6 of 8 conversations); Medium for reading the two forms as one underlying drive — that is inference.
- **Gap:** His request wording in C6–C8 is not visible (N21).

---

### N25 — He explicitly instructed the assistant to stop asking for confirmations and take initiative
- **Type:** Process
- **Source:** C6 — "Understood. I'll take full initiative on drafting and optimizing all filings without pausing for minor confirmations." Live corroboration: this session's own instruction, "Re-run and automatically proceed to next step."
- **Body:** Confirms N06 on a second platform, in a second domain, a year apart. Clarifying questions are friction, not help. The design rule that follows is propose-then-confirm: produce the draft, state the assumption, let him correct it.
- **Confidence:** High that the instruction was given — the AI's readback is verbatim-style and it changed behaviour immediately afterwards.
- **Gap:** His exact wording not captured (N21).

---

### N26 — Five consecutive assistant turns in C7 asked for confirmations before producing a single document
- **Type:** Process (measured stall)
- **Source:** C7 — sequential requests for: institution identifiers → tone (formal-legal vs empathetic) → address/date vs placeholders → one combined block vs separate files → typeface and line spacing.
- **Body:** Five round-trips of formatting questions before the first deliverable. Every one of them was answerable by proposing a default and noting it. This is the concrete cost of ask-then-wait, and it is the highest-leverage stall in the corpus because it is entirely avoidable by the responder.
- **Confidence:** High — the five turns are consecutive and visible.
- **Gap:** His replies are absent, so his tolerance for each question is unknown.

---

### N27 — C8 ends with the same question asked three times in a row; four promised documents were never produced
- **Type:** Process (measured stall)
- **Source:** C8 — the final three assistant turns each request "the approximate starting month of financial loss." Thread ends there. The Legal Memorandum, Affidavit of Fact, Financial Loss Statement and Health Impact Declaration are all promised and absent.
- **Body:** The mirror image of N01. In N01 he loops because no exit test was defined; here the assistant loops because it will not proceed without one datum. Same failure, opposite direction: **the loop stalls whenever neither side holds a stop rule.** A default-and-flag ("assuming April 2024 — correct me") would have delivered four documents.
- **Confidence:** High — three identical consecutive requests are visible.
- **Gap:** Cannot tell whether he replied and the export dropped it (N21), or the thread genuinely died.

---

### N28 — In this corpus, initiative produced deliverables and confirmation-seeking produced none
- **Type:** Process
- **Source:** C6 (after "take full initiative": 4 PDFs + 2 full maps delivered, and one turn states "Next, I will automatically proceed"), C7 (5 confirmation turns → PDFs eventually delivered, promised markdown set never), C8 (deadlock → nothing), C3 (clarifying questions → deliverable absent).
- **Body:** The two threads that ended with nothing delivered both ended on a confirmation question. The thread where he told the assistant to act produced the most artefacts. Not absolute — C7 shows confirmations can eventually yield — but the direction is consistent across four conversations and two platforms.
- **Confidence:** Medium — n=4, and his turns are not visible, so cause and effect cannot be fully separated.
- **Gap:** Needs the remaining conversations to test.

---

### N29 — He runs the same operating pattern on two different AI platforms
- **Type:** Process
- **Source:** C1–C5 (Claude) and C6–C8 (ChatGPT): heavy front-loaded scaffolding, versioned artefacts, render-to-deliverable second step, initiative preferred over questions, node/edge architecture metaphors.
- **Body:** The strongest available test of whether these are his patterns or one model's habits — and they replicate. This retires most of the original G9 concern. Caveat: both systems are instruction-following assistants with broadly similar training, so replication is good evidence, not proof.
- **Confidence:** Medium — the patterns clearly appear on both; the inference "therefore his, not the AI's" is strong but not conclusive.
- **Gap:** A third, structurally different system (or his handwritten notes) would settle it.

---

### N30 — The externalised-memory project predates the "second brain" design by about five months
- **Type:** Process / Content
- **Source:** C6/C7/C8 — a working schema in Oct 2025: `RLN_ID: RLN20251014-*` codes, YAML front-matter, tags, backlinks, an explicit `/Living Notebook/03_Projects/...` folder tree, SCQH + MECE triage, Now / Next 2 / Later horizons, "Danger Radar." Versus C1 (Feb–Mar 2026) proposing CNN→RNN→RL to automate it.
- **Body:** The first genuinely longitudinal observation in the corpus. He was hand-running a structured second brain in October 2025; the 2026 architecture is an attempt to automate what he was already doing manually. This field test is the third iteration of the same project.
- **Confidence:** High — RLN date codes and export stamps are explicit on both ends.
- **Gap:** The Oct 2025 → Feb 2026 middle is missing; whether the RLN was sustained or abandoned is unknown.

---

### N31 — His own instruments use decimal scores; his instruction to me forbids them
- **Type:** Process
- **Source:** C2 (Loop Score 6.7/10), C4 (5.7/10), C8 (severity 90/100 from Impact 10 × Urgency 10 × Risk 9 − Effort 7) versus his standing rule: "Confidence = High / Medium / Low + one line of why. **Never a decimal.**"
- **Body:** Not a contradiction — a boundary. Numbers he computed from data are wanted; numbers the AI invents to sound precise are not. The rule is anti-false-precision, not anti-quantification. Practical read: give him bands for judgment and exact figures only where they trace to a source.
- **Confidence:** High that both exist; Medium for this interpretation of why.
- **Gap:** He has not stated the rationale; this is inference.

---

### N32 — He scores and triages every map he builds
- **Type:** Process
- **Source:** C8 (severity 90 → "Critical Priority / Immediate Action"), C2/C4 (Loop Score with 4 named bands), C6 ("Danger Radar" risk × severity × urgency tables), C7 (Now / Next 2 / Later).
- **Body:** Across both domains, a structured map is immediately followed by a triage layer that converts it into a single priority verdict. Four conversations, two domains, two platforms. Strong predictor of what he will ask for next after any map (see `05-PHASE-P.md`).
- **Confidence:** High — explicit scoring instruments in four conversations.
- **Gap:** None for the observation; instrument validity is out of scope.

---

### N33 — Content: the legal claim structure he is assembling (declared, not adjudicated)
- **Type:** Content
- **Source:** C6, C7, C8.
- **Body:** Six legal axes: employment retaliation (Title VII, FMLA 29 CFR §825.220), privacy (HIPAA 45 CFR §164.530(b), §164.508), education due process (ACGME IV.C.1.e), civil rights (§1983/1985), defamation, immigration hardship. Damages ledger subtotal **$693,000** across 8 line items. Causation chain: academic-record falsification → licensure block → employment loss → housing, insurance and health harm. Filing deadlines tracked (EEOC 300-day, HHS OCR 180-day).
- **Confidence:** High that these are the assertions in his affidavits and RLN nodes.
- **Gap:** **Unverified and unadjudicated.** No court records, exhibits or filings are in this session. Recorded as the content of his corpus, not as findings of fact — and this note carries no legal opinion.

---

### N34 — The two reference files are not conversations and cannot support behavioural claims
- **Type:** Process (data integrity)
- **Source:** R1 `examples.md`, R2 `cybertruck_domain_knowledge.md`.
- **Body:** Both are distilled reference material with no dialogue and no ask→outcome sequence. R1 (prompt-optimisation examples across 10 platforms) matches the `prompt-optimizer` skill in his workspace and may be third-party content — authorship is unknown. R2 (Cybertruck 48V jump-start facts, NYC sourcing) is a personal fact sheet. What they show, weakly: he maintains structured reference files for both tooling and one-off practical problems, consistent with N30.
- **Confidence:** High that they are not conversations; Low for any behavioural inference from them.
- **Gap:** Authorship of R1 unknown (G12).

