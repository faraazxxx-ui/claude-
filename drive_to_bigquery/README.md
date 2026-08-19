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

69 checks, no credentials needed: exclusion correctness against real filenames,
family grouping, schema-drift reconciliation, type coercion, chunking
invariants, SQL well-formedness and INSERT arity, and that the notebook's
embedded modules still match the sources.

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
