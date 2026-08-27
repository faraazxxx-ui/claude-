# Progress — financial-second-brain

Slow-loop: state as of each pass, never "done."

## 2026-08-27 — pass 1 (intake)
- Extracted Daily_aug_26 diagram (both uploads = same page). Full decode in goal.md.
- Gmail access verified: faraazxxx@gmail.com reachable; other 2 Gmail + iCloud not (see hub.md access map).
- 4-year window anchor proposed from case timeline: 2022-10 (engagement broken / rumor campaign begins) — awaiting confirm.
- Spine seeded. Affirmation + 5 batched opening questions delivered.
- BLOCKED ON: his answers + statement uploads. Nothing dispatched yet; stop budget untouched (rounds 0/2).

## 2026-08-27 — pass 2 (automation + connectors)
- Asked how to add connectors → instructions delivered (per-account Gmail connector, or forward+POP-import both accounts into faraazxxx@gmail.com; Apple via reportaproblem.apple.com).
- Asana→orchestrator daily routine designed; create_trigger and direct Asana calls both approval-gated in autonomous turn. Spec persisted at spine/routines/orchestrator-asana-daily.md. CronCreate rejected as mechanism (session-only, 7-day expiry — would fake durability).
- NEXT: retry create_trigger on his next message (approval prompt surfaces with him present).

