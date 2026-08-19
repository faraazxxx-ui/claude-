#!/usr/bin/env python3
"""Load an entire Google Drive into BigQuery.

Three datasets, three jobs:

  drive_raw        file_manifest -- one row per file in Drive, loaded or not.
                   The census. Nothing is silently dropped; anything that fails
                   is recorded here with its error.
  drive_tables     one table per *family* of tabular files. Date-sharded exports
                   (heart_rate_2026-04-05.csv, heart_rate_2026-07-05.csv, ...)
                   collapse into one table with _src_date provenance.
  drive_documents  documents -- extracted text from PDFs, Word, slides, txt/md.

Usage
-----
    python pipeline.py inventory --project PROJECT [--folder FOLDER_ID]
    python pipeline.py plan      --project PROJECT [--folder FOLDER_ID]
    python pipeline.py load      --project PROJECT [--folder FOLDER_ID]

`inventory` writes only the manifest. `plan` prints the table layout without
touching BigQuery. `load` does everything and is safe to re-run: files already
marked loaded in the manifest are skipped.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import sys
import traceback
from pathlib import Path

import pandas as pd
from google.auth import default as google_auth_default
from google.oauth2 import service_account
from googleapiclient.discovery import build

sys.path.insert(0, str(Path(__file__).resolve().parent))

import bq  # noqa: E402
import drive as drive_mod  # noqa: E402
from classify import build_families, sanitize_table_name  # noqa: E402
from parse import extract_text, read_tabular, reconcile  # noqa: E402

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/bigquery",
]

RAW_DATASET = "drive_raw"
TABLES_DATASET = "drive_tables"
DOCS_DATASET = "drive_documents"

# Files bigger than this are recorded in the manifest but not parsed, so one
# 4 GB video cannot stall a run over thousands of small files.
MAX_PARSE_BYTES = 512 * 1024 * 1024

# Rows are accumulated per family and flushed in batches to bound memory.
FLUSH_ROWS = 400_000

log = logging.getLogger("drive2bq")


# --------------------------------------------------------------------- helpers


def credentials():
    """Service-account JSON if provided, otherwise Application Default Creds."""
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if key_path and Path(key_path).is_file():
        return service_account.Credentials.from_service_account_file(
            key_path, scopes=SCOPES
        )
    creds, _ = google_auth_default(scopes=SCOPES)
    return creds


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _is_stringish(series: pd.Series) -> bool:
    """True for object and for pandas' native string dtypes.

    pandas 2.2 gives ``object``, pandas 3 gives ``str``; checking only for
    ``object`` silently skips every column on newer pandas and leaves the whole
    table as strings.
    """
    return series.dtype == object or pd.api.types.is_string_dtype(series.dtype)


def coerce_types(frame: pd.DataFrame) -> pd.DataFrame:
    """Promote all-string columns to numeric/timestamp where unambiguous.

    Everything is read as string to keep a family's files schema-compatible;
    this puts the real types back once the whole family is merged, so the
    resulting tables are actually queryable with SUM/AVG and date filters.
    """
    for column in frame.columns:
        if column.startswith("_src_") or column == "_ingested_at":
            continue
        series = frame[column]
        if not _is_stringish(series):
            continue
        non_null = series.dropna()
        if non_null.empty:
            continue

        numeric = pd.to_numeric(non_null, errors="coerce")
        if numeric.notna().all():
            full = pd.to_numeric(series, errors="coerce")
            # Keep integers narrow when there is no fractional part.
            if (full.dropna() % 1 == 0).all():
                frame[column] = full.astype("Int64")
            else:
                frame[column] = full
            continue

        # Only try dates on values that look like them, so free text that
        # happens to start with a digit is not mangled into 1970.
        sample = non_null.astype(str).head(200)
        if sample.str.match(r"^\d{4}-\d{2}-\d{2}([ T]|$)").mean() > 0.9:
            parsed = pd.to_datetime(series, errors="coerce", format="mixed", utc=True)
            if parsed.notna().sum() >= non_null.shape[0] * 0.99:
                frame[column] = parsed

    # Provenance columns get real types too, so _src_date is filterable as a
    # DATE and _ingested_at as a TIMESTAMP rather than both landing as strings.
    if "_src_date" in frame.columns:
        frame["_src_date"] = pd.to_datetime(
            frame["_src_date"], errors="coerce", format="%Y-%m-%d"
        ).dt.date
    if "_ingested_at" in frame.columns:
        frame["_ingested_at"] = pd.to_datetime(
            frame["_ingested_at"], errors="coerce", utc=True
        )
    return frame


def add_provenance(frame: pd.DataFrame, record: dict, sheet: str) -> pd.DataFrame:
    frame = frame.copy()
    frame.insert(0, "_src_file_id", record["file_id"])
    frame.insert(1, "_src_file_name", record["name"])
    frame.insert(2, "_src_date", record.get("shard_date"))
    frame.insert(3, "_src_sheet", sheet or None)
    frame.insert(4, "_ingested_at", now())
    return frame


def manifest_row(record: dict, **overrides) -> dict:
    row = {
        "file_id": record["file_id"],
        "name": record["name"],
        "path": record["path"],
        "mime_type": record["mime_type"],
        "extension": record["extension"],
        "size_bytes": record["size_bytes"],
        "md5_checksum": record["md5_checksum"],
        "created_time": record["created_time"],
        "modified_time": record["modified_time"],
        "parent_id": record["parent_id"],
        "kind": record["kind"],
        "fmt": record["fmt"],
        "family_stem": record["family_stem"],
        "shard_date": record["shard_date"],
        "target_dataset": None,
        "target_table": None,
        "ingest_status": "pending",
        "ingest_error": None,
        "row_count": None,
        "ingested_at": now(),
    }
    row.update(overrides)
    return row


def enumerate_drive(args, drive_service=None) -> list[dict]:
    """Enumerate via a mounted path when given, otherwise via the Drive API."""
    if args.local_root:
        log.info("enumerating mounted Drive at %s ...", args.local_root)
        files = list(drive_mod.walk_local(args.local_root))
    else:
        log.info(
            "enumerating Drive%s ...", f" folder {args.folder}" if args.folder else " (all)"
        )
        files = list(drive_mod.walk(drive_service, root_id=args.folder))
    log.info("found %d files", len(files))
    return files


def fetch_bytes(record: dict, args, drive_service) -> tuple[bytes, str]:
    """Read one file's bytes in whichever mode is active."""
    if args.local_root:
        return drive_mod.read_local(record, service=drive_service)
    return drive_mod.download(drive_service, record["file_id"], record["mime_type"])


