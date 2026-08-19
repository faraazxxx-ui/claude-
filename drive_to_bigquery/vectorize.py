"""Embed loaded content into a searchable vector table in BigQuery.

Embeddings are generated *inside* BigQuery via `ML.GENERATE_EMBEDDING` against a
remote Vertex AI model, so the text never leaves BigQuery and there is no
client-side embedding loop to babysit or pay egress on.

Four steps, each idempotent:

1. a CLOUD_RESOURCE connection from BigQuery to Vertex AI  (one-time, needs the
   `bq` CLI and an IAM grant -- see `connection_commands`)
2. a remote MODEL wrapping a Vertex text-embedding endpoint
3. `drive_vectors.embeddings` -- one row per embedded unit, all sources unified
4. a VECTOR INDEX over it, plus a `search` table function

Everything lands in ONE vector table on purpose. A document chunk, a spreadsheet
row and a photo's filename are all just text with provenance, and one index over
all of them means one query searches the whole Drive.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess

log = logging.getLogger(__name__)

VECTORS_DATASET = "drive_vectors"
EMBEDDINGS_TABLE = "embeddings"
MODEL_NAME = "embedder"
CONNECTION_NAME = "drive_vertex"
INDEX_NAME = "embeddings_idx"

# Vertex text-embedding endpoint. `text-embedding-005` is the stable default;
# `gemini-embedding-001` is newer and higher quality but returns 3072 dims,
# which makes for a much larger index. Override with --embedding-model.
DEFAULT_ENDPOINT = "text-embedding-005"

# BigQuery only *uses* a vector index once the table is large enough; below this
# it silently falls back to a brute-force scan, which is correct but slower.
INDEX_MIN_ROWS = 5000

# ML.GENERATE_EMBEDDING is billed per input token and rate limited, so text is
# embedded in batches rather than one enormous query.
EMBED_BATCH_ROWS = 20_000


def connection_commands(project: str, location: str) -> list[str]:
    """Shell commands that create the Vertex connection and grant it access.

    Kept as text rather than executed blindly: the IAM grant widens a project's
    permissions, so it should be visible and reviewable before it runs.
    """
    conn = f"{project}.{location}.{CONNECTION_NAME}"
    return [
        f"bq mk --connection --location={location} --project_id={project} "
        f"--connection_type=CLOUD_RESOURCE {CONNECTION_NAME}",
        f"bq show --format=json --connection {conn}",
        # The connection gets its own service account; it needs Vertex access.
        f"gcloud projects add-iam-policy-binding {project} "
        f"--member=serviceAccount:$CONNECTION_SA --role=roles/aiplatform.user",
    ]


def ensure_connection(project: str, location: str, dry_run: bool = False) -> str | None:
    """Create the connection if absent and return its service account id."""
    if not shutil.which("bq"):
        log.warning("bq CLI not found; create the connection manually")
        return None

    conn = f"{project}.{location}.{CONNECTION_NAME}"
    show = ["bq", "show", "--format=json", "--connection", conn]

    result = subprocess.run(show, capture_output=True, text=True)
    if result.returncode != 0:
        if dry_run:
            log.info("[dry-run] would create connection %s", conn)
            return None
        log.info("creating connection %s", conn)
        create = subprocess.run(
            [
                "bq", "mk", "--connection",
                f"--location={location}",
                f"--project_id={project}",
                "--connection_type=CLOUD_RESOURCE",
                CONNECTION_NAME,
            ],
            capture_output=True,
            text=True,
        )
        if create.returncode != 0:
            raise RuntimeError(f"could not create connection: {create.stderr.strip()}")
        result = subprocess.run(show, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"connection created but unreadable: {result.stderr.strip()}")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    account = (payload.get("cloudResource") or {}).get("serviceAccountId")
    if account:
        log.info("connection service account: %s", account)
        log.info(
            "if embedding fails with a permission error, grant it Vertex access:\n"
            "  gcloud projects add-iam-policy-binding %s \\\n"
            "    --member=serviceAccount:%s --role=roles/aiplatform.user",
            project,
            account,
        )
    return account


def create_model_sql(project: str, location: str, endpoint: str = DEFAULT_ENDPOINT) -> str:
    return f"""
CREATE OR REPLACE MODEL `{project}.{VECTORS_DATASET}.{MODEL_NAME}`
REMOTE WITH CONNECTION `{project}.{location}.{CONNECTION_NAME}`
OPTIONS (ENDPOINT = '{endpoint}')
""".strip()


def create_embeddings_table_sql(project: str) -> str:
    """The unified vector table.

    `embedding` is left as ARRAY<FLOAT64> rather than a fixed-width type because
    the dimension depends on which endpoint is configured.
    """
    return f"""
