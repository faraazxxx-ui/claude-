---
name: life-intelligence-engine
description: >
  Deep document analysis and second-brain builder that ingests all personal files
  (PDFs, text, code, images, notes) from iCloud, Google Drive, or local sources,
  performs multi-layer parallel triage with tokenized node decomposition, RAG-enhanced
  chain-of-thought reasoning, and transformer-style sequential reassembly, then
  organizes everything into a structured second brain across Notion, Evernote,
  Obsidian, and Google NotebookLM. Use when the user wants to: analyze all their
  files, build a personal knowledge base, triage documents into life domains,
  create a second brain, perform deep document intelligence, or organize their
  digital life. Also use when user mentions document triage, life organization,
  knowledge graph, RAG analysis, or multi-database sync.
---

# Life Intelligence Engine

Ingest, decompose, analyze, and organize an entire personal file corpus into a
structured second brain. Every file is broken into atomic nodes, analyzed through
multi-layer parallel processing, and reassembled into a unified knowledge
architecture across four target databases.

## Architecture Overview

```
INPUT LAYER          PROCESSING LAYER              OUTPUT LAYER
─────────────       ──────────────────            ─────────────
iCloud files   ──►  1. Crawl & Catalog       ──►  Notion DB
Google Drive   ──►  2. Download & Extract    ──►  Evernote ENEX
Local files    ──►  3. Tokenize & Segment    ──►  Obsidian Vault
                    4. Parallel Deep Analysis      NotebookLM
                    5. Multi-Agent Triage
                    6. Knowledge Reassembly
                    7. Second Brain Map
                    8. Export & Report
```

## Proven Pipeline (Battle-Tested)

This pipeline was validated against a real corpus of 3,700 files (51.5 GB)
across 432 folders, extracting 1.29 million words from 1,004 downloaded files.

### Step 1: Crawl & Catalog Google Drive

Recursively crawl all Google Drive folders to build a complete file manifest.
Uses `gws` CLI with `--params` JSON syntax for the Drive API.

```python
# Key pattern for listing folder contents:
import subprocess, json

def list_folder(folder_id):
    params = json.dumps({
        "q": f"'{folder_id}' in parents and trashed = false",
        "fields": "files(id,name,mimeType,size,modifiedTime)",
        "pageSize": 1000
    })
    cmd = ["gws", "drive", "files", "list", "--params", params]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout).get("files", [])
```

**Critical gws syntax notes:**
- Use `--params` with JSON string, NOT `--query` or `--file-id`
- For downloads: `gws drive files get --params '{"fileId": "ID", "alt": "media"}' -o filename`
- For exports: `gws drive files export --params '{"fileId": "ID", "mimeType": "text/plain"}' -o filename`
- Output path (`-o`) must be relative to cwd, NOT absolute

Script: `scripts/catalog_files.py` — Recursive folder crawler
Output: `lie-output/gdrive_manifest.json`

### Step 2: Download & Extract

Download all text-extractable files. Skip audio/video (>50MB) for initial pass.
Export Google Docs as plain text, Google Sheets as CSV.

| File Type | Download Method | Extraction |
|-----------|----------------|------------|
| PDF | `files get` (alt: media) | PyMuPDF (fitz) |
| DOCX | `files get` (alt: media) | python-docx |
| Google Docs | `files export` (text/plain) | Direct text |
| Google Sheets | `files export` (text/csv) | Direct CSV |
| XLSX | `files get` (alt: media) | openpyxl |
| TXT/MD/CSV/HTML/JSON | `files get` (alt: media) | Direct read |
| RTF | `files get` (alt: media) | striprtf |
| Images | `files get` (alt: media) | Store for OCR |

Script: `scripts/extract_and_tokenize.py`
Output: `lie-output/extracted/all_extracted.json`, `lie-output/extracted/full_corpus.txt`

### Step 3: Segment for Parallel Analysis

Group extracted files into analysis segments by root folder and content type.
Each segment contains up to 50 files with combined text (truncated to 5000 chars
per file for analysis efficiency).

Output: `lie-output/segments/segment_NNN.json`, `lie-output/segments/segment_index.json`

### Step 4: Parallel Deep Analysis (Wide Research)

