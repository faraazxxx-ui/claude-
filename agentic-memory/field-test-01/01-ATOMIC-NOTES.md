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