def needs_api(files: list[dict]) -> bool:
    """True when any file can only be read by exporting through the API."""
    return any(f.get("mime_type") in drive_mod.EXPORT_MIMES for f in files)


def make_drive_service(optional: bool = False):
    """Build a Drive client, tolerating absent credentials in local mode."""
    try:
        return build("drive", "v3", credentials=credentials(), cache_discovery=False)
    except Exception as exc:
        if not optional:
            raise
        log.warning("no Drive credentials (%s); native Google files will be skipped", exc)
        return None


def summarize(files: list[dict]) -> dict:
    by_kind: dict[str, int] = {}
    bytes_by_kind: dict[str, int] = {}
    for record in files:
        by_kind[record["kind"]] = by_kind.get(record["kind"], 0) + 1
        bytes_by_kind[record["kind"]] = bytes_by_kind.get(record["kind"], 0) + int(
            record["size_bytes"] or 0
        )
    return {"count": len(files), "by_kind": by_kind, "bytes_by_kind": bytes_by_kind}


# ------------------------------------------------------------------- commands


def cmd_inventory(args) -> int:
    drive_service = make_drive_service(optional=bool(args.local_root))
    files = enumerate_drive(args, drive_service)

    stats = summarize(files)
    families = build_families(files)
    print(json.dumps({**stats, "families": len(families)}, indent=2))

    loader = bq.Loader(args.project, args.location, dry_run=args.dry_run)
    loader.ensure_dataset(RAW_DATASET)
    loader.ensure_table(RAW_DATASET, bq.MANIFEST_TABLE, bq.MANIFEST_SCHEMA)
    rows = [manifest_row(r, ingest_status="inventoried") for r in files]
    loader.load_rows(rows, RAW_DATASET, bq.MANIFEST_TABLE, bq.MANIFEST_SCHEMA)
    log.info("manifest written: %d rows", len(rows))

    Path(args.out).write_text(json.dumps(files, indent=2))
    log.info("local inventory cached at %s", args.out)
    return 0


