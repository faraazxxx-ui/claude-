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
import chunk as chunk_mod  # noqa: E402
import dedupe  # noqa: E402
import drive as drive_mod  # noqa: E402
import graph as gr  # noqa: E402
import preflight  # noqa: E402
import quickinsights as qi  # noqa: E402
import vectorize as vec  # noqa: E402
from classify import build_families, partition, sanitize_table_name  # noqa: E402
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
        "content_hash": record.get("content_hash"),
        "duplicate_of": record.get("duplicate_of"),
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


def apply_exclusions(files: list[dict], args) -> tuple[list[dict], list[dict]]:
    """Split off excluded files and report what went."""
    kept, excluded = partition(
        files,
        skip_health=args.skip_health,
        exclude_path=args.exclude_path,
        exclude_family=args.exclude_family,
    )
    if excluded:
        reasons: dict[str, int] = {}
        for record in excluded:
            reasons[record["exclude_reason"]] = reasons.get(record["exclude_reason"], 0) + 1
        for reason, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
            log.info("excluded %d files: %s", count, reason)
    return kept, excluded


def apply_dedup(files: list[dict], args) -> tuple[list[dict], list[dict]]:
    """Drop duplicate content before anything expensive touches it.

    Embedding a document nine times costs nine times as much and, worse, makes
    every cross-link ranking start with a file matching its own copies at
    distance zero. Dedup first or the insight layer produces confident noise.
    """
    if args.no_dedup:
        for record in files:
            record.setdefault("content_hash", record.get("md5_checksum"))
        return files, []
    dedupe.assign_hashes(files)
    canonical, duplicates = dedupe.partition_duplicates(files)
    stats = dedupe.summarize(canonical, duplicates)
    if duplicates:
        log.info(
            "dedup: %d files -> %d distinct (%.2fx), %.1f MiB redundant",
            stats["total"], stats["canonical"], stats["factor"],
            stats["wasted_bytes"] / 1024 / 1024,
        )
        for name, copies, wasted in dedupe.top_duplicated(duplicates, 8):
            log.info("  %2d copies  %7.1f MiB redundant  %s", copies,
                     wasted / 1024 / 1024, name[:60])
    return canonical, duplicates


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

    total_found = len(files)
    files, excluded = apply_exclusions(files, args)
    files, duplicates = apply_dedup(files, args)
    stats = summarize(files)
    families = build_families(files)

    if duplicates:
        d = dedupe.summarize(files, duplicates)
        print(f"\nDuplicates: {d['duplicates']} redundant copies of "
              f"{d['canonical']} distinct files ({d['factor']}x), "
              f"{d['wasted_bytes'] / 1024 / 1024:,.1f} MiB")
        for name, copies, wasted in dedupe.top_duplicated(duplicates, 10):
            print(f"  {copies:>3} copies  {wasted / 1024 / 1024:>8.1f} MiB  {name[:56]}")

    print(f"\nFiles: {stats['count']} to load", end="")
    print(f"  ({len(excluded)} excluded of {total_found} found)" if excluded else "")
    for kind, count in sorted(stats["by_kind"].items(), key=lambda kv: -kv[1]):
        mib = stats["bytes_by_kind"].get(kind, 0) / 1024 / 1024
        print(f"  {kind:<10} {count:>6}  ({mib:,.1f} MiB)")

    if excluded:
        excluded_mib = sum(int(f.get("size_bytes") or 0) for f in excluded) / 1024 / 1024
        print(f"\nExcluded ({excluded_mib:,.1f} MiB), still listed in the manifest:")
        stems: dict[str, int] = {}
        for record in excluded:
            stems[record.get("family_stem") or record["kind"]] = (
                stems.get(record.get("family_stem") or record["kind"], 0) + 1
            )
        for stem, count in sorted(stems.items(), key=lambda kv: -kv[1])[:15]:
            print(f"  {stem:<48} {count:>5} files")
        if len(stems) > 15:
            print(f"  ... and {len(stems) - 15} more families")

    print(f"\n{TABLES_DATASET}: {len(families)} tables")
    for name, family in sorted(families.items(), key=lambda kv: -len(kv[1].files)):
        mib = family.total_bytes / 1024 / 1024
        print(f"  {name:<48} {len(family.files):>5} files  ({mib:,.1f} MiB)")

    docs = [f for f in files if f["kind"] == "document"]
    other = [f for f in files if f["kind"] in {"media", "other"}]
    print(f"\n{DOCS_DATASET}.documents: {len(docs)} files (chunked for embedding)")
    print(f"{RAW_DATASET}.file_manifest: {total_found} files "
          f"({len(other)} metadata only, {len(excluded)} excluded)")
    if args.vectorize:
        print(f"{vec.VECTORS_DATASET}.embeddings: document chunks + "
              f"{len(other)} file-metadata rows + rows of chosen tables")
    return 0


