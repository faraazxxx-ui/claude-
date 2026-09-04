# Phase R — Gap List (Field Test #1, Round 2)

What is thin, missing, or unverified — and exactly what closes each gap. Ordered by how much it limits the deliverable.

| # | Gap | Why it matters | What closes it | Severity |
|---|-----|----------------|----------------|----------|
| G1 | **8 of ~50 conversations** | A 16% sample. Better than Round 1's 10%; still indicative rather than representative | Export and attach the remaining ~42 | **High** *(narrowed)* |
| G10 | **His own messages absent from C6–C8** | Every behavioural claim from the three ChatGPT threads is one inference-step removed; P2 cannot be tested at all | Re-export those conversations with user turns included — the exporter dropped them | **High** *(new)* |
| G2 | **2021 – mid-2025 absent** | Corpus now spans Oct 2025 → Mar 2026 (~5 months). One longitudinal observation became possible (N30); four of five years are still missing | Add pre-2025 exports; sort by conversation date, not export date | **High** *(narrowed)* |
| G3 | **Domain coverage still narrow** | Legal/financial is now present, which was the Round 1 blocker. Two domains is enough to separate domain-specific from general; it is not enough to map his range | Add workflow, finance, clinical-practice and technical conversations | Medium *(was High)* |
| G11 | **Promised deliverables absent in 4 of 8** | C3, C6, C7, C8 all end with an artefact offered and missing. Truncation and genuine non-delivery are indistinguishable, so N28 cannot be confirmed | Re-export those four threads in full, or confirm from his files whether the documents exist | Medium *(new)* |
| G5 | **Content notes unverified** | The health claims (N15–N18) are AI-synthesised; the legal claims (N33) are his declared assertions, unadjudicated. His loop never fact-checks either (N07) | Verify health citations against a literature source; treat legal content as pleading, not fact | Medium |
| G6 | **Raw source data absent** | Loop Score cannot be recomputed, so the 6.7-vs-5.7 discrepancy (N09) stays unresolved. Legal exhibits are likewise absent | Attach the wearable CSVs; attach or index the legal exhibit bundle | Medium |
| G7 | **Self-reported profile and claims unconfirmed** | Clinical history (N13) and legal assertions (N33) are declared in-prompt, not verified. Downstream notes inherit that uncertainty | Confirm against records before any clinical or legal use | Medium |
| G4 | **C3 deliverable truncated** | What he was actually told about compression is unknown | Re-export C3 including the post-launch research output | Medium |
| G8 | **Exports show summaries, not full outputs** | C1's dashboards and several assistant turns exist only as pointers | Export full message bodies, not collapsed thought-process | Low |
| G12 | **R1 authorship unknown** | `examples.md` may be third-party skill content; treating it as his writing would create a false pattern | Confirm whether he wrote it or installed it | Low *(new)* |
| G9 | **Separating his patterns from the AI's** | Largely addressed: five of seven patterns replicate across two different platforms (N29). Residual risk — both are instruction-following assistants with similar training | A structurally different source: his handwritten notes, dictations, or a non-LLM tool | Low *(was the unfixable one)* |

## Thin-evidence flags carried from the notes

- **N24** (render-as-deliverable is one drive): High for the pattern, Medium for treating dashboard and PDF as the same impulse — that reading is inference.
- **N28** (initiative delivers, confirmation-seeking does not): Medium — n=4, and cause cannot be separated from effect without his turns (G10, G11).
- **N29** (patterns are his, not the model's): Medium — replication across two platforms is strong evidence, not proof.
- **N31** (why decimals are barred): Medium — the rationale is inferred; he has not stated it.
- **N07** (corrects form, not facts): Medium — argument from absence, still unchallenged in Round 2.
- **N09** (score delta pinned to one node): Medium and unrecomputable (G6).

## What this gap list is *not* claiming

- Not claiming the missing ~42 conversations resemble these 8.
- Not claiming the health content is wrong — only **unverified in this session**.
- Not claiming anything about the merits of his litigation. N33 records what his documents assert; it takes no position on whether the assertions are correct, and offers no legal opinion.
- Not claiming anything about conversations, dates or domains not present.

## The one thing to do first

**G10, then G1.** Re-exporting C6–C8 *with his messages* is cheap and upgrades three conversations from inference to direct evidence — it also makes P2 testable for the first time outside C1. After that, volume: the remaining ~42, prioritising anything older than October 2025, because the single most valuable new capability in Round 2 was seeing the same person five months apart (N30).