CREATE TABLE IF NOT EXISTS `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}` (
  vector_id     STRING NOT NULL,
  source_kind   STRING,      -- document_chunk | table_row | file_metadata
  source_table  STRING,
  file_id       STRING,
  name          STRING,
  path          STRING,
  chunk_index   INT64,
  chunk_total   INT64,
  content       STRING,
  embedding     ARRAY<FLOAT64>,
  embedded_at   TIMESTAMP
)
""".strip()


def create_staging_table_sql(project: str) -> str:
    """Text waiting to be embedded. Emptied as batches succeed."""
    return f"""
CREATE TABLE IF NOT EXISTS `{project}.{VECTORS_DATASET}.embed_queue` (
  vector_id     STRING NOT NULL,
  source_kind   STRING,
  source_table  STRING,
  file_id       STRING,
  name          STRING,
  path          STRING,
  chunk_index   INT64,
  chunk_total   INT64,
  content       STRING,
  queued_at     TIMESTAMP
)
""".strip()


def enqueue_from_chunks_sql(project: str) -> str:
    """Queue every document chunk not already embedded."""
    return f"""
INSERT INTO `{project}.{VECTORS_DATASET}.embed_queue`
  (vector_id, source_kind, source_table, file_id, name, path,
   chunk_index, chunk_total, content, queued_at)
SELECT
  c.chunk_id                        AS vector_id,
  'document_chunk'                  AS source_kind,
  'drive_documents.document_chunks' AS source_table,
  c.file_id, c.name, c.path, c.chunk_index, c.chunk_total,
  c.content,
  CURRENT_TIMESTAMP()               AS queued_at
FROM `{project}.drive_documents.document_chunks` c
WHERE c.content IS NOT NULL AND LENGTH(TRIM(c.content)) > 0
  AND NOT EXISTS (
    SELECT 1 FROM `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}` e
    WHERE e.vector_id = c.chunk_id
  )
  AND NOT EXISTS (
    SELECT 1 FROM `{project}.{VECTORS_DATASET}.embed_queue` q
    WHERE q.vector_id = c.chunk_id
  )
""".strip()


def enqueue_file_metadata_sql(project: str) -> str:
    """Queue a text line per non-tabular file so media is findable by name.

    A photo has no extractable content, but its name and folder path carry real
    signal -- this is what makes "that scan from the hospital" locatable at all.
    """
    return f"""
INSERT INTO `{project}.{VECTORS_DATASET}.embed_queue`
  (vector_id, source_kind, source_table, file_id, name, path,
   chunk_index, chunk_total, content, queued_at)
SELECT
  CONCAT('meta::', m.file_id) AS vector_id,
  'file_metadata'             AS source_kind,
  'drive_raw.file_manifest'   AS source_table,
  m.file_id, m.name, m.path,
  CAST(NULL AS INT64) AS chunk_index,
  CAST(NULL AS INT64) AS chunk_total,
  CONCAT(
    'File: ', m.name, '\\n',
    'Folder: ', IFNULL(REGEXP_EXTRACT(m.path, r'^(.*)/[^/]+$'), '(root)'), '\\n',
    'Type: ', IFNULL(m.fmt, 'unknown'), ' (', IFNULL(m.kind, 'unknown'), ')', '\\n',
    'Modified: ', IFNULL(CAST(DATE(m.modified_time) AS STRING), 'unknown')
  ) AS content,
  CURRENT_TIMESTAMP() AS queued_at
FROM `{project}.drive_raw.file_manifest` m
WHERE m.kind IN ('media', 'other')
  AND NOT EXISTS (
    SELECT 1 FROM `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}` e
    WHERE e.vector_id = CONCAT('meta::', m.file_id)
  )
  AND NOT EXISTS (
    SELECT 1 FROM `{project}.{VECTORS_DATASET}.embed_queue` q
    WHERE q.vector_id = CONCAT('meta::', m.file_id)
  )
""".strip()


def enqueue_table_rows_sql(project: str, table: str, limit: int) -> str:
    """Queue a text rendering of each row of one table.

    Only worth doing for tables whose rows are descriptive rather than
    telemetry, which is why the caller chooses which tables. Rows are rendered
    as JSON so column names travel with the values -- `"grade":"fail"` embeds
    far better than a bare `fail`.
    """
    return f"""