def cmd_load(args) -> int:
    drive_service = make_drive_service(optional=bool(args.local_root))
    loader = bq.Loader(args.project, args.location, dry_run=args.dry_run)
    preflight.run(loader, args.project,
                  [RAW_DATASET, TABLES_DATASET, DOCS_DATASET], args.location,
                  need_vertex=args.vectorize, connection=vec.CONNECTION_NAME)

    for dataset in (RAW_DATASET, TABLES_DATASET, DOCS_DATASET):
        loader.ensure_dataset(dataset)
    loader.ensure_table(RAW_DATASET, bq.MANIFEST_TABLE, bq.MANIFEST_SCHEMA)
    loader.ensure_table(DOCS_DATASET, bq.DOCUMENTS_TABLE, bq.DOCUMENTS_SCHEMA)
    loader.ensure_table(DOCS_DATASET, bq.CHUNKS_TABLE, bq.CHUNKS_SCHEMA)

    if args.from_cache and Path(args.out).is_file():
        files = json.loads(Path(args.out).read_text())
        log.info("loaded %d files from cache %s", len(files), args.out)
    else:
        files = enumerate_drive(args, drive_service)
        Path(args.out).write_text(json.dumps(files, indent=2))

    total_found = len(files)
    files, excluded = apply_exclusions(files, args)
    files, duplicates = apply_dedup(files, args)

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
    counters = {"loaded": 0, "skipped": 0, "failed": 0, "rows": 0, "chunks": 0}

    # Duplicates are censused with a pointer to their canonical copy, so
    # "where are all the copies of this" stays answerable without re-ingesting.
    for record in duplicates:
        manifest.append(
            manifest_row(
                record,
                ingest_status="duplicate",
                ingest_error=f"duplicate of {record.get('duplicate_of_path')}",
            )
        )

    # Excluded files are still censused, so drive_raw stays a complete picture of
    # the Drive even when the load is deliberately scoped.
    for record in excluded:
        manifest.append(
            manifest_row(
                record,
                ingest_status="excluded",
                ingest_error=record.get("exclude_reason"),
            )
        )

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

    # ---- documents -> drive_documents (+ chunks for embedding) -------------
    doc_rows: list[dict] = []
    chunk_rows: list[dict] = []
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
            # Chunk for embedding. One vector per document would average away
            # the passage you were actually looking for.
            pieces = chunk_mod.chunk_document(record, text)
            for piece in pieces:
                chunk_rows.append({**piece, "ingested_at": now()})
            counters["chunks"] += len(pieces)

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
        if len(chunk_rows) >= 5000:
            loader.load_rows(chunk_rows, DOCS_DATASET, bq.CHUNKS_TABLE, bq.CHUNKS_SCHEMA)
            chunk_rows = []

    loader.load_rows(doc_rows, DOCS_DATASET, bq.DOCUMENTS_TABLE, bq.DOCUMENTS_SCHEMA)
    loader.load_rows(chunk_rows, DOCS_DATASET, bq.CHUNKS_TABLE, bq.CHUNKS_SCHEMA)

    # ---- everything else: metadata only ------------------------------------
    for record in files:
        if record["kind"] in {"media", "other"} and record["file_id"] not in done:
            manifest.append(manifest_row(record, ingest_status="metadata_only"))

    loader.load_rows(manifest, RAW_DATASET, bq.MANIFEST_TABLE, bq.MANIFEST_SCHEMA)

    log.info(
        "done: %d loaded, %d skipped, %d failed, %d excluded, "
        "%d rows into %d tables, %d chunks",
        counters["loaded"],
        counters["skipped"],
        counters["failed"],
        len(excluded),
        counters["rows"],
        len(families),
        counters["chunks"],
    )
    counters["excluded"] = len(excluded)
    counters["duplicates"] = len(duplicates)
    counters["found"] = total_found
    print(json.dumps(counters, indent=2))

    if args.vectorize:
        log.info("vectorizing ...")
        rc = run_vectorize(args, loader)
        if rc:
            return rc
    return 1 if counters["failed"] and args.strict else 0


