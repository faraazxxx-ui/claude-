# Ingest — atomic notes → BigQuery `documents` rows

**Status:** the file is built and validated. **34 rows, zero orphan claims, validation PASS.** Everything up to the point where your Google Cloud credentials are required is done.

| Artefact | What it is |
|----------|-----------|
| `notes.jsonl` | 34 newline-delimited rows, one per atomic note. Loadable as-is. |
| `schema.json` | The guide's Stage 2.2 field list, verbatim, for `bq load`. |
| `build_jsonl.py` | Regenerates both from `01-ATOMIC-NOTES.md`. The markdown stays the single source of truth. |

## Field mapping

| `documents` field | Filled with | Rule |
|-------------------|-------------|------|
| `document_id` | `N01`–`N34` | Note ID. Stable, so re-loads upsert rather than duplicate. |
| `title` | The note title | Which is the claim itself — so a title-only search result is still a complete statement. |
| `content` | Body **+ Source + Confidence + Gap** | Provenance travels inside the retrieval unit. A retrieved chunk can never become an orphan claim. |
| `source_type` | `chat` | From the guide's enum. |
| `life_domain` | `health` · `finance` · `digital` · `reference` | Content notes from the Claude/health threads → `health`; from the ChatGPT/legal threads → `finance` (the guide's "Finance & Legal"); all process notes → `digital` ("Digital & Technical: ChatGPT exports, configs"); the reference-file note → `reference`. |
| `metadata.source` | `C1`–`C8` | Conversation IDs, ranges expanded. |
| `metadata.created_at` | Conversation date | C6–C8 are stamped in the export (2025-10-14). C1–C5 are only known from their export stamp, so those rows carry a `date:approx` tag rather than implying a date we cannot see. |
| `metadata.tags` | `type:` · `conf:` · `platform:` · `src:` · `pattern:` · `gap` · `date:approx` | Every filter in the artefact maps to a tag, so the same questions work in SQL. |
| `metadata.importance_score` | `9` · `7` · `5` | **Stated rule, not a judgment:** 9 if the note supports an act-now pattern (P6, P1, P3), else 7 for High confidence and 5 for Medium. Whole numbers — the schema requires FLOAT, but no decimal is invented. |
| `metadata.triage_category` | `behavioral-map` | Distinguishes these rows from clinical or legal source documents in the same table. |
| `embeddings` | `[]` | **Empty by design.** Embedding is the guide's Stage 4, a separate step with a separate cost. Loading now and embedding later is supported. |
| `chunk_index` | `0` | Each note is one chunk. Bodies are ≤150 words, well inside the guide's 512-token chunk size — no splitting needed. |
| `ingestion_timestamp` | Build time, UTC | Required, and the guide partitions on it by month. |

## Validation result

```
rows: 34
orphan claims: 0
life_domain: digital=24, finance=1, health=8, reference=1
validation: PASS
```

Checked per row: required fields present · `source_type` and `life_domain` inside the guide's enums · non-empty title and content · at least one source conversation (the reference-file note is the single documented exception) · one JSON object per line, no arrays.

## Retrieval, working now — without any credentials

The published artefact carries a search panel over these 34 notes with four preset questions, including *"Where does my approach stall?"* It returns the specific notes with their source conversations. That is the mission's done-when — *"I can ask where my approach stalls and get back the notes"* — satisfied locally, so the retrieval layer is proven before any cloud spend.

## What is blocked on you — the handoff

Four steps need your Google Cloud account. They are listed, not silently skipped.

| # | Step | Why it needs you |
|---|------|------------------|
| 1 | A GCS bucket and a BigQuery dataset | Project ownership and billing |
| 2 | IAM: `roles/bigquery.dataEditor` + `roles/storage.admin` | Your account's permissions |
| 3 | Upload and load — `gsutil cp` then `bq load --source_format=NEWLINE_DELIMITED_JSON` with `schema.json`, partitioned by month on `ingestion_timestamp`, clustered on `source_type, life_domain` per the guide | Authenticated CLI |
| 4 | Embeddings (Stage 4) | An embedding-model API key. Note the guide's warning: changing model later means re-embedding everything, so pick once. |

**The automated route, once credentials exist:** `build_jsonl.py` already regenerates the file from the markdown, so the whole chain becomes one scheduled job — regenerate, upload, load, embed only what changed. Nothing above needs to stay manual except the first-time account setup.

**Watson X remains deferred.** Nothing in the stack supports it.

## One judgment call worth your review

`life_domain` puts 24 of 34 notes in `digital`. That is correct by the guide's taxonomy — process notes are about AI tooling — but it means a domain-filtered query for "how I think" looks like a technical query rather than a personal one. If you would rather these sat under `personal`, it is a one-line change in the build script. Flagged rather than decided, because it changes how every future query behaves.
