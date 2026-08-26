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

# Life Intelligence Engine (v2.0 - Rebuilt)

This skill ingests, decomposes, analyzes, and organizes an entire personal file corpus into a structured, queryable, and extensible second brain. It uses a forensic, 9-pass architecture to extract every layer of meaning, distinguish evidence from inference, and build a durable knowledge system that improves over time.

## Required 9-Pass Architecture

The engine operates on a sophisticated 9-pass pipeline, ensuring deep, structured, and reliable analysis. This architecture is designed for high-fidelity extraction and robust, long-term knowledge management.

```
INPUT LAYER          PROCESSING LAYER                             OUTPUT LAYER
─────────────       ───────────────────────────────────           ─────────────
Google Drive   ──►  1. Inventory & Manifest Generation       ──►  Notion DB
Local files    ──►  2. Full-Content Extraction & OCR         ──►  Evernote ENEX
(iCloud, etc.) ──►  3. Evidence-Inference Separation         ──►  Obsidian Vault
               ──►  4. Semantic Clustering & Node Creation     ──►  NotebookLM
               ──►  5. Multi-Layer Parallel Analysis
               ──►  6. Second-Brain Domain Triage
               ──►  7. Per-Domain Sub-Triage
               ──►  8. Cleanup, Risk Review & Entity Resolution
               ──►  9. Structured Output Package Generation
```

---

## Pass 1: Inventory & Manifest Generation

This pass recursively crawls all specified data sources (starting with Google Drive) to build a complete file manifest. This manifest assigns a stable, unique ID to every file, which is crucial for tracking, incremental updates, and relationship mapping.

**Tooling:** The `gws` (Google Workspace) CLI is used for its robust and direct API access.

**Critical `gws` Syntax Notes (Preserve These):**
*   Always use the `--params` flag with a JSON string for complex queries. Do not use `--query` or `--file-id` directly for lists.
*   **List Folder Contents:**
    ```bash
    gws drive files list --params 
    gws drive files list --params '{"q": "\'FOLDER_ID\' in parents and trashed = false", "fields": "files(id,name,mimeType,size,modifiedTime,md5Checksum)", "pageSize": 1000}'
    ```
*   **Download Files:**
    ```bash
    gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' -o "path/to/filename"
    ```
*   **Export Google Workspace Files:**
    ```bash
    gws drive files export --params '{"fileId": "FILE_ID", "mimeType": "text/plain"}' -o "path/to/filename.txt"
    ```
*   The output path (`-o`) must be a relative path from the current working directory, not an absolute path.

**Output:** A `manifest.json` file containing a list of all files, their metadata (ID, path, MIME type, size, hash), and a status field for tracking.

---

## Pass 2: Full-Content Extraction

This pass extracts the complete, un-truncated content from every file identified in the manifest. It replaces brittle, format-specific parsers with powerful, unified document processing tools. **The previous 5000-character truncation limit is eliminated.**

**Primary Tooling: Production-Grade Parsers**
Instead of bespoke scripts, we leverage industry-standard open-source tools to handle the complexity of modern file formats.

| Tool | GitHub URL | What it Replaces | Purpose |
|---|---|---|---|
| **Unstructured.io** | `https://github.com/Unstructured-IO/unstructured` | Custom `python-docx`, `PyMuPDF`, `openpyxl` scripts | A single, powerful library to partition and extract text, tables, and metadata from dozens of formats (PDF, DOCX, PPTX, EML, HTML, etc.). Handles complex layouts with ease. |
| **Marker** | `https://github.com/VikParuchuri/marker` | Cloud OCR services | State-of-the-art PDF-to-Markdown conversion. Outperforms most commercial OCRs, preserving formatting, tables, and headers. Essential for scanned documents and complex PDFs. |

**Extraction Workflow:**
1.  **Prioritize Marker for PDFs:** For any `application/pdf` file, first attempt conversion with Marker to get clean, structured Markdown.
2.  **Use Unstructured.io as the Universal Engine:** For all other supported formats (and as a fallback for Marker), use the `unstructured` library. It intelligently routes files to the correct parsing backend.
3.  **Handle Audio/Video:** For media files, use the built-in sandbox utilities for transcription:
    *   Audio: `manus-speech-to-text /path/to/audio.mp3`
    *   Video: `manus-analyze-video /path/to/video.mp4 "transcribe and summarize"`

**Installation:**
```bash
# Install Unstructured.io with all dependencies for local processing
sudo uv pip install --system "unstructured[all-docs]"

# Install Marker (requires PyTorch)
sudo uv pip install --system marker-pdf
```

**Output:** A directory (`/lie-output/extracted/`) containing one text file per source document, named with its stable ID from the manifest.

---

## Pass 3: Evidence-Inference Separation

This is a mandatory reasoning pass that occurs *before* analysis. For each extracted document, the agent must explicitly distinguish between **direct evidence** (quoted text, file metadata) and **inferred context** (summaries, interpretations, classifications). This prevents hallucinations and ensures all claims are traceable.

