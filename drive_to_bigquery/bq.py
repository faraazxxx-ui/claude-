"""BigQuery dataset/table management and loading."""

from __future__ import annotations

import io
import logging

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
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


# BigQuery field type -> the exact Arrow type its Parquet column must carry.
_ARROW_TYPES = {
    "STRING": pa.string(),
    "BYTES": pa.binary(),
    "INT64": pa.int64(),
    "INTEGER": pa.int64(),
    "FLOAT64": pa.float64(),
    "FLOAT": pa.float64(),
    "NUMERIC": pa.float64(),
    "BOOL": pa.bool_(),
    "BOOLEAN": pa.bool_(),
    "TIMESTAMP": pa.timestamp("us", tz="UTC"),
    "DATETIME": pa.timestamp("us"),
    "DATE": pa.date32(),
}


def to_parquet_bytes(frame: pd.DataFrame, schema: list) -> io.BytesIO:
    """Serialise a frame to Parquet with types pinned by the BigQuery schema.

    Casting pandas dtypes alone is not enough: a column that is entirely null
    serialises as Arrow `null` whatever its pandas dtype, and BigQuery rejects
    that for anything but a STRING field. Building the Arrow schema explicitly
    pins every column, empty or not.
    """
    frame = coerce_to_schema(frame, schema)
    fields = []
    for field in schema:
        arrow_type = _ARROW_TYPES.get(field.field_type.upper(), pa.string())
        if field.name not in frame.columns:
            # A schema field the caller never populated still needs a column, or
            # from_pandas rejects the frame.
            frame[field.name] = None
        fields.append(pa.field(field.name, arrow_type, nullable=field.mode != "REQUIRED"))

    table = pa.Table.from_pandas(
        frame[[f.name for f in schema]], schema=pa.schema(fields), preserve_index=False
    )
    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)
    return buffer


def coerce_to_schema(frame: pd.DataFrame, schema: list) -> pd.DataFrame:
    """Cast a DataFrame so its Parquet types match a declared BigQuery schema.

    Loading Parquet against an explicit schema is strict: the Parquet physical
    type has to match the declared field type. Two pandas behaviours break that
    silently, and both bite the very first load:

    * An INT64 column containing any None becomes float64, so Parquet carries
      `double` where BigQuery expects an integer.
    * ISO-8601 strings stay strings. A TIMESTAMP or DATE field receives
      `large_string` and the load is rejected.

    An all-null column is a third case: it serialises as Parquet `null`, which a
    STRING field tolerates but an INT64 or TIMESTAMP field does not, so the cast
    is applied even when there is nothing to convert.
    """
    frame = frame.copy()
    for field in schema:
        name, kind = field.name, field.field_type.upper()
        if name not in frame.columns:
            continue
        column = frame[name]
        try:
            if kind in {"INT64", "INTEGER"}:
                # Nullable integer, so None survives without forcing float.
                frame[name] = pd.to_numeric(column, errors="coerce").astype("Int64")
            elif kind in {"FLOAT64", "FLOAT"}:
                frame[name] = pd.to_numeric(column, errors="coerce").astype("Float64")
            elif kind in {"BOOL", "BOOLEAN"}:
                frame[name] = column.astype("boolean")
            elif kind == "TIMESTAMP":
                frame[name] = pd.to_datetime(column, errors="coerce", utc=True, format="ISO8601")
            elif kind == "DATE":
                parsed = pd.to_datetime(column, errors="coerce", format="ISO8601")
                # BigQuery wants a date, not a midnight timestamp.
                frame[name] = parsed.dt.date.astype("object").where(parsed.notna(), None)
            else:
                frame[name] = column.astype("string")
        except (TypeError, ValueError) as exc:
            raise RuntimeError(
                f"column {name!r} cannot be cast to {kind} for load: {exc}"
            ) from exc
    return frame


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

        buffer = to_parquet_bytes(pd.DataFrame(rows), schema)
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
