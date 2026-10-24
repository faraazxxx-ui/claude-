# Life Intelligence Engine: Execution-Grade Prompt

Use this exact prompt for future runs of the Life Intelligence Engine when new files are added or a full corpus re-analysis is needed.

---

## Master Execution Prompt

```
Analyze this corpus recursively and build a lifelong second-brain system from it.

Process every accessible file, folder, document, scan, screenshot, image, PDF,
spreadsheet, note, code file, media transcript, and metadata source.

Your task is not to summarize loosely. Your task is to extract, classify,
cross-link, triage, and architect the corpus as a durable personal knowledge system.

Perform the work in these passes:

Pass 1 — Inventory
Build a full file inventory with stable IDs, original paths, filenames, types,
sizes, likely modality, and initial sensitivity flags.

Pass 2 — Extraction
Extract every recoverable layer of information: raw text, OCR text, document
structure, code semantics, image-visible text, image content, metadata, entities,
dates, topics, obligations, relationships, and references. Use Unstructured.io
for document parsing and Marker for PDF-to-Markdown conversion. Use
manus-speech-to-text for audio files and manus-analyze-video for video files.
DO NOT truncate content. Extract the FULL text of every file.

Pass 3 — Evidence Separation
Distinguish observed facts from inferred context. Mark uncertainty explicitly.
Do not hallucinate categories or personal narratives not supported by evidence.
For each file, create a structured record with:
  - source_evidence: direct quotes, metadata, dates, names
  - inferred_context: summaries, interpretations, classifications
  - uncertainty_flags: what could not be determined

Pass 4 — Semantic Clustering
Group files into meaningful clusters using shared entities, timelines,
institutions, topics, cases, projects, and life domains. Use sentence-transformers
for embedding and HDBSCAN for clustering. Do NOT segment by folder.

Pass 5 — Triage
For each file and cluster, assign: keep, keep-sensitive, review,
merge/duplicate, archive, or junk candidate. Explain why.

Pass 6 — Second-Brain Architecture
Organize the full corpus into the following 13-domain taxonomy:
  1. Identity & Personal Records
  2. Legal
  3. Finance
  4. Health
  5. Education
  6. Career & Work
  7. Projects & Operations
  8. Creative & Media
  9. Relationships & Correspondence
  10. Knowledge & Research
  11. Planning, Journals & Reflection
  12. Admin, Accounts & Devices
  13. Archive / Cold Storage

Pass 7 — Sub-Triage
Within each top-level category, create internal subcategories and recommended
folder/database structures.

Pass 8 — Cleanup + Risk Review
Detect duplicates, naming inconsistencies, missing metadata,
privacy-sensitive documents, legal/financial/health records, and items
needing manual review. Perform entity resolution using fuzzy matching
(thefuzz library) to deduplicate entity variations.

Pass 9 — Output Package
Produce the final output in this order:
  1. Executive summary (BLUF)
  2. Actionable intelligence briefing (deadlines first)
  3. Strategic narrative (chapters, not summaries)
  4. Master timeline
  5. Deduplicated entity registry with relationships
  6. Evidence-backed 13-domain taxonomy
  7. Second brain vault structure (Notion, Obsidian, Evernote, NotebookLM)
  8. Per-domain sub-triage
  9. Sensitivity and risk register
  10. Duplicates and cleanup candidates
  11. Unresolved ambiguities
  12. Future ingestion protocol
  13. Definition of done checklist
  14. Corpus statistics

For every file or cluster, output:
  - what it is
  - what evidence supports that
  - why it matters
  - suggested category
  - suggested subcategory
  - date or date range
  - entities involved
  - sensitivity level
  - action status
  - retrieval tags
  - related files/clusters

Optimize for zero-loss understanding, evidence-backed classification,
long-term retrieval, and graceful future expansion.
```

---

## Parallel Analysis Prompt Template (for map tool)

Use this prompt template when running the parallel deep analysis on each segment/cluster:

```
You are an expert intelligence analyst performing deep multi-layer analysis
on a segment of a personal document corpus. Read the segment file at:
<file>{{input}}</file>

Perform the following 6-layer analysis:

LAYER 1 — Content and Purpose
For each file in this segment, identify:
- What type of document is this?
- What was its original purpose?
- What is the key information it contains?

LAYER 2 — Structured Data Extraction
Extract all structured data:
- Dates and deadlines (with exact dates where possible)
- Financial figures and amounts
- Obligations and requirements
- Specific claims or allegations
- Case numbers, docket references, account numbers

LAYER 3 — Entity and Relationship Extraction
Identify all entities:
- People (full names, titles, roles)
- Organizations (full names, abbreviations)
- Locations (addresses, jurisdictions)
- Legal cases (case numbers, court names)
Map relationships between entities found in this segment.

LAYER 4 — Narrative and Themes
- What story does this collection of documents tell?
- What are the underlying arguments or recurring themes?
- What is the emotional tone or urgency level?

LAYER 5 — Urgency and Actionability
- Is there a required action? A deadline? A risk?
- Assign a priority score (1-10, where 10 = immediate action required)
- Classify: CRITICAL-LEGAL, CRITICAL-PERSONAL, HIGH-PRIORITY,
  STANDARD, REFERENCE, or ARCHIVE

LAYER 6 — Evidence vs. Inference
For your key findings, explicitly separate:
- EVIDENCE: Direct quotes, dates, names from the documents
- INFERENCE: Your interpretation or summary
- UNCERTAINTY: What you could not determine

Also identify:
- Cross-references to other documents or segments
- Sensitivity flags (PII, PHI, legal privilege, financial data)
- Suggested domain classification (from the 13-domain taxonomy)
- Suggested sub-category within that domain

Output your analysis as structured JSON.
```

---

## Anti-Hallucination Guards

When executing this pipeline, enforce these rules:

1. **Never invent dates.** If a date cannot be extracted from the document, mark it as "TBD" or "Unknown."
2. **Never merge entities without evidence.** Entity resolution must be based on contextual co-occurrence or explicit references, not assumptions.
3. **Never classify without justification.** Every domain assignment must cite at least one piece of evidence from the source document.
4. **Never truncate content.** If a file is too large for a single analysis pass, split it into chunks with overlap, not truncation.
5. **Always flag uncertainty.** If a classification or interpretation is uncertain, say so explicitly in the uncertainty_flags field.