**Workflow:**
1.  For each extracted text file, create a corresponding `_analysis.json` file.
2.  The agent populates a `source_evidence` field with direct quotes and facts.
3.  The agent populates an `inferred_context` field with its own understanding and summary.
4.  All subsequent passes must reference these two distinct fields, maintaining a clear chain of provenance.

**Example Snippet (`<stable_id>_analysis.json`):**
```json
{
  "source_evidence": {
    "quotes": [
      "On November 21, 2023, the court ordered...",
      "Faraaz Rahman's FMLA leave was approved for the period of..."
    ],
    "metadata": {
      "file_name": "Motion_to_Dismiss.pdf",
      "modified_date": "2023-11-22T10:05:00Z"
    }
  },
  "inferred_context": {
    "summary": "This document is a legal motion related to the dismissal of a case involving Faraaz Rahman, likely connected to his employment and FMLA leave.",
    "uncertainty_flags": ["The exact outcome of the motion is not stated in this document."]
  }
}
```

---

## Pass 4: Semantic Clustering & Node Creation

This pass moves away from brittle, folder-based segmentation. Instead, it uses semantic analysis to group related documents and concepts, regardless of their original location. This creates a more intuitive and powerful knowledge graph.

**Tooling:**
*   **Sentence-Transformers:** For generating high-quality vector embeddings of text chunks.
*   **Clustering Algorithm:** (e.g., HDBSCAN or K-Means) for grouping vectors.

**Workflow:**
1.  **Chunking:** Break down the extracted text from each document into meaningful chunks (e.g., paragraphs or sections).
2.  **Embedding:** Use a pre-trained `sentence-transformers` model (like `all-MiniLM-L6-v2`) to convert each chunk into a vector embedding.
3.  **Clustering:** Apply a clustering algorithm to the embeddings. Documents that appear in the same clusters are semantically related.
4.  **Node Creation:** Each cluster becomes a 
‘node’ in the knowledge graph, representing a core concept, event, or theme.

**Installation:**
```bash
sudo uv pip install --system sentence-transformers scikit-learn
```

**Output:** An updated `manifest.json` and a new `semantic_nodes.json` file that maps file IDs to semantic cluster IDs.

---

## Pass 5: Multi-Layer Parallel Analysis

With the corpus now organized into semantic nodes, we perform a deep, 6-layer analysis on each node in parallel using the `map` tool. This is where the core intelligence extraction happens.

**Analysis Layers (Applied to each semantic node):**
1.  **Content & Purpose:** What is this collection of information? What was its original function?
2.  **Key Information:** Extract structured data: dates, deadlines, financial figures, obligations, and specific claims.
3.  **Entities & Relationships:** Identify all people, organizations, and locations. Use fuzzy matching to begin resolving variations.
4.  **Narrative & Themes:** What story does this node tell? What are the underlying arguments or recurring themes?
5.  **Urgency & Actionability:** Is there a required action? A deadline? A risk? Assign a priority score.
6.  **Connections & Questions:** How does this node relate to others? What remains unclear or requires manual review?

**Tooling for Entity Resolution:**
*   **thefuzz:** A library for fuzzy string matching. Essential for resolving entity variations like “Dr. Rahman” and “Faraaz Rahman”.

**Installation:**
```bash
sudo uv pip install --system thefuzz
```

**Output:** A set of analysis files, one for each semantic node, containing the structured output from the 6-layer analysis.

---

## Pass 6: Second-Brain Domain Triage

This pass assigns each semantic node to one of the 13 required life domains. This classification is based on the rich data from the parallel analysis, not just keywords.

**Required 13-Domain Taxonomy:**

| Domain | Description |
|---|---|
| 1. Identity & Personal Records | Passports, licenses, birth certificates, personal statements. |
| 2. Legal | Court cases, contracts, legal correspondence, immigration. |
| 3. Finance | Bank statements, taxes, investments, invoices, receipts. |
| 4. Health | Medical records, insurance, FMLA, disability documentation. |
| 5. Education | Transcripts, diplomas, certifications, academic research. |
| 6. Career & Work | Resumes, employment contracts, performance reviews, job descriptions. |
| 7. Projects & Operations | Business plans, project management docs, operational workflows. |
| 8. Creative & Media | Writing, designs, photos, videos, source materials. |
| 9. Relationships & Correspondence | Emails, letters, text messages, contact information. |
| 10. Knowledge & Research | Articles, notes, web clippings, reference materials. |
| 11. Planning, Journals & Reflection | Calendars, to-do lists, diaries, personal reflections. |
| 12. Admin, Accounts & Devices | Bills, account credentials, device manuals, software licenses. |
| 13. Archive / Cold Storage | Old, inactive files to be kept but not actively used. |

**Workflow:** A classification agent assigns a primary and, if necessary, a secondary domain to each semantic node, providing a justification based on the analysis data.

**Output:** The `semantic_nodes.json` file is updated with `primary_domain` and `secondary_domain` fields.

