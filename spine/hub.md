# Hub — active task registry

Fixed for each task's duration. Sub-agents write down into goal/verify/progress; nothing edits from above mid-task.

| Task | Mode | Zone | State | Opened |
|---|---|---|---|---|
| financial-second-brain | slow-loop | Confidential (legal-tagged rows: Privileged) | awaiting statements + answers to 5 opening questions | 2026-08-27 |

## Zone rules in force
- Financial ledger, statements, email-derived receipts: **Confidential**. Stays in this repo / session workspace. No public RAG, no shared index, no public artifact sharing.
- Rows tagged `DUBAI-TRANSFER` or `SURVIVAL-EXPENSE` (litigation 3:26-cv-00197 exhibits-in-waiting): **Privileged**. Same handling as `apex-legal-strategy/references/`.
- Raw statement PDFs are NOT committed to git. Normalized/derived data only, and only if Dr. Rahman approves.

## Access map (verified 2026-08-27)
- Gmail reachable now: `faraazxxx@gmail.com` (live-verified via connector)
- NOT reachable: `dr.faraaz.rahman@gmail.com`, `drrahman@therahmanfoundation.com` — need per-account Gmail connectors authorized in claude.ai Settings → Connectors
- NOT reachable: `faraaz.rahman@icloud.com` — no iCloud Mail connector exists; use reportaproblem.apple.com purchase-history export + Settings → Apple ID → Subscriptions screenshots instead
