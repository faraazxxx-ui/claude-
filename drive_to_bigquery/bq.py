"""BigQuery dataset/table management and loading."""

from __future__ import annotations

import io
import logging

import pandas as pd
from google.api_core import exceptions as gexc
from google.cloud import bigquery

log = logging.getLogger(__name__)

MANIFEST_TABLE = "file_manifest"
DOCUMENTS_TABLE = "documents"

MANIFEST_SCHEMA = [
    bigquery.SchemaField("file_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("path", "STRING"),
    bigquery.SchemaField("mime_type", "STRING"),
    bigquery.SchemaField("extension", "STRING"),
    bigquery.SchemaField("size_bytes", "INT64"),
    bigquery.SchemaField("md5_checksum", "STRING"),
    bigquery.SchemaField("created_time", "TIMESTAMP"),
    bigquery.SchemaField("modified_time", "TIMESTAMP"),
    bigquery.SchemaField("parent_id", "STRING"),
    bigquery.SchemaField("kind", "STRING"),
    bigquery.SchemaField("fmt", "STRING"),
    bigquery.SchemaField("family_stem", "STRING"),
    bigquery.SchemaField("shard_date", "DATE"),
    bigquery.SchemaField("content_hash", "STRING"),
    bigquery.SchemaField("duplicate_of", "STRING"),
    bigquery.SchemaField("target_dataset", "STRING"),
    bigquery.SchemaField("target_table", "STRING"),
    bigquery.SchemaField("ingest_status", "STRING"),
    bigquery.SchemaField("ingest_error", "STRING"),
    bigquery.SchemaField("row_count", "INT64"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP"),
]

CHUNKS_TABLE = "document_chunks"

CHUNKS_SCHEMA = [
    bigquery.SchemaField("chunk_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("file_id", "STRING"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("path", "STRING"),
    bigquery.SchemaField("chunk_index", "INT64"),
    bigquery.SchemaField("chunk_total", "INT64"),
    bigquery.SchemaField("char_count", "INT64"),
    # `content` is what gets embedded (name-prefixed); `raw_content` is the
    # verbatim passage, for display without the synthetic header.
    bigquery.SchemaField("content", "STRING"),
    bigquery.SchemaField("raw_content", "STRING"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP"),
]

DOCUMENTS_SCHEMA = [
    bigquery.SchemaField("file_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("path", "STRING"),
    bigquery.SchemaField("mime_type", "STRING"),
    bigquery.SchemaField("fmt", "STRING"),
    bigquery.SchemaField("size_bytes", "INT64"),
    bigquery.SchemaField("created_time", "TIMESTAMP"),
    bigquery.SchemaField("modified_time", "TIMESTAMP"),
    bigquery.SchemaField("page_count", "INT64"),
    bigquery.SchemaField("char_count", "INT64"),
    bigquery.SchemaField("extraction_method", "STRING"),
    bigquery.SchemaField("content", "STRING"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP"),
]

# Provenance columns prepended to every table in the tables dataset, so a row
# can always be traced back to the Drive file it came from.
PROVENANCE = ("_src_file_id", "_src_file_name", "_src_date", "_src_sheet", "_ingested_at")


class Loader:
    def __init__(self, project: str, location: str = "US", dry_run: bool = False):
        self.project = project
        self.location = location
        self.dry_run = dry_run
        self.client = None if dry_run else bigquery.Client(project=project)

    # ---------------------------------------------------------------- datasets

    def ensure_dataset(self, dataset_id: str) -> None:
        if self.dry_run:
            log.info("[dry-run] ensure dataset %s.%s", self.project, dataset_id)
            return
        ref = bigquery.Dataset(f"{self.project}.{dataset_id}")
        ref.location = self.location
        try:
            self.client.create_dataset(ref)
            log.info("created dataset %s", dataset_id)
        except gexc.Conflict:
            log.debug("dataset %s already exists", dataset_id)

    def ensure_table(self, dataset_id: str, table_id: str, schema: list) -> None:
        if self.dry_run:
            log.info("[dry-run] ensure table %s.%s", dataset_id, table_id)
            return
        table = bigquery.Table(f"{self.project}.{dataset_id}.{table_id}", schema=schema)
        try:
            self.client.create_table(table)
            log.info("created table %s.%s", dataset_id, table_id)
        except gexc.Conflict:
            log.debug("table %s.%s already exists", dataset_id, table_id)

    # ------------------------------------------------------------------ loads

    def load_frame(
        self,
        frame: pd.DataFrame,
        dataset_id: str,
        table_id: str,
        write_disposition: str = "WRITE_APPEND",
    ) -> int:
        """Load a DataFrame via Parquet, letting the schema widen as needed."""
        if frame.empty:
            return 0
        if self.dry_run:
            log.info(
                "[dry-run] load %d rows x %d cols -> %s.%s",
                len(frame),
                len(frame.columns),
                dataset_id,
                table_id,
            )
            return len(frame)

        buffer = io.BytesIO()
        frame.to_parquet(buffer, index=False, engine="pyarrow")
        buffer.seek(0)

        config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=write_disposition,
            autodetect=True,
            schema_update_options=[
                bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
            ],
        )
        target = f"{self.project}.{dataset_id}.{table_id}"
        job = self.client.load_table_from_file(buffer, target, job_config=config)
        job.result()
        if job.errors:
            raise RuntimeError(f"load into {target} failed: {job.errors}")
        return len(frame)

    def load_rows(self, rows: list[dict], dataset_id: str, table_id: str, schema: list) -> int:
        """Load explicit dict rows against a fixed schema (manifest, documents)."""
        if not rows:
            return 0
        if self.dry_run:
            log.info("[dry-run] load %d rows -> %s.%s", len(rows), dataset_id, table_id)
            return len(rows)

        frame = pd.DataFrame(rows)
        buffer = io.BytesIO()
        frame.to_parquet(buffer, index=False, engine="pyarrow")
        buffer.seek(0)
        config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition="WRITE_APPEND",
            schema=schema,
        )
        target = f"{self.project}.{dataset_id}.{table_id}"
        job = self.client.load_table_from_file(buffer, target, job_config=config)
        job.result()
        if job.errors:
            raise RuntimeError(f"load into {target} failed: {job.errors}")
        return len(rows)

    # ----------------------------------------------------------------- resume

    def already_ingested(self, dataset_id: str) -> set[str]:
        """File ids already recorded as loaded, so a rerun resumes cleanly."""
        if self.dry_run:
            return set()
        query = f"""
            SELECT DISTINCT file_id
            FROM `{self.project}.{dataset_id}.{MANIFEST_TABLE}`
            WHERE ingest_status = 'loaded'
        """
        try:
            return {row.file_id for row in self.client.query(query).result()}
        except gexc.NotFound:
            return set()

    # -------------------------------------------------------------------- sql

    def sql(self, statement: str, label: str = "") -> object | None:
        """Run one statement. Returns the row iterator, or None in dry-run."""
        if self.dry_run:
            log.info("[dry-run] %s\n%s", label or "sql", statement)
            return None
        log.debug("%s\n%s", label or "sql", statement)
        job = self.client.query(statement)
        return job.result()

    def scalar(self, statement: str, default=None):
        """Run a statement and return the first column of the first row."""
        if self.dry_run:
            log.info("[dry-run] scalar: %s", statement)
            return default
        for row in self.client.query(statement).result():
            return row[0]
        return default

    def list_table_ids(self, dataset_id: str) -> list[str]:
        if self.dry_run:
            return []
        try:
            return [t.table_id for t in self.client.list_tables(f"{self.project}.{dataset_id}")]
        except gexc.NotFound:
            return []