---

## Pass 7: Per-Domain Sub-Triage

Within each of the 13 domains, this pass creates logical subcategories. This adds a crucial layer of granularity for organization and retrieval.

**Workflow:**
*   For each domain, an agent analyzes all assigned nodes.
*   It identifies recurring themes or sub-types of documents.
*   It creates sub-categories and assigns each node to one, along with a file count and sensitivity level.

**Example (Legal Domain):**
*   Sub-category: `Case - People v. Rahman (24-15519)`
*   Sub-category: `Employment - UHS Dispute`
*   Sub-category: `Immigration - Visa Application`

**Output:** The `semantic_nodes.json` is further updated with a `sub_category` field.

---

## Pass 8: Cleanup, Risk Review & Entity Resolution

This is the final synthesis and quality control pass. It consolidates all analysis, resolves entities definitively, and flags risks.

**Key Activities:**
1.  **Entity Resolution (Deduplication):**
    *   **Tool:** `dedupe` - A powerful Python library for ML-based deduplication and entity resolution.
    *   **Process:** Gathers all extracted entities, trains a model to identify duplicates (e.g., “Faraaz Rahman”, “Mohammed F. Rahman”, “Dr. Rahman”), and merges them into a canonical entity registry.
2.  **Duplicate File Detection:** Identifies and flags files with identical content hashes (MD5, SHA256) for cleanup.
3.  **Naming Inconsistency Analysis:** Flags files with inconsistent or unhelpful names (e.g., `Scan_001.pdf`).
4.  **Sensitivity & Risk Register:** Creates a master list of all documents flagged as sensitive, noting the type of risk (PII, financial, legal privilege) and recommending handling procedures.
5.  **Unresolved Ambiguities:** Compiles a list of all questions and uncertainties flagged during analysis that require manual user review.

**Installation:**
```bash
sudo uv pip install --system dedupe
```

**Output:**
*   `entity_registry.json`: A clean, deduplicated list of all entities and their relationships.
*   `risk_register.md`: A human-readable report of all sensitive items and risks.
*   `cleanup_candidates.json`: A list of duplicate and poorly named files.
*   `manual_review.md`: A list of items requiring user attention.

---

## Pass 9: Structured Output Package Generation

This final pass assembles all the generated intelligence into the required master report and prepares the data for export to second-brain applications.

**Per-File/Cluster Output Schema (for export):**
For each file or semantic cluster, a structured data object is created with the following fields:

*   `title`: What it is.
*   `evidence_summary`: What evidence supports that.
*   `relevance`: Why it matters.
*   `suggested_category`: The assigned 13-domain category.
*   `suggested_subcategory`: The assigned sub-category.
*   `date_range`: Extracted date or date range.
*   `entities`: List of resolved entities involved.
*   `sensitivity_level`: (e.g., `Confidential`, `PII`, `Legal Privilege`).
*   `action_status`: (e.g., `Action Required`, `For Review`, `Archived`).
*   `retrieval_tags`: Keywords for search.
*   `related_nodes`: Links to other semantic nodes.

**Master Report:** A comprehensive Markdown document is generated, containing the key intelligence briefings, architectural maps, and risk registers.

**Export:** The structured data is then formatted for ingestion into Notion, Obsidian, Evernote, and Google NotebookLM, using their respective APIs or file formats.

---

## Incremental Ingestion Protocol

This architecture is designed to be a living system. New files are ingested without requiring a full rework of the existing knowledge base.

1.  **Detect New Files:** Re-run the **Inventory** pass. The manifest’s use of file hashes makes detecting new or changed files trivial.
2.  **Process New Files:** Subject only the new files to Passes 2-5 (Extraction, Evidence Separation, Clustering, Analysis).
3.  **Integrate & Update:**
    *   Merge new analysis results into the existing data.
    *   Re-run the **Triage** and **Sub-Triage** passes (6 & 7) to classify the new information within the existing structure.
    *   Re-run the **Cleanup & Resolution** pass (8) to update the entity registry and risk registers.
4.  **Regenerate Outputs:** Re-run the **Output Package** pass (9) to generate an updated master report and export files.

---

## Definition of Done

This checklist validates the successful completion of the Life Intelligence Engine task:

- [ ] **Inventory:** Every accessible file has been inventoried in the manifest.
- [ ] **Extraction:** Every recoverable layer of content (text, tables, OCR) has been extracted without truncation.
- [ ] **Classification:** Every file/node has a designated category and sub-category from the 13-domain taxonomy.
- [ ] **Entity Indexing:** Every important entity has been indexed, resolved, and deduplicated.
- [ ] **Sensitivity Flagging:** Every sensitive item (PII, legal, financial) has been flagged in the risk register.
- [ ] **Cleanup:** Duplicate files and junk have been identified for cleanup.
- [ ] **Taxonomy:** A stable, lifelong taxonomy (domains and sub-domains) has been established.
- [ ] **Extensibility:** The system is ready to ingest future uploads without requiring a full rebuild.
