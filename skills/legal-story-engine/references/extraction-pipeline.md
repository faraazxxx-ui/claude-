# Extraction pipeline (Layer 1 method)

Proven on the Aug 2 2026 Drazen meeting (102K chars → 80-block canon, 32/32 fidelity samples passed).

1. **Deterministic prep (no model):** extract raw text; split auto-notes ("claims") from verbatim record
   ("evidence") — they are different epistemic classes; cut segments (~15-17K chars) at speaker/timestamp
   boundaries with one-block overlap; write segment files.
2. **Roster resolution (one agent):** participant list + sample segments → speaker roster with confidence +
   cues, and a garble glossary (candidate → correction → quoted basis). Auto-transcription lumps speakers —
   assume labels are wrong until shown right. Corrections below ~0.7 confidence stay tentative.
3. **Sectioned analysis (one agent per segment):** per block — corrected speakers, faithful summary, key
   verbatim quotes with significance, corrections applied with basis, closed-enum topic tags, one-line
   callout. Per segment — facts (with anchors + claim links), action items (with owners), damages mentions,
   open questions. Full JSON to disk; compact receipt back.
4. **Merge (one agent):** dedupe overlap seams keeping the richer twin; unify entities; global order;
   reconcile action-item counts against the auto-notes' claims and record discrepancies rather than forcing
   agreement.
5. **Fidelity check (adversarial):** sample ≥15 quotes/anchors against raw (fragment-tolerant matching —
   stitched quotes verify fragment-by-fragment); timestamps exist and are monotonic; item counts reconcile;
   attribution spot-checks; every correction has a basis. Bounded repair loop, then scripted main-loop gate
   re-checks independently (JSON parses, counts, anchors).

Failure modes seen in practice: ellipsis-stitched quotes failing naive grep (use fragment windows);
background cross-talk mis-attributed as substantive turns (flag, don't interpret); auto-notes undercounting
action items (16 real vs 12 claimed); trailing audio compressed into the last block.