def run_vectorize(args, loader: bq.Loader) -> int:
    """Embed loaded content into drive_vectors.embeddings and index it.

    Idempotent throughout: the queue only ever receives ids that are not already
    embedded, so re-running after adding files embeds just the new material.
    """
    project = args.project
    preflight.run(loader, project, [vec.VECTORS_DATASET], args.location,
                  need_vertex=True, connection=vec.CONNECTION_NAME)

    loader.ensure_dataset(vec.VECTORS_DATASET)
    vec.ensure_connection(project, args.location, dry_run=args.dry_run)

    loader.sql(vec.create_model_sql(project, args.location, args.embedding_model), "model")
    loader.sql(vec.create_embeddings_table_sql(project), "embeddings table")
    loader.sql(vec.create_staging_table_sql(project), "embed queue")

    # Queue everything worth embedding.
    loader.sql(vec.enqueue_from_chunks_sql(project), "queue document chunks")
    loader.sql(vec.enqueue_file_metadata_sql(project), "queue file metadata")

    # Rows are only embedded for tables the caller names; telemetry rows are
    # meaningless as text and would dominate the index.
    for table in args.vectorize_tables or []:
        if table not in loader.list_table_ids(TABLES_DATASET) and not args.dry_run:
            log.warning("no such table %s.%s, skipping", TABLES_DATASET, table)
            continue
        loader.sql(
            vec.enqueue_table_rows_sql(project, table, args.max_rows_per_table),
            f"queue rows of {table}",
        )

    depth = loader.scalar(vec.queue_depth_sql(project), default=0) or 0
    log.info("%s rows queued for embedding", f"{depth:,}")

    # Drain the queue in batches so one oversized query cannot fail the lot.
    batches = 0
    while True:
        if args.dry_run:
            loader.sql(vec.embed_batch_sql(project, args.embed_batch), "embed batch")
            loader.sql(vec.dequeue_embedded_sql(project), "dequeue")
            break
        loader.sql(vec.embed_batch_sql(project, args.embed_batch), "embed batch")
        loader.sql(vec.dequeue_embedded_sql(project), "dequeue")
        batches += 1
        remaining = loader.scalar(vec.queue_depth_sql(project), default=0) or 0
        log.info("batch %d done, %s still queued", batches, f"{remaining:,}")
        if remaining == 0:
            break
        if remaining >= depth and batches > 1:
            # Nothing drained this round: every remaining row is failing.
            log.error(
                "embedding stalled with %s rows queued; inspect "
                "`%s.%s.embed_queue` and the model's status output",
                f"{remaining:,}",
                project,
                vec.VECTORS_DATASET,
            )
            return 1
        depth = remaining
        if batches >= args.max_batches:
            log.warning(
                "stopping after %d batches with %s queued; re-run `vectorize` to continue",
                batches,
                f"{remaining:,}",
            )
            break

    total = loader.scalar(
        f"SELECT COUNT(*) FROM `{project}.{vec.VECTORS_DATASET}.{vec.EMBEDDINGS_TABLE}`",
        default=0,
    ) or 0
    log.info("%s vectors in %s.%s", f"{total:,}", vec.VECTORS_DATASET, vec.EMBEDDINGS_TABLE)

    # A vector index only kicks in above a row threshold; below it BigQuery
    # brute-forces the scan, which is correct but slower.
    if total >= vec.INDEX_MIN_ROWS or args.dry_run:
        loader.sql(vec.create_index_sql(project), "vector index")
    else:
        log.info(
            "skipping vector index: %s rows is below BigQuery's %s-row minimum, "
            "so search will scan instead (same results)",
            f"{total:,}",
            f"{vec.INDEX_MIN_ROWS:,}",
        )

    loader.sql(vec.create_search_function_sql(project), "search function")
    log.info(
        "search with:  SELECT * FROM `%s.%s.search`('your question', 10)",
        project,
        vec.VECTORS_DATASET,
    )
    return 0


