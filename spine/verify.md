# Verify — standing rubric (pass/fail per line; no scores, no decimals, no vibes)

Grader must be a separate pass from the builder. Any %/confidence/accuracy number without shown derivation → automatic fail on that line.

## Ledger integrity
- [ ] Every card's row sum reconciles to its printed statement total to the penny; mismatches halt the pipeline, never papered over.
- [ ] Zero invented merchants: every row cites source PDF filename + page.
- [ ] Refunds/credits netted once, never double-counted.
- [ ] Foreign-currency rows reported in USD with FX flag.
- [ ] Statement coverage map shows every month in window as present/missing; no silent gaps.

## Bleed roster
- [ ] Every confirmed cancel-list target matched to statement lines or explicitly marked "not found in window."
- [ ] Recurring detection ran across ALL in-scope cards (incl. Chase + Dad's card), not just AMEX.
- [ ] Duplicate subscriptions across cards surfaced.
- [ ] Every opaque Apple row: Gmail-confirmed binding OR labeled hypothesis with verification path.

## Legal overlays
- [ ] Dubai-transfer rows: complete for every uploaded bank statement in window; each cites source.
- [ ] Survival-expense tally exists in BOTH forms: all-in and categorized (fixed survival / discretionary / litigation-direct).
- [ ] Privileged rows never appear in any shareable/public output.

## Output contract
- [ ] Answer first; structure shown; ≤120 words prose around artifacts; confidence as High/Medium/Low + one line; one named next step.