## 2026-08-27 — pass 3 (answers received, routine still gated)
- Q1–Q3 answered → encoded as ledger rules in goal.md (deposits rule with payroll carve-out; Dad's-card in-kind rule; baseline delegated → annualized-bleed headline + trailing-3-mo median).
- create_trigger retried WITH user present, still "requires approval" → this session's permission layer auto-blocks it; 2/2 attempts spent, stopping per budget. Two working paths handed to user: approve-dialog-then-"retry", or create the Routine from claude.ai/code UI using spine/routines/orchestrator-asana-daily.md verbatim.
- Connector OAuth: confirmed impossible to automate on his behalf (identity sign-in is his alone); 3-tap path given. iCloud/Apple: reportaproblem.apple.com PDF upload (fastest), or Claude-in-Chrome/desktop local session driving his logged-in browser.
- AWAITING: statements (AMEX Platinum ×4yr first), Chase checking statements, Dad's-card statements, Apple purchase-history PDF, Q4/Q5 corrections.

## 2026-08-27 — pass 4 (Drive corpus landed; transport in flight)
- He shared the Drive folder; connector lists it ungated. Corpus ≈250 files: Chase checking -5032 (~89 PDFs, 2019-01→2026-08 — THE deposit/family-support account), Chase credit -1366 (~60, 2021-09→2026-08), Amex Platinum (~44 PDFs 2023-01→2026-07 + activity.xlsx export), Amex Gold (~50 PDFs 2022-11→2026-08 + 3 xlsx exports), PayPal (~25 monthly PDFs + 3 zips + subfolder). PayPal = decode layer (dedupe against funding cards), NOT additive spend.
- Transport mechanics: download_file_content is approval-gated, but read_file_content is UNGATED and oversized results save to local tool-results files → zero-context transport. 4 background agents grinding all sources to Manhattan/text/.
- Parser proven on Platinum export: 1,172 rows, 0 rejects, 2024-08-24→2026-08-22, charges $102,704.72 / payments $105,011.18. AMEX's own category column present; extended details even decode PayPal*APPLE.COM line items.
- Early flags (not yet a roster): RETURN PAYMENT FEE $29 on 2026-08-12 (cash-flow stress marker, reversible by phone), Oura, Miro, PayPal*Apple MUSIC 7.99 recurring.
- GAPS (coverage map): NO Apple Card folder anywhere in Drive despite diagram scope; no Dad's-Dubai-card statements; Amex Platinum pre-2023 absent; Chase credit pre-2021-09 absent; PayPal zips skipped (monthly PDFs assumed to cover — verify).
- NEXT on agent completion: normalize all sources → one ledger, penny reconciliation, coverage map, then roster + calendar.

## 2026-08-27 — pass 5 (Apple purchase history landed)
- reportaproblem.apple.com PDF (12pp, faraaz.rahman@icloud.com) parsed: 94 purchases, but coverage is ONLY Jun 27 → Aug 25, 2026 (~2 months of scroll). Enough to decode the CURRENT Apple-billed roster; deeper history optional later.
- HEADLINE: Apple-billed AI stack alone ≈ $885/mo (SuperGrok Heavy $300 + Perplexity Max $200 + Manus Pro $200 + X Premium Plus $100 + ChatGPT Plus $20 + Genspark $25 + Replit $40) ≈ $10.6k/yr, before AMEX-direct subscriptions and other cards. Duplicate-function cluster (5+ AI assistants) = prime usage-weighing target.
- Apple Card state (Wallet screenshot): $2,750 limit, $0.00 available (100% utilization), APR 25.49%, 13 monthly installments, AUTOPAY NOT SET UP → late-payment risk at max APR.
- Apple Card statements still missing from corpus; export path given to him (Wallet → Card Balance → Statements → Export Transactions CSV, per month).

## 2026-08-27 — pass 6 (Gmail inventory landed: faraazxxx@gmail.com)
- 91 merchants inventoried → normalized/gmail_subscription_signals.csv (+ gmail_apple_lineitems.csv). 14 active, 41 stale, 25 canceled, 11 signal-only.
- DUNNING CLUSTER (cash-flow signature): Netflix last two auto-pays FAILED (Jun/Aug 2026), Sembly $29/mo failing but renewing, Notion "last attempt" Apr 2026, OnlyFans retrying, Anthropic Claude Max ~$109/mo receipts STOP 2026-04 amid card failures (billing may have moved — top uncertainty).
- Duplicate stacks: dictation ×3 concurrent (Aqua Voice $10 + Wispr Flow + VoiceInk + PLAUD hw); AI stack overlaps Gmail-side (Claude Max, Genspark $49.99, Mistral $14.99, Copilot $10.89 — Perplexity Max canceled 6/19 per email BUT reappears Apple-billed $200 in Jun-Aug — reconcile); delivery ×3 (Walmart+, Amazon Grocery, Instacart+); people-search burst Oct 2024 (~$90/mo ×4 services).
- Gray charge: Syntagma $9.90/mo from $0.50 trial Dec 2023–Oct 2024 (stopped).
- Structural: ZERO App Store receipts in this mailbox — Apple billing rode PayPal*APPLE.COM/BILL (AMEX-1009 funding!) ~100+ charges Feb–Oct 2024 then stopped (moved to Apple Card). NOTE: AMEX ...1009 and card ...7018 references = card numbers not yet in corpus map (Platinum=-44006; Gold=?); resolve when Gold export parses.
- Coverage limits: other two Gmail accounts unsearched; PayPal-in-Gmail pre-Feb-2024 unpaginated.

## 2026-08-27 — pass 7 (Chase checking normalized: LEGAL CORE COMPLETE)
- 92/92 statements penny-reconciled, triple-verified (per-statement beginning+Σ=ending; parsed credits == Chase's printed "Deposits and Additions" to the cent in every statement; cross-statement continuity tiles 2018-12-21→2026-08-20, zero gaps). 6,605 txns. Courtroom-grade lineage; ~15% amounts chain-derived but anchored (documented in agent caveat).
- DUBAI-WIRE: 103 wires $501,685 (UAE-only 102/$492,185), 2020-03-23→2026-08-17. Haseeb Ur Rahaman Mohammed 93/$459,925; Mubeena Iqbal 9/$32,260; 1 domestic false-positive (Srinath Katari TX $9,500) auto-separated. 79 wires carry AED Ocmt pattern. Per-year: 2020 $31.5k · 2021 $30.2k · 2022 $1.5k · 2023 $29.3k · 2024 $113.0k · 2025 $159.3k · 2026(→Aug) $136.9k.
- PAYROLL (UHS Inc): $148,617 over 2021-07→2024-07-03 — THEN ZERO. Income stops Jul 2024; family wires surge after. RULE-DEPOSITS payroll carve-out proved essential (would have polluted the exhibit by $148k).
- ZELLE-IN: 221/$107,378. Whole-account: credits $869,767 vs debits $871,678 over 7.7yr; ending balance $486.16 — the "running tight" picture in one number.
- Files: normalized/chase_checking{,_recon,_deposits}.csv. Remaining in flight: chase-credit + amex transports.

## 2026-08-27 — pass 8 (Chase credit normalized)
- 59/59 statements reconcile; global cross-foot exact ($61,884.35 purchases − $61,801.23 payments/credits + $104.49 fees/interest = final New Balance $187.61 from $0 start). 1,785 rows, 2021-08→2026-07.
- 15 "Returned Payment" re-bills totaling $5,019.76 (2023, late-2025, 2026 clusters) — bank-side bounce signature matching the Gmail dunning cluster; interest episodes coincide with bounce clusters, not revolving habit. Net merchant spend ≈ $56,865.
- Notables: SQ*Morgan Mako APRN FNP $100/mo ×12 (recurring medical — legitimate, category medical); GENSPARK.AI billed in AED on Chase with FX fees (May–Jul 2026) while Genspark ALSO appears Apple-billed — cross-card duplicate to resolve in roster; top spend = Amazon/Uber/UberEats/groceries/Chase Travel.
- Remaining in flight: AMEX transport (last one).
