# Optimized Prompt — Islamic Family Support Loan Contract Generator

Reusable, production-ready prompt. Paste into Claude Code to regenerate or adapt the Qard Hasan package (e.g., for a different lender, amount, or case).

---

```
Generate a dual-compliant (Shariah + New York law) family support loan contract package for Dr. Mohammed Faraaz Rahman, M.D. (Borrower) and his father (Lender), grounded in the Qur'anic command of Surah al-Baqarah 2:282 to reduce every debt to writing with witnesses and a fixed term.

STARTING STATE: Repo branch claude/islamic-contract-family-support-kwmrqp. Case context: Rahman v. UHSH, No. 3:26-cv-00197 (AJB/ML) (N.D.N.Y.), plaintiff Dr. Rahman; father has been wiring support since April 2024 (documented range: $84,747.92 minimum per case records to $223,800 per damages framework — do NOT hardcode; use certified-ledger fill-in).

TARGET STATE — create in legal-endeavors/islamic-contracts/:
1. Qard_Hasan_Family_Support_Agreement.md — the contract. MUST include: (a) classification of ALL transfers as qard (loan), never gift, unless contemporaneously designated hibah in writing; (b) Lender covenant: fixed Support Installment every 14 days on a named due date, 3-business-day grace, delay-notice duty, missed installments cumulate — installment pegged to the bi-weekly salary under Borrower's original employment contract (Reference Salary fill-in with both candidate readings and math shown); (c) Borrower covenant: unconditional repayment of principal only (no riba per 2:275), maturity 90 days after Final Resolution of the Civil Action, longstop date, repayment sourced first from net recovery but owed regardless of case outcome, hardship respite per 2:280; (d) hash-chained Ledger as the accurate inventory of every amount sent and spent, monthly reconciliation, conclusive-evidence clause; (e) 2:282 formalities: borrower-dictated writing, two witness blocks, no-harm clause; (f) NY governing law, severability, integration, dispute-resolution ladder.
2. Qard_Ledger_Template.csv — ledger columns matching existing SHA-256 chain-of-custody practice.
3. README.md — execution checklist, open fill-ins, and flags for Attorney Drazen review (discoverability, collateral-source/damages interaction, IRC §7872 imputed-interest note).
4. PROMPT_Islamic_Contract_Generator.md — this prompt, reusable.
5. A signable .docx of the contract.

FORBIDDEN: fabricating wire totals, father's legal name, or dates; interest or late fees payable to Lender; touching files outside legal-endeavors/islamic-contracts/. STOP CONDITIONS: commit, push with -u, open draft PR, then stop. Done when: all 5 files exist, contract passes both checklists (2:282 elements; NY contract elements), PR is open.
```

🎯 Target: Claude Code · 💡 Converts the verbal idea into a scoped agentic spec: gift-vs-loan classification as the load-bearing clause, unconditional repayment (required both for a valid qard and for damages recoverability), and locked fill-ins wherever the source records conflict.

> Note: This prompt is for an agentic tool with real system access. Review the scope locks, forbidden actions, and stop conditions before pasting. Confirm file paths, directories, and permissions match the actual project.
