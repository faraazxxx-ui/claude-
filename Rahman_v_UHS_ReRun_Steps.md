# Rahman v. UHS — Re-Run of All Legal Requests (Mistake-Free Steps)

**Case:** Mohammed Faraaz Rahman, M.D. v. United Health Services Hospitals, Inc. et al.
**Case No.:** 3:26-cv-00197 (AJB/ML) — U.S. District Court, Northern District of New York
**Plaintiff's Counsel:** Douglas Walter Drazen, Esq.
**Posture:** Post-Answer / Pre-Discovery (Defendants answered March 9, 2026; no Rule 12(b)(6) motions filed)
**Re-run date:** August 17, 2026
**Classification:** Attorney Work Product — Privileged & Confidential

> This document re-runs every Rahman legal request from the prior (private) Mistral chat, in a single canonical sequence, with the cross-track inconsistencies reconciled. Each step lists the request, the canonical answer, the exact command/file to use, and the verification check. Run them in order.

---

## ⚠️ Read First: Reconciled Facts (corrects the 5 cross-track mistakes)

The two prior Rahman tracks in this repo (`legal-endeavors/` and `skills/apex-legal-strategy/`) disagreed on five material points. Everything below uses the **canonical** values. Do not mix the old values into filings.

| # | Issue | Old track A (`legal-endeavors`) | Old track B (`skills/apex-legal-strategy`) | CANONICAL (use this) | Why |
|---|---|---|---|---|---|
| 1 | Acquittal date | August 2025 | September 2025 | **August 2025** (Binghamton City Court) | `case-context.md` timeline + `evidence_checklist.md` Exhibit F + RFA #6 all state August 2025; the Sept 2025 line in track B is unreconciled and would shift the SOL by a month. Confirm exact docket date with Drazen before any SOL filing. |
| 2 | Family wire transfers | 39 wires + 11 Zelle = **$84,747.92** | 38 wires = **$223,800** | **Use the $84,747.92 / 39-wire + 11-Zelle figure** as the *documented minimum* in filings; treat $223,800/38-wire as an unverified alternate count to reconcile, NOT a substitute | case-context.md + evidence_checklist.md give the precise figure ($84,747.92) and transfer counts; the $223,800 figure in track B's evidence-inventory has no matching ledger total and double-counts against the documented minimum. Reconcile the underlying bank statements before any damages demand. |
| 3 | Co-resident's name | **Dr. Sundas Rashid** | "Sundas" (no surname) | **Sundas Rashid** | The malicious-prosecution / defamation claim is *against* her (litigation-playbook Phase 2); use her full name consistently. |
| 4 | Audio recording (Exhibit A: "We knew it is false. We framed him") | Listed as Exhibit A in case-context.md, evidence_checklist.md, litigation-playbook.md | MISSING from apex skill's evidence-inventory.md (which instead lists bodycam, TP-7 field recordings, Sundas statement video) | **Audio admission IS part of the evidence set** | The two tracks have *different evidence inventories*. The audio admission is the single highest-leverage settlement item (litigation-playbook §3 lever #2). It must appear in the canonical evidence inventory. |
| 5 | `FINAL_DELIVERABLE_Rahman_Risk_Assessment.md` | File present | — | **This file is mislabeled** — it is the Minecore shipping/geopolitical risk report (Haseeb Rahman, Strait of Hormuz), NOT a Rahman v. UHS legal risk assessment | The filename implies a legal deliverable that does not exist. A real Rahman v. UHS legal risk assessment is created in Step 11 below. |

---

## The 11 Requests, Re-Run In Order

### Step 1 — Case Context Master File
**Request:** "Build the master case-context file: identity, parties/counsel, timeline, causes of action, defendants' answers, evidence inventory, damages, legal theories, deadlines."
**Canonical file:** `legal-endeavors/references/case-context.md`
**Action:** Read it; it is the single source of truth and is already current. No edits needed.
**Verify:**
- [ ] Caption lists all 5 defendants (UHS, Ahmed, Nadeem, Rehman, Ali)
- [ ] Federal case number = 3:26-cv-00197 (AJB/ML)
- [ ] 4 causes of action present (Title VI; tortious interference; breach of contract; injunctive relief)
- [ ] Acquittal shown as August 2025 (canonical)
- [ ] Damages framework table present ($1.05M economic / $1.5–3M non-economic / $1–2M punitive → $4.2M–$6.8M)

```
cat legal-endeavors/references/case-context.md
```

---

### Step 2 — Case Timeline & Causal Chains
**Request:** "Map the chronological spine plus the causal chains and open gaps."
**Canonical file:** `skills/apex-legal-strategy/references/case-timeline.md`
**Action:** Read it. Note the 4 causal chains (Engagement→Retaliation→Sabotage; Medical Emergency→Institutional Exploitation; HIPAA Breach→Criminal Complaint→Prosecution; Institutional Pattern→Federal Liability) and the open gaps list.
**Verify:**
- [ ] All 4 chains present
- [ ] Chain 3 ends at "NOT GUILTY with prejudice → malicious prosecution claim"
- [ ] Open gaps list includes: false-verger dates/authors, Florida-contract notice, Sundas-family instigation chain, EEOC charge status, Nadeem identity

