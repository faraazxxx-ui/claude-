# Drive → BigQuery

Loads an entire Google Drive into BigQuery, turning loose files into queryable
tables. Built for `pelagic-gist-505800-b9`.

## Run it in Colab (recommended)

Open **`Drive_to_BigQuery.ipynb`** in [Google Colab](https://colab.research.google.com/)
and run the cells top to bottom.

This is the path of least resistance because Colab already has what a load like
this needs and an agent sandbox does not:

- `drive.mount()` makes all 1000+ files ordinary local paths — no API
  pagination, no per-file request, no download quota
- `auth.authenticate_user()` authenticates BigQuery **as you** — no service
  account, no JSON key, no folder sharing, nothing to paste
- the notebook carries its own copy of the pipeline, so there is no clone step

Nothing is written to BigQuery until step 5, and step 4 prints the full table
plan first.

The notebook is generated from the modules in this directory. After editing any
of them, re-run:

```bash
python build_notebook.py
```

A test asserts the embedded copies stay byte-identical to the sources, so the
notebook cannot silently drift.

## Status

**Tested, but never yet run against a live BigQuery project** — this repo's
development environment has no Google credentials.

Verified by direct execution:

- family grouping and table naming, against real filenames from the Drive
- schema-drift reconciliation across files in a family
- type coercion (string → INT64 / FLOAT64 / TIMESTAMP / DATE), and the guard
  that stops free text becoming a bogus 1970 date
- Parquet serialization, the format BigQuery ingests
- `plan` on a 100-file real inventory → 28 tables
- `load --dry-run` end to end against a mounted-Drive fixture, including native
  Google file stubs, hidden files, and mount bookkeeping directories
- health exclusion against real filenames, with deliberate trap cases
- chunking invariants, and every generated SQL statement's structure
- the notebook's embedded modules extract byte-identically and run

Run `python test_pipeline.py` for all of it (69 checks).

Not verified: anything that requires a live project — the BigQuery load calls,
Drive API download, and the whole Vertex embedding path
(`ML.GENERATE_EMBEDDING`, `CREATE VECTOR INDEX`, `VECTOR_SEARCH`). The SQL is
checked for structure, not accepted by a server. Colab is where it first
executes; expect to iterate on the Vertex connection step, which is the most
environment-dependent part.

## The problem it solves

A Google Takeout / Fitbit export is thousands of files that are really a few
dozen tables sharded by date:

```
heart_rate_2026-03-23.csv   1.5 MiB
heart_rate_2026-03-24.csv   2.2 MiB
heart_rate_2026-04-05.csv   1.4 MiB
...
```

Loading these one-table-per-file gives you 1000+ single-day tables, which is
unusable. This groups them by stem into one `heart_rate` table with a
`_src_date` column, so a query spans the whole history.

Measured on the first 100 CSVs in the Drive: **100 files → 28 tables.**

## Layout

| Dataset | Contents |
|---|---|
| `drive_raw.file_manifest` | One row per file in Drive — the census. Every file appears here whether it loaded, failed, or was excluded, with `ingest_status` and `ingest_error`. Nothing is silently dropped. |
| `drive_tables.<family>` | One table per family of tabular files (CSV, TSV, XLSX, Sheets, JSON). |
| `drive_documents.documents` | Extracted text from PDF, Word, PowerPoint, txt, md, html. |
| `drive_documents.document_chunks` | Those documents split into embedding-sized passages. |
| `drive_vectors.embeddings` | One vector table over documents, table rows **and** filenames, plus a `search()` table function. |
| `drive_graph` | `cross_links` (chunk↔chunk edges), `entity_mentions`, `entities` — the corpus crossed against itself. |
| `drive_insights` | Seven views over that, plus an `ask()` function. |

Media and unparseable binaries are recorded in the manifest as
`metadata_only` — searchable by name, path, and size, without their bytes.

### Provenance

Every row in `drive_tables` carries where it came from:

| Column | Meaning |
|---|---|
| `_src_file_id` | Drive file id |
| `_src_file_name` | original filename |
| `_src_date` | DATE parsed from the filename shard |
| `_src_sheet` | worksheet name, for multi-sheet workbooks |
| `_ingested_at` | load timestamp |

## Usage (CLI)

The notebook shells out to this, and it runs anywhere — Cloud Shell, a laptop, a
VM.

```bash
pip install -r requirements.txt

# What would be built, and how many tables — no BigQuery writes.
python pipeline.py plan --project pelagic-gist-505800-b9

# Census only: write drive_raw.file_manifest and stop.
python pipeline.py inventory --project pelagic-gist-505800-b9

# Everything.
python pipeline.py load --project pelagic-gist-505800-b9
```

### Two source modes

**Mounted Drive** — pass `--local-root`. Reads from the filesystem, so it needs
no Drive credentials and makes no API calls. Use this in Colab, or with Drive for
Desktop:

```bash
python pipeline.py load --project PROJECT --local-root /content/drive/MyDrive
```

**Drive API** — the default. Pass `--folder FOLDER_ID` to scope the walk. The
`D:` folder in this Drive is `1CcS-mQ_tjZ7NIXpRfajhWvognhwDzIQh`; the bulk of the
health CSVs live under `1pBl7xkcG0hFRo2mYgyFA1JhaouJpMI7e`.

Both modes produce identical records, so everything downstream behaves the same.
Mounted mode is markedly cheaper on a Drive with thousands of files.

## Scoping the load

`--skip-health` excludes wearable telemetry: the per-day Fitbit-style exports
(`heart_rate_*`, `body_temperature_*`, `micro_motion_*`, `sedentary_period_*`,
steps, calories, SpO2 and the rest). Millions of rows carrying almost no
information each, and nothing worth embedding.

It matches on both folder (`Fitbit`, `Google Fit`, `Apple Health`) and family
name, anchored so it does not over-reach. Verified against the real Drive: all
19 telemetry families excluded, all 9 documents and spreadsheets kept —
including the two traps, a PDF named `heart rate lecture notes.pdf` and a
clinical note under `Medical Notes`.

**`--skip-health` is about telemetry, not about medicine.** Clinical notes,
medical PDFs and anything under `Medical Notes` are documents; they are kept and
vectored. To drop those too:

```bash
python pipeline.py load --project PROJECT --local-root ROOT \
    --skip-health --exclude-path 'Medical Notes'
```

`--exclude-path` and `--exclude-family` take arbitrary regexes. Excluded files
are still written to the manifest with `ingest_status = 'excluded'` and the
reason, so the census stays a complete picture of the Drive even when the load
is deliberately partial.

## Vectors

```bash
python pipeline.py vectorize --project PROJECT \
    --vectorize-tables pgy_1 pgy_2 pgy_3
```

Or `--vectorize` on a `load` to do both in one pass.

Embeddings are generated **inside** BigQuery by `ML.GENERATE_EMBEDDING` against a
remote Vertex AI model. The text never leaves BigQuery, and there is no
client-side embedding loop to babysit or pay egress on.

Three kinds of thing get embedded, into one table on purpose — a document
passage, a spreadsheet row and a photo's filename are all just text with
provenance, and one index over all of them means one query searches everything:

| `source_kind` | What it is |
|---|---|
| `document_chunk` | A ~2000-char passage of a document, with 200 chars of overlap. One vector per whole document would average away the passage you were looking for. |
| `file_metadata` | Name, folder, type and date of every image, video and binary. A photo has no extractable text, but *"that scan from the hospital"* still has to be findable. |
| `table_row` | A row of a table named in `--vectorize-tables`, rendered as JSON so column names travel with the values. |

Row-level vectors are opt-in per table because telemetry rows are meaningless as
text and would swamp the index.

```sql
SELECT * FROM `pelagic-gist-505800-b9.drive_vectors.search`(
  'academic probation appeal deadline', 10
);
```

### One-time Vertex setup

`ML.GENERATE_EMBEDDING` needs a CLOUD_RESOURCE connection whose service account
holds `roles/aiplatform.user`. The notebook does this in step 6; `vectorize`
creates the connection itself when `bq` is on PATH, and logs the exact grant
command when it cannot. The IAM grant takes a moment to propagate — if embedding
fails with a permission error, wait and re-run.

Embedding is resumable by construction: text is queued in
`drive_vectors.embed_queue`, drained in batches, and rows are dequeued only once
they land in the vector table. A row whose embedding failed stays queued. If a
batch drains nothing, the run stops with an error rather than looping forever.

Two knobs worth knowing:

- `--embedding-model` defaults to `text-embedding-005`. `gemini-embedding-001` is
  newer and stronger but returns 3072 dimensions, making a much larger index.
- BigQuery only *uses* a vector index above ~5000 rows; below that it brute-force
  scans, returning the same results more slowly. The pipeline skips index
  creation below that threshold and says so rather than failing.

## Tests

```bash
python test_pipeline.py
```

215 checks, no credentials needed: exclusion correctness against real filenames,
family grouping, schema-drift reconciliation, type coercion, chunking
invariants, SQL well-formedness (balanced literals via a real quote-aware
scanner, INSERT arity, no unrendered placeholders), and that the notebook's
embedded modules still match the sources.

## Insights with no setup at all

**Run this first.** `quickinsights` is plain SQL over the manifest and extracted
text — no embeddings, no Vertex connection, no model. Seconds to run, cents to
bill, nothing that can be misconfigured.

```bash
python pipeline.py quickinsights --project PROJECT
```

| View | Answers |
|---|---|
| `duplicates` | Which files exist as many copies, and how much space that wastes. |
| `census` | What is in here, by kind and format, with date ranges. |
| `storage` | Where the bytes are per folder, and what fraction is redundant. |
| `name_clusters` | Near-duplicates hashing misses — `report.pdf` vs `report (1).pdf`, version chains. |
| `file_timeline` | Corpus activity by month and folder. |
| `doc_terms` | Rare-term index over document text. |
| `term_bridges` | Documents crossed by shared rare terms — no vectors needed. |
| `distinctive_terms` | What each document is about, by rarest frequent terms. |

`term_bridges` deserves attention: it crosses documents using shared *rare*
terms scored by inverse document frequency, so a pair sharing one very rare term
(a case number, an unusual surname) outranks a pair sharing several common ones.
Terms in more than 20% of documents are dropped as boilerplate. Less subtle than
embeddings — it cannot spot a paraphrase — but for records work shared
*identifiers* are usually what matter, and it costs nothing.

## Deduplication

Measured on the target Drive: **31 distinct spreadsheets exist as 100 files.**
`PGY-3.xlsx` appears nine times; a 240 MB textbook PDF twice. Roughly 3x
duplication.

`load` deduplicates by content hash before parsing. Two reasons, the second
mattering more than the first:

1. Embedding cost is paid per copy — 3x the bill for no extra information.
2. Every duplicate pair sits at cosine distance ~0, so without dedup
   `file_bridges` and `indirect_relations` would rank identical-file matches
   above every genuine connection. The expensive layer would produce confident
   noise.

Hashing is cheap because two files of different sizes cannot be identical, so
only size-colliding files are ever read. Files above 64 MiB are hashed from a
head+tail sample plus size rather than read whole.

Nothing is lost: every copy stays in the manifest as `duplicate` with a pointer
to its canonical copy, so "where are all the copies of this" stays answerable.
The canonical copy is the shallowest path, so it tends to be the sensibly-placed
one rather than a backup buried in a nested tree. `--no-dedup` disables it.

## Crossing, and keeping it live

Semantic search only answers what you thought to ask. These stages make the
corpus surface connections nobody queried for.

```bash
python pipeline.py crosslink --project PROJECT   # pass 1: chunk <-> chunk edges
python pipeline.py entities  --project PROJECT   # pass 2: entities through edges
python pipeline.py insights  --project PROJECT --insight-feed
python pipeline.py activate  --project PROJECT   # all three + schedule commands
```

**Pass 1 — crossing.** The embedding table is searched against itself and
nearest neighbours *in different files* become edges in
`drive_graph.cross_links`. Same-file neighbours are dropped (a document being
locally coherent tells you nothing), pairs are deduplicated to one unordered
edge, and anything past a cosine distance of 0.35 is discarded as noise.

**Pass 2 — crossing the crossings.** Gemini extracts entities per chunk into
`entity_mentions`, which resolve into `entities` by a casefolded normal form, so
"Dr. Rahman" and "dr rahman" are one entity. Those entities are then pushed
*through* the pass-1 edges.

### The views

| View | What it answers |
|---|---|
| `file_bridges` | Which two parts of the Drive meet, and whether the link crosses a folder boundary. |
| `indirect_relations` | Entity pairs that never share a passage but sit at either end of a link between files. This relationship exists in no single document — only in the geometry between them. |
| `entity_timeline` | Every dated appearance of an entity, from any source, with where the date came from (`in_text` / `filename` / `file_mtime`). |
| `entity_cooccurrence` | Entities appearing in the same passage — the direct crossing. |
| `entity_gaps` | Entities in your documents but absent from every spreadsheet, or the reverse. A gap or a finding. |
| `recent_activity` | What changed lately, by day and kind. |
| `pipeline_health` | Per-stage watermarks, with `stale` set past 48 hours. |

Plus two functions: `drive_vectors.search(query, k)` for passages, and
`drive_insights.ask(question, k)` for a cited answer — retrieval-augmented, and
instructed to say when the corpus does not contain the answer.

`insight_feed` optionally has Gemini narrate the strongest bridges. It is told to
be blunt and to label most matches `COINCIDENTAL`, so `looks_meaningful = true`
means something.

### Active, not static

Everything downstream of the vector table is pure SQL, so BigQuery refreshes it
on a timer with no machine of yours involved. `activate` prints the
`bq query --schedule` commands to register.

Ingest is the exception — it needs Drive access. Re-run the notebook after
adding files, or put `load` on Cloud Run behind Cloud Scheduler.

Each stage writes a watermark to `drive_graph.pipeline_state`, and
`pipeline_health` flags anything that has not run in 48 hours. That is the
difference between a live system and one that quietly stopped.

### Cost and correctness warnings

- Pass 1 is a self-join over the whole vector table. Cost scales with the square
  of the corpus. `--neighbours` (default 8) and `--max-link-distance` bound it.
- Entity extraction calls Gemini once per chunk. It is resumable and skips
  chunks already done, but the first run over a large corpus is the expensive
  one. `--extract-batch` sets the batch size.
- `extract_entities_sql` and `insight_feed_sql` are the only two statements using
  BigQuery's generative SQL surface, which moves faster than the rest. They are
  deliberately isolated so a drifted signature is a one-place fix.

Useful flags:

| Flag | Effect |
|---|---|
| `--dry-run` | log every BigQuery operation, execute none |
| `--from-cache` | reuse `drive_inventory.json` instead of re-walking Drive |
| `--replace` | truncate tables instead of appending |
| `--no-resume` | reload files already marked loaded |
| `--strict` | exit non-zero if any file failed |

### Re-running is safe

`load` reads back the file ids already marked `loaded` in the manifest and skips
them, so an interrupted run resumes where it stopped rather than duplicating
rows. Use `--no-resume` to override.

## Credentials

In Colab, step 3 handles this and there is nothing to configure.

Elsewhere the pipeline needs one identity with write on BigQuery, plus read on
Drive unless you are using `--local-root`:

```
https://www.googleapis.com/auth/bigquery
https://www.googleapis.com/auth/drive.readonly
```

It picks up whichever it finds:

1. `GOOGLE_APPLICATION_CREDENTIALS` pointing at a service-account JSON key
2. Application Default Credentials (`gcloud auth application-default login`)

Two things worth knowing before choosing a service account:

- The Drive folders must be shared with the service account's email. A service
  account sees nothing in a personal Drive by default, and the symptom is an
  empty inventory rather than an error.
- `--local-root` sidesteps Drive auth entirely, needing only BigQuery. Combining
  Drive for Desktop with a BigQuery-only service account is the least-privilege
  option.

Never paste a key into a chat transcript. Set it as an environment secret.

## Design notes

**Everything is read as string, then coerced after merging.** Per-file type
inference is what breaks these loads: one day's file has all-integer values and
the next has a decimal, so file 1 defines an INT64 column and file 2 fails
against it. Reading as string and inferring once on the merged frame avoids it.

**Columns are unioned, not intersected.** A file missing a column gets NULL for
it rather than having its other fields dropped.

**Date coercion is guarded.** A text column is only parsed as a date when >90%
of a sample actually looks like `YYYY-MM-DD`, so free text such as
`"2 pills daily"` is not mangled into a 1970 timestamp.

**Large files are recorded, not parsed.** Anything over `MAX_PARSE_BYTES`
(512 MiB) lands in the manifest with a reason, so one large video cannot stall
a run across thousands of small files.

## Known limitations

- Trailing-number filenames are treated as distinct tables, not shards:
  `video transcript.xlsx` and `video transcript 2.xlsx` produce two tables.
  This is deliberate — `PGY-1.xlsx` / `PGY-2.xlsx` / `PGY-3.xlsx` are genuinely
  different data and must not be merged. Merge after the fact in SQL if a given
  pair really is one table.
- Text extraction is not OCR. A scanned PDF yields a row with empty `content`
  and `extraction_method = 'pypdf'`; add an OCR pass if those matter.
- `.xls` needs `xlrd`, which no longer supports some very old workbooks.
- Native Google files (Sheets, Docs, Slides) are not real files on a mount —
  Drive represents them as small JSON stubs holding an id and no data. The
  pipeline recovers the id from the stub and exports through the Drive API, so
  in `--local-root` mode these are the one file type that still needs Drive
  credentials. Without them they are recorded as `failed` with a clear reason
  and everything else loads. Uploaded `.xlsx` files are real files and are
  unaffected.