def cmd_vectorize(args) -> int:
    loader = bq.Loader(args.project, args.location, dry_run=args.dry_run)
    return run_vectorize(args, loader)


def run_crosslink(args, loader: bq.Loader) -> int:
    """Pass 1: search the embeddings against themselves and record the edges."""
    project = args.project
    loader.ensure_dataset(gr.GRAPH_DATASET)
    loader.ensure_dataset(gr.INSIGHTS_DATASET)
    loader.sql(gr.create_state_table_sql(project), "state table")

    log.info("crossing every chunk against every other chunk ...")
    loader.sql(
        gr.build_links_sql(
            project, vec.VECTORS_DATASET, vec.EMBEDDINGS_TABLE,
            neighbours=args.neighbours, max_distance=args.max_link_distance,
        ),
        "build cross links",
    )
    links = loader.scalar(
        f"SELECT COUNT(*) FROM `{project}.{gr.GRAPH_DATASET}.{gr.LINKS_TABLE}`", default=0
    ) or 0
    log.info("%s cross-file links", f"{links:,}")
    loader.sql(gr.record_state_sql(project, "cross_links", links), "state")
    return 0


def run_entities(args, loader: bq.Loader) -> int:
    """Pass 2: extract entities, resolve them, and push them through the edges."""
    project = args.project
    loader.ensure_dataset(gr.GRAPH_DATASET)
    loader.sql(gr.create_mentions_table_sql(project), "mentions table")
    loader.sql(
        gr.create_extractor_model_sql(
            project, vec.VECTORS_DATASET, args.location,
            vec.CONNECTION_NAME, args.text_model,
        ),
        "extractor model",
    )

    pending = loader.scalar(
        gr.pending_extraction_sql(project, vec.VECTORS_DATASET), default=0
    ) or 0
    log.info("%s chunks awaiting entity extraction", f"{pending:,}")

    batches = 0
    while True:
        loader.sql(
            gr.extract_entities_sql(project, vec.VECTORS_DATASET, args.extract_batch),
            "extract entities",
        )
        if args.dry_run:
            break
        batches += 1
        remaining = loader.scalar(
            gr.pending_extraction_sql(project, vec.VECTORS_DATASET), default=0
        ) or 0
        log.info("batch %d done, %s chunks left", batches, f"{remaining:,}")
        if remaining == 0:
            break
        if remaining >= pending:
            # Nothing consumed: every remaining chunk is failing extraction.
            log.error(
                "extraction stalled at %s chunks. The generative SQL in "
                "graph.extract_entities_sql is the thing to check.",
                f"{remaining:,}",
            )
            return 1
        pending = remaining
        if batches >= args.max_batches:
            log.warning("stopping after %d batches, %s left", batches, f"{remaining:,}")
            break

    loader.sql(gr.build_entities_sql(project), "resolve entities")
    mentions = loader.scalar(
        f"SELECT COUNT(*) FROM `{project}.{gr.GRAPH_DATASET}.{gr.MENTIONS_TABLE}`", default=0
    ) or 0
    entities = loader.scalar(
        f"SELECT COUNT(*) FROM `{project}.{gr.GRAPH_DATASET}.{gr.ENTITIES_TABLE}`", default=0
    ) or 0
    log.info("%s mentions resolving to %s entities", f"{mentions:,}", f"{entities:,}")
    loader.sql(gr.record_state_sql(project, "entities", entities), "state")
    return 0