def cmd_plan(args) -> int:
    # Planning from a cached inventory needs no credentials at all, which makes
    # the table layout reviewable before any access is granted.
    if args.from_cache and Path(args.out).is_file():
        files = json.loads(Path(args.out).read_text())
        log.info("loaded %d files from cache %s", len(files), args.out)
    else:
        # A mounted walk needs no credentials at all; the API walk does.
        drive_service = make_drive_service(optional=bool(args.local_root))
        files = enumerate_drive(args, drive_service)
        Path(args.out).write_text(json.dumps(files, indent=2))

    stats = summarize(files)
    families = build_families(files)

    print(f"\nFiles: {stats['count']}")
    for kind, count in sorted(stats["by_kind"].items(), key=lambda kv: -kv[1]):
        mib = stats["bytes_by_kind"].get(kind, 0) / 1024 / 1024
        print(f"  {kind:<10} {count:>6}  ({mib:,.1f} MiB)")

    print(f"\n{TABLES_DATASET}: {len(families)} tables")
    for name, family in sorted(families.items(), key=lambda kv: -len(kv[1].files)):
        mib = family.total_bytes / 1024 / 1024
        print(f"  {name:<48} {len(family.files):>5} files  ({mib:,.1f} MiB)")

    docs = [f for f in files if f["kind"] == "document"]
    other = [f for f in files if f["kind"] in {"media", "other"}]
    print(f"\n{DOCS_DATASET}.documents: {len(docs)} files")
    print(f"{RAW_DATASET}.file_manifest: {stats['count']} files "
          f"({len(other)} recorded as metadata only)")
    return 0


