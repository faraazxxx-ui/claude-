---
name: legal-story-engine
description: >
  Reusable pipeline that turns raw legal source material (meeting transcripts, evidence files, filings,
  auto-generated notes) into a verified fact canon and then into a persuasive, honest legal narrative and
  argument package. Use for any legal case — this one or future ones — whenever the user wants to: analyze
  or rebuild meeting notes/transcripts with a lawyer, build a theory of the case or "legal story", construct
  a damages architecture or settlement anchor, map pressure points and obstacles with counters, or produce a
  victory-projection/win-probability assessment. Trigger on: legal story, theory of the case, case narrative,
  damages tiers, mediation framing, obstacle counters, transcript forensics, attorney meeting notes.
---

# Legal Story Engine — from raw record to argument

Facts are extracted before they are argued; every argument keeps a leash back to its evidence. The pipeline
has three layers, always in order:

## Layer 1 — Forensics (extraction)

Raw sources → verified canon JSON. Method in `references/extraction-pipeline.md`; block schema in
`references/annotation-schema.md`. Non-negotiables:
- Segment big sources at natural boundaries with overlap; merge dedupes the seams.
- Speaker/entity resolution with stated basis and confidence; garbles corrected only with evidence, else
  marked `[unresolved]`.
- Every fact carries a source anchor (timestamp, page, Bates number). No anchor → not a fact.
- An adversarial fidelity check samples anchors against the raw before the canon is trusted.

## Layer 2 — Strategy components (five workers, one canon)

Each consumes ONLY the canon + verified research; each output is independently red-teamable:

| Component | Output | Core rule |
|---|---|---|
| Damages architecture | Tiered model, machine + human versions | Every figure labeled DOCUMENTED / ESTIMABLE / ASSERTED; arithmetic shown; anchor/posture numbers carry a credibility caveat |
| Legal story | Narrative arc + per-audience variants (mediator, defense, jury) | Every beat anchored; the ask framed as accountability and repair, not punishment |
| Obstacle→counter matrix | One row per obstacle: bite, best counter, fallback, residual risk | Adverse authority is mandatory content — its absence fails review |
| Pressure-point map | Per-adversary leverage + which discovery instrument hits it | Volume pressure is legitimate only when every request is genuinely relevant |
| Victory projection | Per-claim probability bands + what moves them, version-stamped | Bands, never guarantees; refreshed on every ruling/production |

Legal research feeding these: court-database retrieval only (CourtListener etc.); a citation is usable when
it carries a database ID. Web-only findings ship flagged "unverified — confirm with counsel."
Story frameworks (SCQH-for-litigation, arcs, audience shifts): `references/story-frameworks.md`.

## Layer 3 — Assembly + guard

A synthesis pass builds the master document (answer-first, tables, both clocks loud), then a red-team pass
attacks it as opposing counsel (citations, arithmetic, overstated facts, missing adverse authority), then an
archetype/style guard compresses without touching facts. Deliver as interactive artifact or PDF.

## Standing rules

- Work product marking on everything; counsel of record reviews before anything external.
- The client's stated non-monetary objective is strategy, not decoration — cheap-for-defendant concessions
  (record repair, neutral references) are the highest-value mediation currency.
- Run the pipeline itself with the relay-loop skill (fresh agents, compact handoffs, bounded checker loops).