def run_insights(args, loader: bq.Loader) -> int:
    """Build the derived views. Cheap and idempotent -- they are just views."""
    project = args.project
    loader.ensure_dataset(gr.INSIGHTS_DATASET)

    for label, statement in [
        ("entity_timeline", gr.entity_timeline_view_sql(project)),
        ("entity_cooccurrence", gr.cooccurrence_view_sql(project)),
        ("indirect_relations", gr.indirect_relations_view_sql(project)),
        ("file_bridges", gr.file_bridges_view_sql(project)),
        ("entity_gaps", gr.entity_gaps_view_sql(project)),
        ("recent_activity", gr.activity_view_sql(project)),
        ("pipeline_health", gr.health_view_sql(project)),
        ("ask", gr.ask_function_sql(project, vec.VECTORS_DATASET)),
    ]:
        loader.sql(statement, label)
        log.info("built %s.%s", gr.INSIGHTS_DATASET, label)

    if args.insight_feed:
        log.info("writing the narrated insight feed (this one calls Gemini) ...")
        loader.sql(
            gr.insight_feed_sql(project, vec.VECTORS_DATASET, args.feed_size),
            "insight feed",
        )
        rows = loader.scalar(
            f"SELECT COUNT(*) FROM `{project}.{gr.INSIGHTS_DATASET}.insight_feed`", default=0
        ) or 0
        log.info("%s narrated insights", f"{rows:,}")
        loader.sql(gr.record_state_sql(project, "insight_feed", rows), "state")

    log.info("ask a question:  SELECT * FROM `%s.%s.ask`('...', 12)",
             project, gr.INSIGHTS_DATASET)
    return 0


def run_quickinsights(args, loader: bq.Loader) -> int:
    """Insights needing no embeddings, no Vertex, and no LLM."""
    project = args.project
    preflight.run(loader, project, [qi.INSIGHTS_DATASET, RAW_DATASET], args.location)
    loader.ensure_dataset(qi.INSIGHTS_DATASET)
    for label, statement in qi.all_views(project):
        loader.sql(statement, label)
        log.info("built %s.%s", qi.INSIGHTS_DATASET, label)

    if args.dry_run:
        return 0

    rows = list(loader.client.query(qi.headline_sql(project)).result())
    if rows:
        r = rows[0]
        print("\n" + "=" * 62)
        print("  DRIVE AT A GLANCE")
        print("=" * 62)
        print(f"  files                {r.files:>12,}")
        print(f"  distinct contents    {r.distinct_contents:>12,}")
        print(f"  redundant copies     {r.duplicate_files:>12,}"
              f"   ({r.duplicate_gib} GiB)")
        print(f"  total size           {r.total_gib:>12} GiB")
        print(f"  documents            {r.documents:>12,}")
        print(f"  tabular              {r.tabular:>12,}")
        print(f"  media                {r.media:>12,}")
        print(f"  excluded             {r.excluded:>12,}")
        print(f"  failed               {r.failed:>12,}")
        print(f"  date range           {r.earliest} .. {r.latest}")
        print("=" * 62)

    print("\n  worst duplication:")
    for row in loader.client.query(f"""
        SELECT name, copies, ROUND(bytes_wasted / 1048576, 1) AS mib
        FROM `{project}.{qi.INSIGHTS_DATASET}.duplicates`
        ORDER BY bytes_wasted DESC LIMIT 12
    """).result():
        print(f"    {row.copies:>3} copies  {row.mib:>9,.1f} MiB  {row.name[:52]}")

    print("\n  documents most connected by shared rare terms:")
    for row in loader.client.query(f"""
        SELECT a_name, b_name, shared_terms, score, crosses_folder
        FROM `{project}.{qi.INSIGHTS_DATASET}.term_bridges`
        ORDER BY score DESC LIMIT 12
    """).result():
        flag = " *" if row.crosses_folder else "  "
        print(f"   {flag} {row.score:>7.2f}  {row.shared_terms:>4} terms  "
              f"{row.a_name[:28]:<30} <-> {row.b_name[:28]}")
    print("\n  (* = the two files live in different top-level folders)")
    return 0


def cmd_quickinsights(args) -> int:
    return run_quickinsights(args, bq.Loader(args.project, args.location,
                                            dry_run=args.dry_run))


def cmd_crosslink(args) -> int:
    return run_crosslink(args, bq.Loader(args.project, args.location, dry_run=args.dry_run))


def cmd_entities(args) -> int:
    return run_entities(args, bq.Loader(args.project, args.location, dry_run=args.dry_run))


def cmd_insights(args) -> int:
    return run_insights(args, bq.Loader(args.project, args.location, dry_run=args.dry_run))


