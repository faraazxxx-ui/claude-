# Session export — read this first

A complete, machine-checkable record of one Claude Code session: what he typed, what I did, what it cost, and what cannot be recovered. Built for a third party to analyse the session and re-create it.

**Everything here is derived from the raw transcript by `build_export.py`. Nothing is summarised, inferred, or filled in.**

## The one thing to know before you analyse this

**My reasoning text is not in this export, because it is not in the transcript.**

All 60 reasoning blocks were written to disk **signature-only** — the plaintext was never stored. This export can prove, for every reasoning block: that it happened, where in the conversation, how long the signature was, and roughly how many tokens it consumed. It cannot tell you what the reasoning said, and no amount of re-processing the transcript will change that.

Anyone reconstructing "the model's thinking" from this data is reconstructing its *shape and cost*, not its content. Treat any claim to the contrary as false.

## Files

| File | What it is |
|---|---|
| `session.json` | The full export. Every table, every row, every surviving character. Start here. |
| `session.sql` | The same data as portable DDL + INSERTs. SQLite dialect. |
| `session.db` | The SQL already loaded — query it immediately, no setup. |
| `session.md` | Human-readable transcript in order, with reasoning blocks marked as unrecoverable. |
| `MANIFEST.json` | Counts, totals, per-file SHA-256, and the stated limits. |
| `VERIFY.txt` | The mechanical grade. |
| `build_export.py` | Regenerates all of the above from the transcript. |

## Schema

Seven tables. `turns` → `blocks` is the spine; everything else hangs off it.

```
session ──┐
          ├── turns ──┬── blocks ──── tool_calls (via tool_use_id)
          │           └── usage
          ├── exchanges          one authored message + everything it caused
          └── artifacts          files the session produced, with checksums
```

A **block** is one content unit: `text`, `thinking`, `tool_use`, `tool_result`, or `plain`.
A **turn** is one logical message. The CLI writes one block per record, so records sharing a message id are grouped back into a single turn — without that grouping, token usage is counted once per block instead of once per response, which inflates every derived figure. This export does the grouping; check `turn_index` in the builder if you want to confirm it.
An **exchange** is one thing he typed plus every assistant turn, tool call and reply it produced, up to the next thing he typed. This is the unit of "his thinking vs mine."

Four views answer the obvious questions without writing SQL:

| View | Answers |
|---|---|
| `v_his_vs_mine` | What did each of his messages cost, and how much of it did he see? |
| `v_hidden_reasoning` | Where did reasoning happen, and how much? |
| `v_tool_profile` | Which tools, how often, how many errors, how much output? |
| `v_zone_map` | Where does the sensitive material sit? |

```sql
-- The finding this export exists to show.
SELECT exchange_no, ask_chars, hidden_tokens_est, reply_chars, shown_fraction
FROM v_his_vs_mine ORDER BY hidden_tokens_per_ask_token DESC;
```

## Derivations — check these before trusting any number

Two figures are estimates. Both are named as estimates everywhere they appear, and both show their working, so you can reject them and recompute.

**`hidden_tokens_est`** = `output_tokens` − (`visible_chars` ÷ 4)
`output_tokens` is exact and billed; it covers reasoning + reply text + tool arguments. `visible_chars` is the exact character count of everything actually emitted. The ÷ 4 is the standard English chars-per-token approximation — **it is not a measurement**, and it is the only soft term in the calculation. If you have a real tokeniser, substitute it and the figure improves.

**`shown_fraction`** = visible tokens ÷ (visible + hidden) tokens. Inherits the same approximation.

Everything else — character counts, block counts, tool counts, timestamps, checksums — is exact.

## Privacy zones

Every block carries a zone, a reason, and the term that triggered it, so each tag is auditable rather than asserted.

| Zone | Blocks | Why |
|---|---|---|
| Confidential | 24 | Litigation and medical material — his own affidavits, damages, clinical history |
| Private work | 320 | Session-internal working material |

**Ceiling: Confidential.** Rules are deliberately over-inclusive: a false Confidential costs nothing, a false Public cannot be undone. `ZONE_RULES` in the builder is the full rule list — read it, don't guess at it.

The Confidential blocks contain his own legal filings and medical history. Redistribute accordingly.

## Re-creating this session

1. **Read `CLAUDE.md` at the repo root.** The operating rules the session ran under. Without it the behaviour looks arbitrary.
2. **Replay `exchanges` in order.** The `ask` column is what he actually typed, verbatim. Thirteen messages produced the entire session.
3. **Compare against `artifacts`.** Thirteen files with SHA-256 checksums — the deliverables. If a re-run produces different files, the checksums say so immediately.
4. **Expect the reasoning to differ.** You have the inputs and the outputs, not the reasoning between them. A faithful re-creation reproduces the artifacts, not the thought process.

## Known limits

- Reasoning plaintext is absent from the transcript. Not redacted by this export — never written.
- `hidden_tokens_est` depends on a chars-per-token approximation. See above.
- Tool results are truncated by the harness before reaching the transcript, so `result_chars` measures what came back to the model, not what the tool produced.
- The pre-compaction portion of the session survives only as a summary. Exchanges 1–4 therefore show input with no assistant activity attached: the work happened, the records did not survive compaction. That absence is real and is not a parsing failure.
- Two models appear (`claude-opus-4-8`, `claude-opus-5`) because the model was switched mid-session.

## Verification status

`VERIFY.txt` carries a mechanical grade: the SQL is loaded into a fresh database and every table is reconciled against the JSON by row count. It currently reads **PASS**.

That grade covers fidelity — the data survived the round trip. It says nothing about whether the interpretation is right. By contract, the thing that built this cannot be the thing that grades it, so the interpretive check needs fresh eyes.
