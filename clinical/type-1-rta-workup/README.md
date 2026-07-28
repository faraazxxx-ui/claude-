# Type 1 (Distal) RTA — Clinical Workup Package

Clinical decision-support deliverables for a patient presenting with one month of hematuria, flank pain radiating to the back, small nephrolithiasis, a treated pan-sensitive *Klebsiella* UTI, serum bicarbonate 18 mmol/L, anion gap 8–10, and urine pH 6.5–7.0.

**Provisional diagnosis: complete distal (Type 1) renal tubular acidosis.**

## Contents

| File | Purpose | Audience |
|---|---|---|
| [`01-CLINICAL-ANALYSIS.md`](01-CLINICAL-ANALYSIS.md) | Full diagnostic reasoning — RTA subtype discrimination, diagnostic criteria, urine pH interpretation, ketonuria differential and its effect on the urine anion gap, ranked unifying hypotheses for the hematuria, *Klebsiella*/urease analysis, dietary associations, NAGMA symptomatology, and a gap list | Physician |
| [`02-OUTPATIENT-ORDER-SET.md`](02-OUTPATIENT-ORDER-SET.md) | Checkbox order set — acid–base confirmation, autoimmune panel (tiered), 24-hour urine stone panel, imaging, hematuria pathway, empiric management, referrals | Physician / order entry |
| [`03-NEPHROLOGY-REFERRAL-NOTE.md`](03-NEPHROLOGY-REFERRAL-NOTE.md) | Formal referral letter template with bracketed identifier fields | Nephrology |
| [`04-PATIENT-HANDOUT.md`](04-PATIENT-HANDOUT.md) | Plain-language patient education, markdown source | Patient |
| [`patient-handout.html`](patient-handout.html) | The same handout as a printable single-sheet page (open and print; print styles target one side of US Letter) | Patient |

## Three things that drive the whole workup

1. **The bicarbonate of 18 is not the discriminator.** It is compatible with Type 1, Type 2, and Type 4 RTA. The diagnosis rests on the **urine pH of 6.5–7.0 in the presence of acidemia** — an intact distal nephron should acidify below 5.3–5.5 at that bicarbonate.
2. **The urine anion gap is invalid in this patient.** Her ketoanions are unmeasured urinary anions that make the UAG falsely positive and counterfeit the impaired-ammoniagenesis signature of distal RTA. Use the **urine osmolal gap** instead.
3. **The *Klebsiella* is more plausibly a consequence than a cause.** Urease alkalinizes urine but cannot produce a systemic metabolic acidosis, and urease-driven pH typically exceeds 7.5. It still has to be excluded formally with a sterile test-of-cure culture at the time the pH is re-measured.

## Highest-yield outstanding items

- **Serum potassium** — separates Type 1 from Type 4, and hypokalemic paralysis is the one emergency in this picture
- **Venous blood gas** — a low bicarbonate with a normal gap may be compensation for chronic respiratory alkalosis rather than an acidosis at all
- **Stone composition analysis** — apatite confirms dRTA, struvite reframes the case around the infection. Free if she strains.
- **Medication reconciliation** — topiramate, acetazolamide and zonisamide produce a fully reversible phenocopy

## Two ambiguities in the source dictation, deliberately not silently resolved

| Item | Issue | Why it matters |
|---|---|---|
| Stone size recorded as **"0.2 mm"** | Below CT spatial resolution (~0.5–1 mm) — almost certainly **2 mm / 0.2 cm** | Record accuracy |
| **"All obstructive"** vs **non-obstructive** | Dictation is ambiguous | **Materially different management.** An obstructing stone with infection is a urologic emergency requiring same-day decompression. Everything in the order set assumes non-obstructing. |

Also unspecified: whether the hematuria is **gross (visible)** or **microscopic**. Gross hematuria in an adult warrants full evaluation — cystoscopy plus CT urography — regardless of risk category; microscopic hematuria is triaged through the 2025 AUA/SUFU risk stratification.

## Scope

These are decision-support documents for a licensed physician. They support clinical judgment; they do not substitute for it, or for the nephrology and urology evaluations they recommend.

**All files are de-identified by design** — no name, date of birth, or medical record number appears anywhere in this directory. Identifier fields are bracketed placeholders to be populated in the EMR.