def cmd_activate(args) -> int:
    """Everything downstream of the vector table, in order, then the schedules.

    This is the command to put on a timer: crossing, entities, insights.
    """
    loader = bq.Loader(args.project, args.location, dry_run=args.dry_run)
    for step in (run_crosslink, run_entities, run_insights):
        rc = step(args, loader)
        if rc:
            return rc

    print("\nTo let BigQuery refresh this on its own, run these once:\n")
    for name, command in gr.schedule_commands(args.project, args.location):
        print(f"# {name}\n{command}\n")
    print(
        "The ingest step still needs somewhere with Drive access (re-run the\n"
        "notebook, or put `load` on Cloud Run + Cloud Scheduler). Everything\n"
        "above is pure SQL, so BigQuery drives it with no machine of yours."
    )
    return 0


# ----------------------------------------------------------------------- main


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=["inventory", "plan", "load", "quickinsights", "vectorize",
                 "crosslink", "entities", "insights", "activate"],
    )
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

    scope = parser.add_argument_group("scope")
    scope.add_argument(
        "--skip-health",
        action="store_true",
        help="exclude wearable/health telemetry (Fitbit-style per-day exports). "
        "Excluded files are still recorded in the manifest as 'excluded'.",
    )
    scope.add_argument(
        "--no-dedup",
        action="store_true",
        help="load every copy of duplicated content (default is to keep one and "
        "record the rest in the manifest as 'duplicate')",
    )
    scope.add_argument("--exclude-path", help="regex; exclude files whose path matches")
    scope.add_argument("--exclude-family", help="regex; exclude matching table families")

    vector = parser.add_argument_group("vectors")
    vector.add_argument(
        "--vectorize",
        action="store_true",
        help="after loading, embed content into drive_vectors.embeddings",
    )
    vector.add_argument(
        "--vectorize-tables",
        nargs="*",
        metavar="TABLE",
        help="also embed the rows of these drive_tables tables (descriptive "
        "tables only -- telemetry rows are meaningless as text)",
    )
    vector.add_argument(
        "--embedding-model",
        default=vec.DEFAULT_ENDPOINT,
        help=f"Vertex embedding endpoint (default {vec.DEFAULT_ENDPOINT}; "
        "gemini-embedding-001 is newer but 3072-dim)",
    )
    vector.add_argument(
        "--embed-batch", type=int, default=vec.EMBED_BATCH_ROWS, help="rows per embed query"
    )
    vector.add_argument(
        "--max-batches", type=int, default=500, help="stop after this many embed batches"
    )
    vector.add_argument(
        "--max-rows-per-table",
        type=int,
        default=50_000,
        help="cap on rows embedded per table",
    )

    cross = parser.add_argument_group("crossing and insights")
    cross.add_argument(
        "--neighbours",
        type=int,
        default=gr.NEIGHBOURS_PER_CHUNK,
        help=f"cross-file neighbours kept per chunk (default {gr.NEIGHBOURS_PER_CHUNK})",
    )
    cross.add_argument(
        "--max-link-distance",
        type=float,
        default=gr.MAX_LINK_DISTANCE,
        help=f"cosine distance above which a link is discarded "
        f"(default {gr.MAX_LINK_DISTANCE})",
    )
    cross.add_argument(
        "--text-model",
        default=gr.DEFAULT_TEXT_ENDPOINT,
        help=f"Gemini endpoint for extraction and narration "
        f"(default {gr.DEFAULT_TEXT_ENDPOINT})",
    )
    cross.add_argument(
        "--extract-batch", type=int, default=2000, help="chunks per extraction query"
    )
    cross.add_argument(
        "--insight-feed",
        action="store_true",
        help="also have Gemini narrate the strongest bridges (costs tokens)",
    )
    cross.add_argument(
        "--feed-size", type=int, default=40, help="bridges to narrate"
    )

    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
    )

    handler = {
        "inventory": cmd_inventory,
        "plan": cmd_plan,
        "load": cmd_load,
        "quickinsights": cmd_quickinsights,
        "vectorize": cmd_vectorize,
        "crosslink": cmd_crosslink,
        "entities": cmd_entities,
        "insights": cmd_insights,
        "activate": cmd_activate,
    }[args.command]
    try:
        return handler(args)
    except preflight.PreflightError as exc:
        # A configuration problem with a known fix; a traceback would only bury it.
        print(f"\nCannot proceed:\n\n  {exc}\n", file=sys.stderr)
        return 3
    except Exception:
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