```
cat skills/apex-legal-strategy/references/case-timeline.md
```

---

### Step 3 — Defendant Answers: Paragraph-Level Analysis
**Request:** "Analyze both Answers (Doc 11 Ahmed / Doc 12 UHS group) paragraph-by-paragraph and extract exploitable contradictions."
**Canonical file:** `skills/apex-legal-strategy/references/defendant-answers.md`
**Action:** Read it. The 4 "gold nuggets": (1) Ahmed ¶2 admits association, denies influence; (2) Ahmed ¶10 admission; (3) UHS AF 7 same-decision = Mt. Healthy implicit admission; (4) AF 6 vs AF 8 internal contradiction.
**Verify:**
- [ ] Ahmed's 7 affirmative defenses listed
- [ ] UHS group's 10 affirmative defenses listed
- [ ] Contradiction matrix present
- [ ] Cross-group divergence strategy (Ahmed separate counsel = conflict/indemnification signal)

```
cat skills/apex-legal-strategy/references/defendant-answers.md
```

---

### Step 4 — Defense Analysis: Countering All 17 Affirmative Defenses
**Request:** "Produce a counter-strategy for each affirmative defense, with the best evidence and legal framework per theme."
**Canonical file:** `legal-endeavors/references/defense-analysis.md`
**Action:** Read it. All 17 defenses (Ahmed ×7, UHS group ×10) countered; counter-strategy matrix maps defense theme → best evidence → legal framework (Staub v. Proctor; McDonnell Douglas; National R.R. Passenger Corp. v. Morgan).
**Verify:**
- [ ] 7 Ahmed defenses + 10 UHS-group defenses each have a counter-strategy
- [ ] Counter-strategy matrix has 6 themes ("didn't know" / "legitimate reasons" / "too late" / "not our fault" / "caps" / "didn't mitigate")
- [ ] Continuing-violation + discovery-rule from Aug 2025 acquittal both cited for SOL defense

```
cat legal-endeavors/references/defense-analysis.md
```

---

### Step 5 — Damages Calculator
**Request:** "Build the damages framework with three scenarios and per-category evidence checklist + expert needs."
**Canonical file:** `skills/apex-legal-strategy/references/damages-calculator.md`
**Action:** Read it. Three scenarios: $1.2M conservative / $2.5M moderate w/ punitives / $4.9M full claim.
**⚠️ Reconciliation note:** This file's "Family wire transfers (father) $223,800 / 38 wires" figure is the **unverified alternate**. In any filing, state family support as the documented minimum **$84,747.92 across 39 wires + 11 Zelle transfers** (per case-context.md) and reconcile the ledger before the settlement demand.
**Verify:**
- [ ] Three scenario totals present ($1.2M / $2.5M / $4.9M)
- [ ] Lost salary stated as **per-year** ($300K/yr) with explicit duration assumption
- [ ] Punitive range 1:1–3:1 vs. compensatory, justified by egregiousness
- [ ] Expert list: Norman Spencer (opinion letter Mar 21, 2025), vocational/economic, mental-health, cardiology

```
cat skills/apex-legal-strategy/references/damages-calculator.md
```

---

