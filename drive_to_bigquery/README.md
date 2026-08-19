# Drive → BigQuery

Loads an entire Google Drive into BigQuery, turning loose files into queryable
tables. Built for `pelagic-gist-505800-b9`.

## Status

**The code is written and tested. It has not been run against BigQuery, because
this environment has no Google credentials.** See [Credentials](#credentials).

What is verified:

- family grouping and table naming, against real filenames from the Drive
- schema-drift reconciliation across files in a family
- type coercion (string → INT64 / FLOAT64 / TIMESTAMP / DATE)
- Parquet serialization, which is the format BigQuery ingests
- `plan` end-to-end on a 100-file real inventory → 28 tables

What is not verified: the BigQuery calls themselves (`create_dataset`,
`create_table`, `load_table_from_file`) and Drive download, both of which need
credentials.

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
| `drive_raw.file_manifest` | One row per file in Drive — the census. Every file appears here whether it loaded or not, with `ingest_status` and `ingest_error`. Nothing is silently dropped. |
| `drive_tables.<family>` | One table per family of tabular files (CSV, TSV, XLSX, Sheets, JSON). |
| `drive_documents.documents` | Extracted text from PDF, Word, PowerPoint, txt, md, html. |

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

## Usage

```bash
pip install -r requirements.txt

# What would be built, and how many tables — no BigQuery writes.
python pipeline.py plan --project pelagic-gist-505800-b9

# Census only: write drive_raw.file_manifest and stop.
python pipeline.py inventory --project pelagic-gist-505800-b9

# Everything.
python pipeline.py load --project pelagic-gist-505800-b9
```

Scope to one folder with `--folder FOLDER_ID`. The `D:` folder in this Drive is
`1CcS-mQ_tjZ7NIXpRfajhWvognhwDzIQh`; the bulk of the health CSVs live under
`1pBl7xkcG0hFRo2mYgyFA1JhaouJpMI7e`.

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

The pipeline needs one identity with read on Drive and write on BigQuery:

```
https://www.googleapis.com/auth/drive.readonly
https://www.googleapis.com/auth/bigquery
```

It picks up whichever it finds:

1. `GOOGLE_APPLICATION_CREDENTIALS` pointing at a service-account JSON key
2. Application Default Credentials (`gcloud auth application-default login`)

For a service account, the Drive folders must be shared with the service
account's email — a service account sees nothing in a personal Drive by
default. That is the step most likely to produce a confusing empty inventory.

Do not paste a key into chat. Set it as a secret/environment variable in the
environment config.

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
