# Export to Google NotebookLM

## Table of Contents
1. NotebookLM Source Requirements
2. Document Optimization Strategy
3. Export Workflow
4. Audio Overview Generation
5. Notebook Organization

## NotebookLM Source Requirements

Google NotebookLM accepts these source types:
- Google Docs (preferred — richest integration)
- Google Slides
- PDFs (uploaded)
- Web URLs
- Plain text (pasted)
- YouTube videos

**Optimal source size**: 5,000–50,000 words per document. NotebookLM handles
up to 500,000 words per notebook across all sources combined.

## Document Optimization Strategy

NotebookLM works best with well-structured, narrative documents rather than
raw data dumps. Prepare sources as **domain summary documents**:

For each domain, generate a single comprehensive Google Doc containing:

```
# [Domain Name] — Life Intelligence Summary

## Overview
[2-3 paragraph executive summary of this domain]

## Key Documents
[List of source files with one-line descriptions]

## Core Content
[Reassembled content from all clusters, organized by sub-topic]
[Use clear headings, paragraphs, and context]

## Key Entities
[People, organizations, concepts with brief descriptions]

## Cross-Domain Connections
[How this domain relates to others]

## Timeline
[Chronological events related to this domain]
```

**Critical**: NotebookLM's audio overview feature works best when content
reads naturally. Avoid bullet-point lists, raw data tables, and code blocks.
Convert technical content to narrative prose where possible.

## Export Workflow

```bash
python3 /home/ubuntu/skills/life-intelligence-engine/scripts/export_notebooklm.py \
  --assembled-dir /home/ubuntu/work/lie-output/assembled/ \
  --output-dir /home/ubuntu/work/lie-output/notebooklm-export/
```

The script generates one Markdown file per domain, optimized for NotebookLM
ingestion. Then upload to Google Drive:

```bash
# Upload domain summaries to Google Drive
for f in /home/ubuntu/work/lie-output/notebooklm-export/*.md; do
  gws docs create --title "LIE - $(basename $f .md)" --content "$f"
done
```

Alternatively, use rclone for bulk upload:

```bash
rclone copy /home/ubuntu/work/lie-output/notebooklm-export/ \
  manus_google_drive:/Life-Intelligence-Engine/NotebookLM-Sources/ \
  --config /home/ubuntu/.gdrive-rclone.ini
```

## Audio Overview Generation

After uploading sources to NotebookLM:

1. Create a new notebook at notebooklm.google.com
2. Add the Google Docs as sources (one per domain)
3. Use the "Audio Overview" feature to generate a podcast-style summary
4. Create separate notebooks for focused topics:
   - **Life Overview** — Add all domain summaries
   - **Career Deep Dive** — Add only Career & Work + related cross-refs
   - **Financial Review** — Add Finance & Legal + related
   - **Personal Growth** — Add Learning + Personal + Creative

NotebookLM audio overviews are excellent for hands-free review of your
knowledge base during commutes or exercise.

## Notebook Organization

Recommended NotebookLM notebook structure:

| Notebook | Sources | Purpose |
|----------|---------|--------|
| Life Master | All domain summaries | Complete overview |
| Career & Growth | Career, Learning, Creative | Professional development |
| Life Admin | Finance, Home, Digital | Practical management |
| Wellbeing | Health, Personal, Relationships | Personal life |
| Reference Library | Reference, Archive | Lookup and research |

Each notebook can generate its own audio overview, giving you different
"podcast episodes" for different aspects of your life.