def cmd_load(args) -> int:
    drive_service = make_drive_service(optional=bool(args.local_root))
    loader = bq.Loader(args.project, args.location, dry_run=args.dry_run)

    for dataset in (RAW_DATASET, TABLES_DATASET, DOCS_DATASET):
        loader.ensure_dataset(dataset)
    loader.ensure_table(RAW_DATASET, bq.MANIFEST_TABLE, bq.MANIFEST_SCHEMA)
    loader.ensure_table(DOCS_DATASET, bq.DOCUMENTS_TABLE, bq.DOCUMENTS_SCHEMA)

    if args.from_cache and Path(args.out).is_file():
        files = json.loads(Path(args.out).read_text())
        log.info("loaded %d files from cache %s", len(files), args.out)
    else:
        files = enumerate_drive(args, drive_service)
        Path(args.out).write_text(json.dumps(files, indent=2))

    if args.local_root and drive_service is None and needs_api(files):
        native = sum(1 for f in files if f.get("mime_type") in drive_mod.EXPORT_MIMES)
        log.warning(
            "%d native Google files (Sheets/Docs/Slides) cannot be read from the "
            "mount without credentials; they will be recorded as failed",
            native,
        )

    done = set() if args.no_resume else loader.already_ingested(RAW_DATASET)
    if done:
        log.info("resuming: %d files already loaded, skipping", len(done))

    families = build_families(files)
    manifest: list[dict] = []
    counters = {"loaded": 0, "skipped": 0, "failed": 0, "rows": 0}

    # ---- tabular families -> drive_tables ---------------------------------
    for table_name, family in sorted(families.items(), key=lambda kv: -len(kv[1].files)):
        pending = [f for f in family.files if f["file_id"] not in done]
        if not pending:
            continue
        log.info(
            "family %s: %d files (%d already loaded)",
            table_name,
            len(pending),
            len(family.files) - len(pending),
        )

        buffered: list[pd.DataFrame] = []
        buffered_rows = 0
        first_write = args.replace

        def flush(frames, replace):
            if not frames:
                return 0
            merged = coerce_types(reconcile(frames))
            disposition = "WRITE_TRUNCATE" if replace else "WRITE_APPEND"
            return loader.load_frame(merged, TABLES_DATASET, table_name, disposition)

        for record in pending:
            size = int(record["size_bytes"] or 0)
            if size > MAX_PARSE_BYTES:
                manifest.append(
                    manifest_row(
                        record,
                        ingest_status="skipped",
                        ingest_error=f"exceeds MAX_PARSE_BYTES ({size} bytes)",
                        target_dataset=TABLES_DATASET,
                        target_table=table_name,
                    )
                )
                counters["skipped"] += 1
                continue
            try:
                data, exported_fmt = fetch_bytes(record, args, drive_service)
                fmt = exported_fmt or record["fmt"]
                sheets = read_tabular(data, fmt, record["name"])
                rows_here = 0
                for sheet_name, frame in sheets:
                    if frame.empty:
                        continue
                    stamped = add_provenance(frame, record, sheet_name)
                    buffered.append(stamped)
                    buffered_rows += len(stamped)
                    rows_here += len(stamped)

                manifest.append(
                    manifest_row(
                        record,
                        ingest_status="loaded",
                        row_count=rows_here,
                        target_dataset=TABLES_DATASET,
                        target_table=table_name,
                    )
                )
                counters["loaded"] += 1
                counters["rows"] += rows_here
            except Exception as exc:  # keep going; record the failure
                log.warning("failed %s (%s): %s", record["name"], record["file_id"], exc)
                manifest.append(
                    manifest_row(
                        record,
                        ingest_status="failed",
                        ingest_error=f"{type(exc).__name__}: {exc}"[:1000],
                        target_dataset=TABLES_DATASET,
                        target_table=table_name,
                    )
                )
                counters["failed"] += 1

            if buffered_rows >= FLUSH_ROWS:
                flush(buffered, first_write)
                first_write = False
                buffered, buffered_rows = [], 0

        flush(buffered, first_write)

    # ---- documents -> drive_documents -------------------------------------
    doc_rows: list[dict] = []
    for record in files:
        if record["kind"] != "document" or record["file_id"] in done:
            continue
        size = int(record["size_bytes"] or 0)
        if size > MAX_PARSE_BYTES:
            manifest.append(
                manifest_row(record, ingest_status="skipped", ingest_error="too large")
            )
            counters["skipped"] += 1
            continue
        try:
            data, exported_fmt = fetch_bytes(record, args, drive_service)
            fmt = exported_fmt or record["fmt"]
            text, pages, method = extract_text(data, fmt)
            doc_rows.append(
                {
                    "file_id": record["file_id"],
                    "name": record["name"],
                    "path": record["path"],
                    "mime_type": record["mime_type"],
                    "fmt": fmt,
                    "size_bytes": record["size_bytes"],
                    "created_time": record["created_time"],
                    "modified_time": record["modified_time"],
                    "page_count": pages,
                    "char_count": len(text),
                    "extraction_method": method,
                    "content": text,
                    "ingested_at": now(),
                }
            )
            manifest.append(
                manifest_row(
                    record,
                    ingest_status="loaded",
                    row_count=1,
                    target_dataset=DOCS_DATASET,
                    target_table=bq.DOCUMENTS_TABLE,
                )
            )
            counters["loaded"] += 1
        except Exception as exc:
            log.warning("failed doc %s: %s", record["name"], exc)
            manifest.append(
                manifest_row(
                    record,
                    ingest_status="failed",
                    ingest_error=f"{type(exc).__name__}: {exc}"[:1000],
                )
            )
            counters["failed"] += 1

        if len(doc_rows) >= 500:
            loader.load_rows(doc_rows, DOCS_DATASET, bq.DOCUMENTS_TABLE, bq.DOCUMENTS_SCHEMA)
            doc_rows = []

    loader.load_rows(doc_rows, DOCS_DATASET, bq.DOCUMENTS_TABLE, bq.DOCUMENTS_SCHEMA)

    # ---- everything else: metadata only ------------------------------------
    for record in files:
        if record["kind"] in {"media", "other"} and record["file_id"] not in done:
            manifest.append(manifest_row(record, ingest_status="metadata_only"))

    loader.load_rows(manifest, RAW_DATASET, bq.MANIFEST_TABLE, bq.MANIFEST_SCHEMA)

    log.info(
        "done: %d loaded, %d skipped, %d failed, %d rows into %d tables",
        counters["loaded"],
        counters["skipped"],
        counters["failed"],
        counters["rows"],
        len(families),
    )
    print(json.dumps(counters, indent=2))
    return 1 if counters["failed"] and args.strict else 0


# ----------------------------------------------------------------------- main


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["inventory", "plan", "load"])
    parser.add_argument("--project", required=True, help="GCP project id")
    parser.add_argument("--folder", help="Drive folder id to limit the walk to")
    parser.add_argument(
        "--local-root",
        help="path to an already-mounted Drive (e.g. /content/drive/MyDrive) to "
        "read from the filesystem instead of the Drive API",
    )
    parser.add_argument("--location", default="US", help="BigQuery dataset location")
    parser.add_argument("--out", default="drive_inventory.json", help="inventory cache")
    parser.add_argument("--from-cache", action="store_true", help="reuse cached inventory")
    parser.add_argument("--dry-run", action="store_true", help="no BigQuery writes")
    parser.add_argument("--replace", action="store_true", help="truncate tables first")
    parser.add_argument("--no-resume", action="store_true", help="reload everything")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any failure")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
    )

    handler = {"inventory": cmd_inventory, "plan": cmd_plan, "load": cmd_load}[args.command]
    try:
        return handler(args)
    except Exception:
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
