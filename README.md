# Legal Strategy System — Unified Document Hub

> **Owner:** Dr. Faraaz
> **Created:** 2026-02-17
> **Status:** Active — Awaiting Data Population
> **Destination:** `/Users/dr.faraaz/Library/Mobile Documents/com~apple~CloudDocs/Cleaned and Processed Documents/_second-brain`

---

## Directory Map

```
.
├── README.md                          ← You are here (master index)
├── legal-strategy/
│   ├── 00-case-overview.md            ← High-level case summary
│   ├── 01-legal-arguments.md          ← Core legal theories & arguments
│   ├── 02-opposing-counsel-analysis.md← Counter-arguments & weaknesses
│   └── 03-action-items.md             ← Next steps, deadlines, filings
├── financial-analysis/
│   ├── 00-financial-summary.md        ← Transaction overview & totals
│   ├── 01-transaction-ledger.md       ← Line-by-line transaction log
│   └── 02-source-of-funds.md         ← Fund sourcing & tracing
├── timeline/
│   ├── 00-master-chronology.md        ← Complete event timeline
│   └── 01-critical-dates.md           ← Key deadlines & statute dates
├── evidence/
│   ├── 00-evidence-index.md           ← Master evidence catalog
│   └── 01-exhibit-list.md             ← Court-ready exhibit list
├── scripts/
│   ├── export-pdf.sh                  ← Convert all .md → PDF
│   ├── sync-to-second-brain.sh        ← Sync to iCloud _second-brain
│   └── upload-checklist.md            ← Manual upload checklist (Drive, Notion, NotebookLM)
└── output/
    └── (generated PDFs go here)
```

---

## Quick Start

### 1. Pull This Repo to Your Mac
```bash
git clone <repo-url>
cd claude-
git checkout claude/legal-strategy-system-90qYb
```

### 2. Populate Your Data
Open each `.md` file and replace the `[PLACEHOLDER]` sections with your actual data.

### 3. Generate PDFs
```bash
chmod +x scripts/export-pdf.sh
./scripts/export-pdf.sh
```

### 4. Sync to Second Brain
```bash
chmod +x scripts/sync-to-second-brain.sh
./scripts/sync-to-second-brain.sh
```

### 5. Upload to External Services
Follow `scripts/upload-checklist.md` for Google Drive, Notion, and NotebookLM.

---

## Status Tracker

| Document | Status |
|---|---|
| Case Overview | Template Ready — Needs Data |
| Legal Arguments | Template Ready — Needs Data |
| Financial Summary | Template Ready — Needs Data |
| Transaction Ledger | Template Ready — Needs Data |
| Master Chronology | Template Ready — Needs Data |
| Evidence Index | Template Ready — Needs Data |
| PDF Export Script | Ready |
| Sync Script | Ready |