Use the `map` tool to analyze all segments in parallel through 6 layers:

1. **Content Inventory** — What each file is and its purpose
2. **Domain Classification** — Assign to life domains (see table below)
3. **Entity Extraction** — People, orgs, locations, dates, case refs, amounts
4. **Key Themes & Patterns** — Narratives, arguments, claims
5. **Importance & Urgency Triage** — Score 1-10, identify time-sensitive items
6. **Cross-Reference Signals** — Connections between documents

**Prompt template for parallel analysis:**
```
You are an expert intelligence analyst performing deep multi-layer analysis
on a segment of a personal document corpus. Read the segment file at:
<file>{{input}}</file>

Perform LAYER 1 through LAYER 6 analysis [full prompt in scripts/]
```

**Output schema per segment:**
- segment_id, primary_domain, secondary_domains
- importance_score (1-10)
- key_entities (semicolon-separated)
- key_themes, content_summary, file_inventory
- cross_references, critical_items
- triage_category (CRITICAL-LEGAL, CRITICAL-PERSONAL, HIGH-PRIORITY, STANDARD, REFERENCE, ARCHIVE)

### Step 5: Multi-Agent Triage Synthesis

Four synthesis agents process all parallel results:

1. **Entity Consolidator** — Deduplicates and merges entities across segments
2. **Domain Mapper** — Builds domain importance rankings and theme aggregation
3. **Cross-Reference Resolver** — Maps all inter-document connections
4. **Triage Classifier** — Final classification into priority categories

Script: `scripts/assemble_triage.py`
Output: `lie-output/triage/entity_registry.json`, `domain_map.json`, `cross_references.json`, `triage_classification.json`

### Step 6: Build Second Brain Map

Generate the complete knowledge architecture with:
- Vault/database structure recommendation
- Entity registry with relationship mapping
- Active case/matter tracker
- Cross-reference network
- NotebookLM notebook recommendations

Script: `scripts/generate_report.py`
Output: `lie-output/master_report.md`

### Step 7: Export to Target Databases

Export to all four targets:

- **Notion**: See `references/export-notion.md` — Uses Notion MCP server
- **Evernote**: See `references/export-evernote.md` — Generates ENEX files
- **Obsidian**: See `references/export-obsidian.md` — Creates vault with wikilinks
- **NotebookLM**: See `references/export-notebooklm.md` — Optimized Google Docs

Export scripts:
- `scripts/export_evernote.py`
- `scripts/export_obsidian.py`

## Life Domains

| Domain | Description | Example Content |
|--------|-------------|-----------------|
| Career & Work | Professional life, employment | Contracts, CVs, schedules |
| Finance & Legal | Legal cases, financial records | Court filings, demand letters |
| Health & Wellness | Medical, FMLA, conditions | Medical certs, health records |
| Learning & Education | Courses, research, credentials | ACGME docs, research papers |
| Personal & Identity | Identity, immigration, narrative | Visa docs, personal statements |
| Creative & Projects | Side projects, creative work | Business plans, writing |
| Relationships & Social | Family, contacts, communications | Text messages, testimonies |
| Home & Logistics | Housing, vehicles, daily ops | Lease docs, Tesla notices |
| Digital & Technical | Tech, AI tools, configurations | ChatGPT exports, code |
| Reference & Archive | Saved materials, templates | Policies, guides |

## Incremental Updates

When new files are added:
1. Re-run catalog with existing manifest to detect new files by hash comparison
2. Download and extract only new files
3. Create new segments and run parallel analysis
4. Merge new triage results with existing
5. Regenerate master report and export updates

## Key Dependencies

```bash
sudo pip3 install PyMuPDF python-docx openpyxl striprtf pandas
```

## iCloud Access

iCloud Drive shared links require Apple ID authentication. Two options:
1. User logs into iCloud in the browser (use `ask` with `take_over_browser`)
2. User copies iCloud files to Google Drive for processing

## Audio/Video Processing

For audio files, use the built-in transcription utility:
```bash
manus-speech-to-text /path/to/audio.mp3
```

For video analysis:
```bash
manus-analyze-video /path/to/video.mp4 "transcribe and summarize"
```