INSERT INTO `{project}.{VECTORS_DATASET}.embed_queue`
  (vector_id, source_kind, source_table, file_id, name, path,
   chunk_index, chunk_total, content, queued_at)
SELECT
  CONCAT('row::{table}::', CAST(rn AS STRING)) AS vector_id,
  'table_row'                                  AS source_kind,
  'drive_tables.{table}'                       AS source_table,
  file_id,
  name,
  CAST(NULL AS STRING)                         AS path,
  CAST(NULL AS INT64)                          AS chunk_index,
  CAST(NULL AS INT64)                          AS chunk_total,
  CONCAT('Table: {table}\\n', content)          AS content,
  CURRENT_TIMESTAMP()                          AS queued_at
FROM (
  SELECT
    ROW_NUMBER() OVER (ORDER BY _src_file_name, _src_date) AS rn,
    _src_file_id      AS file_id,
    _src_file_name    AS name,
    TO_JSON_STRING(t) AS content
  FROM `{project}.drive_tables.{table}` t
  LIMIT {limit}
)
WHERE content IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}` e
    WHERE e.vector_id = CONCAT('row::{table}::', CAST(rn AS STRING))
  )
""".strip()


def embed_batch_sql(
    project: str, batch_rows: int = EMBED_BATCH_ROWS, task_type: str = "RETRIEVAL_DOCUMENT"
) -> str:
    """Embed one batch off the queue and move it into the vector table.

    `flatten_json_output` gives `ml_generate_embedding_result` as a plain
    ARRAY<FLOAT64>. Rows whose status is non-empty failed and are left in the
    queue rather than being written with a null vector.
    """
    return f"""
INSERT INTO `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}`
  (vector_id, source_kind, source_table, file_id, name, path,
   chunk_index, chunk_total, content, embedding, embedded_at)
SELECT
  vector_id, source_kind, source_table, file_id, name, path,
  chunk_index, chunk_total, content,
  ml_generate_embedding_result AS embedding,
  CURRENT_TIMESTAMP()          AS embedded_at
FROM ML.GENERATE_EMBEDDING(
  MODEL `{project}.{VECTORS_DATASET}.{MODEL_NAME}`,
  (
    SELECT vector_id, source_kind, source_table, file_id, name, path,
           chunk_index, chunk_total, content
    FROM `{project}.{VECTORS_DATASET}.embed_queue`
    LIMIT {batch_rows}
  ),
  STRUCT(TRUE AS flatten_json_output, '{task_type}' AS task_type)
)
WHERE ml_generate_embedding_status = ''
  AND ARRAY_LENGTH(ml_generate_embedding_result) > 0
""".strip()


def dequeue_embedded_sql(project: str) -> str:
    """Drop queue rows that made it into the vector table."""
    return f"""
DELETE FROM `{project}.{VECTORS_DATASET}.embed_queue` q
WHERE EXISTS (
  SELECT 1 FROM `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}` e
  WHERE e.vector_id = q.vector_id
)
""".strip()


def queue_depth_sql(project: str) -> str:
    return f"SELECT COUNT(*) AS n FROM `{project}.{VECTORS_DATASET}.embed_queue`"


def create_index_sql(project: str) -> str:
    return f"""
CREATE OR REPLACE VECTOR INDEX {INDEX_NAME}
ON `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}`(embedding)
OPTIONS (index_type = 'IVF', distance_type = 'COSINE')
""".strip()


def create_search_function_sql(project: str) -> str:
    """A table function so searching is one short query, not a nested mess."""
    return f"""
CREATE OR REPLACE TABLE FUNCTION `{project}.{VECTORS_DATASET}.search`(
  query STRING, top_k INT64
)
AS (
  SELECT
    base.name        AS name,
    base.path        AS path,
    base.source_kind AS source_kind,
    base.chunk_index AS chunk_index,
    distance,
    base.content     AS content
  FROM VECTOR_SEARCH(
    TABLE `{project}.{VECTORS_DATASET}.{EMBEDDINGS_TABLE}`,
    'embedding',
    (
      SELECT ml_generate_embedding_result AS embedding
      FROM ML.GENERATE_EMBEDDING(
        MODEL `{project}.{VECTORS_DATASET}.{MODEL_NAME}`,
        (SELECT query AS content),
        STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type)
      )
    ),
    top_k => top_k,
    distance_type => 'COSINE'
  )
);
""".strip()