### Step 6 — Discovery Strategy
**Request:** "Sequence interrogatories, document requests, and depositions for post-answer / pre-discovery posture."
**Canonical file:** `skills/apex-legal-strategy/references/discovery-strategy.md`
**Action:** Read it. Priority: lock contradictions (AF 6/8, Ahmed role) → Title VI funding jurisdiction → instigation chain before SOL.
**Verify:**
- [ ] 7 priority interrogatories to UHS group + 6 to Ahmed
- [ ] 12 document requests
- [ ] 7-deponent priority order (Ali #1, Ahmed #2, 30(b)(6) #3, Nadeem #4, Rehman #5, Chief Residents #6, HR/FMLA admin #7)
- [ ] Sequencing rationale: written discovery first → Ali before Ahmed → 30(b)(6) mid → funding jurisdiction early → instigation chain continuously

```
cat skills/apex-legal-strategy/references/discovery-strategy.md
```

---

### Step 7 — Evidence Inventory (REFRESHED)
**Request:** "Inventory all evidence in possession with type, status, and strategic use — no orphan claims."
**Canonical file:** `skills/apex-legal-strategy/references/evidence-inventory.md` — **refreshed in this re-run** to add the missing audio-recording admission and reconcile with the `legal-endeavors` exhibit set (Exhibits A–J).
**Action:** The refreshed inventory is written in the next step. See `Rahman_v_UHS_Evidence_Inventory_REFRESHED.md` (created in this re-run).
**Verify:**
- [ ] 15 items total, including the **audio admission** ("We knew it is false. We framed him")
- [ ] Each item has type, status, key use
- [ ] Authentication notes (hash-chain self-authenticating; witness videos need foundation)
- [ ] Gaps list points to discovery-strategy.md

```
cat Rahman_v_UHS_Evidence_Inventory_REFRESHED.md
```

---

### Step 8 — Policies & Regulations Violated
**Request:** "Map institutional obligations breached → claims → evidence needs."
**Canonical file:** `skills/apex-legal-strategy/references/policies-violated.md`
**Action:** Read it. 9 policies/regulations: Title VI, ACGME, FMLA, ADA, HIPAA, FERPA, UHS EO Policy, UHS Resident Handbook, NY HRL.
**Verify:**
- [ ] Full mapping table (policy / obligation / violation / evidence needed)
- [ ] Policy-to-claim map anchors each COA to specific policies
- [ ] Title VI funding jurisdiction flagged as must-establish-in-discovery (Interrogatory 6; Doc Request 12)
- [ ] Contract-claim note: hunt for mandatory "shall" handbook language

```
cat skills/apex-legal-strategy/references/policies-violated.md
```

---

### Step 9 — Litigation Playbook (3-Phase Strategy)
**Request:** "Produce the phased strategy: Shield (immediate) → Sword (offensive claims) → Lever (settlement)."
**Canonical file:** `legal-endeavors/references/litigation-playbook.md`
**Action:** Read it. Phase 2 ("Sword") must be filed **before September 2026** — add malicious prosecution against Sundas Rashid, defamation per se, IIED, ADA, Title VII (if EEOC charge filed), negligent supervision.
**Verify:**
- [ ] 3 phases present with active claims / claims to add / leverage points
- [ ] Discovery priorities table (URGENT: email archive, unredacted academic records)
- [ ] Motion practice roadmap (pre-discovery compel motions → discovery → post-discovery MSJ → in limine)
- [ ] Settlement framework: $4.2M floor / $5.5M mid / $6.8M ceiling + 5 non-monetary terms

```
cat legal-endeavors/references/litigation-playbook.md
```

---

### Step 10 — Deadline Tracker (RUN IT — 5 OVERDUE, SOL in 13 days)
**Request:** "Track every deadline and flag urgent ones."
**Canonical tool:** `legal-endeavors/scripts/deadline_tracker.py`
**Action:** **RUN IT NOW.** As of August 17, 2026, 5 deadlines are OVERDUE and the malicious-prosecution SOL (Aug 31, 2026) is 13 days out.
**Verify:**
- [ ] `python3 scripts/deadline_tracker.py` runs without error
- [ ] `python3 scripts/deadline_tracker.py --urgent` shows the SOL
- [ ] Confirm with counsel whether the overdue Rule 26(f), initial disclosures, EEOC verification, motion to compel, and amended-complaint items have actually been handled (status flags may be stale)

```
cd legal-endeavors && python3 scripts/deadline_tracker.py
cd legal-endeavors && python3 scripts/deadline_tracker.py --urgent
```

> **Most urgent action in the entire case:** file the malicious-prosecution claim before August 31, 2026. Missing it loses the claim permanently. Verify the exact acquittal docket date with Drazen to lock the SOL date.

---

### Step 11 — Rahman v. UHS Legal Risk Assessment (THE REAL ONE)
**Request:** "Produce the final comprehensive legal risk assessment for Rahman v. UHS."
**⚠️ Correction:** The existing `FINAL_DELIVERABLE_Rahman_Risk_Assessment.md` is mislabeled — it is the Minecore shipping/geopolitical report, not a legal assessment. The actual Rahman v. UHS legal risk assessment is created here, fresh: `Rahman_v_UHS_Legal_Risk_Assessment.md`.
**Action:** See the new file. Final-answer-first per the apex output protocol, with SCQH framing, risk-rated claims, deadline-gated additional claims, and the five immediate actions.
**Verify:**
- [ ] Final answer first (2–3 sentences)
- [ ] SCQH framing
- [ ] Risk rating (Low/Med/High) per claim with reasoning
- [ ] Deadline-gated additional claims (malicious prosecution SOL; EEOC/ADA exhaustion)
- [ ] Five immediate actions with deadlines

```
cat Rahman_v_UHS_Legal_Risk_Assessment.md
```

---

## Completion Checklist (run after all 11 steps)

- [ ] All 11 steps executed; each canonical file read/run
- [ ] 5 cross-track inconsistencies reconciled (see top of this file)
- [ ] Evidence inventory refreshed with the audio-recording admission
- [ ] Deadline tracker run; overdue + SOL items flagged to counsel
- [ ] Real legal risk assessment created (mislabeled Minecore file flagged, not deleted)
- [ ] No orphan factual claims — every figure traces to an evidence item

*End of re-run steps.*
