# Phase R — Gap List (Field Test #1)

What is thin, missing, or unverified — and exactly what would close each gap. Ordered by how much it limits the deliverable.

| # | Gap | Why it matters | What closes it | Severity |
|---|-----|----------------|----------------|----------|
| G1 | **5 of ~50 conversations** | Pattern map is a 10% sample; generalization to "his thinking" is Low-confidence | Export/attach the remaining ~45 and re-run this pipeline | **High** |
| G2 | **No 2021–2025 material** | The 5-year arc the mission targets is absent; can't see how his approach *changed over time* | Add older exports; sort by real conversation date, not export date | **High** |
| G3 | **Topic monoculture (health-only)** | His legal thinking (Case 3:26-cv-00197, Apex Legal skill) and other domains are invisible; patterns may be health-specific | Add ≥10 non-health conversations (legal, finance, workflow) | **High** |
| G4 | **C3 deliverable truncated** | "What he was actually told about compression" is unknown; N19 flags this | Re-export C3 including the post-launch research output | Medium |
| G5 | **Content notes N15–N18 unverified** | Health claims are AI-synthesized; his own loop never fact-checks them (N07) | Verify PMIDs/trials via a citation tool before any reuse | Medium |
| G6 | **Raw CSVs absent** | Loop Score (N09) can't be recomputed; the 6.7-vs-5.7 discrepancy can't be resolved | Attach `physiological_cycles.csv`, `Visible_Data_Export…csv`, `sleeps.csv`, `ring_data_*` | Medium |
| G7 | **Self-reported profile unconfirmed (N13)** | Clinical context is declared, not verified; downstream notes inherit that uncertainty | Confirm against actual records before clinical use | Medium |
| G8 | **Exports show summaries, not full outputs** | C1's dashboards, several assistant turns exist only as pointers | Export full assistant message bodies, not collapsed thought-process | Low |
| G9 | **One person, one voice** | No way to separate "his patterns" from "this AI's habits" (e.g., the AI, not him, chose to build dashboards) | Not fixable by more data alone; keep the Process/Content split so AI-behavior notes stay labeled | Low |

## Thin-evidence flags carried from the notes

- **N02** (audiovisual = dashboard): Medium — inferred from acceptance, no explicit confirmation.
- **N06** (delegates decisions back): High within C3, but single-conversation — may not generalize (G3).
- **N07** (corrects form not facts): Medium — argument from absence in a small set.
- **N09** (Loop Score delta → IN node): Medium — plausible from both reports' own wording; unrecomputable (G6).

## What this gap list is *not* claiming

- Not claiming the missing 45 conversations resemble these 5.
- Not claiming the health content is wrong — only **unverified in this session**.
- Not claiming anything about conversations, dates, or topics not present. (Inventory rule.)

## The one thing to do first

**G1 + G3 together.** The cheapest high-value move is to add a *diverse* next batch — some non-health, some older — rather than more health conversations. That directly tests whether P1–P5 are "how he thinks" or just "how he does health analysis." Until then, treat the pattern map as **provisional and health-scoped.**
