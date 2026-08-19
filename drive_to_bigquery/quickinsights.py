"""Insights that need no embeddings, no Vertex connection, and no LLM.

The expensive path (embed -> cross-link -> extract entities) is genuinely more
powerful, but it is also slow, costs real money, and cannot run until a Vertex
connection exists. A large share of useful insight does not need any of it, and
making people climb through the expensive layer to see anything is the wrong
order of work.

Everything here is plain SQL over `drive_raw.file_manifest` and
`drive_documents`. It runs in seconds, costs cents, and depends on nothing that
can be misconfigured.

The one non-obvious piece is `term_bridges`: it crosses documents against each
other using shared *rare terms* rather than vectors. Less semantically subtle
than embeddings -- it will not spot a paraphrase -- but for records work it is
arguably better, because what actually matters is shared identifiers: a name, a
case number, a specific phrase. It needs no model at all.
"""

from __future__ import annotations

INSIGHTS_DATASET = "drive_insights"

# A term appearing in this fraction of documents or more is structural
# boilerplate ("patient", "the", a letterhead) and links everything to
# everything, so it is excluded from bridging.
MAX_DOC_FRACTION = 0.20

# Below this many characters a "document" is a stub and its terms are noise.
MIN_DOC_CHARS = 200


def duplicates_view_sql(project: str) -> str:
    """Every duplicate group, ranked by wasted space."""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.duplicates` AS
SELECT
  ANY_VALUE(name)                    AS name,
  content_hash,
  COUNT(*)                           AS copies,
  ANY_VALUE(size_bytes)              AS bytes_each,
  (COUNT(*) - 1) * ANY_VALUE(size_bytes) AS bytes_wasted,
  ARRAY_AGG(path ORDER BY path)      AS paths,
  ARRAY_AGG(DISTINCT REGEXP_EXTRACT(path, r'^([^/]+)') IGNORE NULLS
            ORDER BY REGEXP_EXTRACT(path, r'^([^/]+)')) AS top_folders
FROM `{project}.drive_raw.file_manifest`
WHERE content_hash IS NOT NULL
GROUP BY content_hash
HAVING copies > 1
""".strip()


def storage_view_sql(project: str) -> str:
    """Where the bytes actually are, and how much of it is redundant."""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.storage` AS
WITH per_folder AS (
  SELECT
    IFNULL(REGEXP_EXTRACT(path, r'^([^/]+)'), '(root)') AS top_folder,
    kind,
    COUNT(*)        AS files,
    SUM(size_bytes) AS bytes,
    COUNTIF(ingest_status = 'duplicate') AS duplicate_files,
    SUM(IF(ingest_status = 'duplicate', size_bytes, 0)) AS duplicate_bytes
  FROM `{project}.drive_raw.file_manifest`
  GROUP BY top_folder, kind
)
SELECT
  top_folder, kind, files, bytes,
  duplicate_files, duplicate_bytes,
  SAFE_DIVIDE(duplicate_bytes, bytes) AS redundant_fraction
FROM per_folder
""".strip()


def census_view_sql(project: str) -> str:
    """The straight answer to "what is actually in here"."""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.census` AS
SELECT
  kind,
  fmt,
  COUNT(*)                             AS files,
  COUNT(DISTINCT content_hash)         AS distinct_contents,
  SUM(size_bytes)                      AS bytes,
  MIN(DATE(modified_time))             AS earliest,
  MAX(DATE(modified_time))             AS latest,
  COUNTIF(ingest_status = 'loaded')    AS loaded,
  COUNTIF(ingest_status = 'duplicate') AS duplicates,
  COUNTIF(ingest_status = 'excluded')  AS excluded,
  COUNTIF(ingest_status = 'failed')    AS failed
FROM `{project}.drive_raw.file_manifest`
GROUP BY kind, fmt
""".strip()


def name_clusters_view_sql(project: str) -> str:
    """Files whose names differ only by a copy/version marker.

    Catches the near-duplicates that content hashing misses: `report.pdf` and
    `report (1).pdf` with one byte changed are two distinct contents but one
    document, and a `_v2`/`final`/`copy` family is usually a version chain worth
    collapsing by hand.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.name_clusters` AS
WITH normalised AS (
  SELECT
    file_id, name, path, size_bytes, content_hash, modified_time,
    -- Strip copy markers, version tags and trailing numbers from the stem.
    TRIM(REGEXP_REPLACE(
      REGEXP_REPLACE(
        LOWER(REGEXP_REPLACE(name, r'\\.[^.]+$', '')),
        r'\\s*\\(\\d+\\)|[ _-]+(copy|final|latest|v\\d+|new|old)$', ''
      ), r'[^a-z0-9]+', ' '
    )) AS stem
  FROM `{project}.drive_raw.file_manifest`
  WHERE kind IN ('document', 'tabular')
)
SELECT
  stem,
  COUNT(*)                     AS variants,
  COUNT(DISTINCT content_hash) AS distinct_contents,
  SUM(size_bytes)              AS bytes,
  MIN(DATE(modified_time))     AS first_modified,
  MAX(DATE(modified_time))     AS last_modified,
  ARRAY_AGG(STRUCT(name, path, size_bytes) ORDER BY path LIMIT 20) AS files
FROM normalised
WHERE stem != ''
GROUP BY stem
HAVING variants > 1
""".strip()


def term_index_sql(project: str) -> str:
    """Rare-term index over document text. No model involved.

    Terms are lowercased alphanumeric tokens of 4+ characters. Document
    frequency is computed so boilerplate can be excluded: a term present in a
    fifth of all documents links everything to everything and carries no signal.
    """
    return f"""
CREATE OR REPLACE TABLE `{project}.{INSIGHTS_DATASET}.doc_terms`
CLUSTER BY term
AS
WITH docs AS (
  SELECT file_id, name, path, content
  FROM `{project}.drive_documents.documents`
  WHERE content IS NOT NULL AND LENGTH(content) >= {MIN_DOC_CHARS}
),
total AS (SELECT COUNT(*) AS n FROM docs),
tokens AS (
  SELECT
    d.file_id, d.name, d.path,
    token
  FROM docs d,
  UNNEST(REGEXP_EXTRACT_ALL(LOWER(d.content), r'[a-z][a-z0-9]{{3,}}')) AS token
),
counted AS (
  SELECT
    file_id, name, path, token AS term,
    COUNT(*) AS term_count
  FROM tokens
  GROUP BY file_id, name, path, term
),
doc_freq AS (
  SELECT term, COUNT(DISTINCT file_id) AS docs_with_term
  FROM counted GROUP BY term
)
SELECT
  c.file_id, c.name, c.path, c.term, c.term_count,
  f.docs_with_term,
  f.docs_with_term / (SELECT n FROM total) AS doc_fraction
FROM counted c
JOIN doc_freq f USING (term)
WHERE f.docs_with_term BETWEEN 2 AND CAST(
        (SELECT n FROM total) * {MAX_DOC_FRACTION} AS INT64)
  AND LENGTH(c.term) >= 4
""".strip()


def term_bridges_view_sql(project: str, min_shared: int = 4) -> str:
    """Document pairs joined by shared rare terms -- crossing without vectors.

    Scored by summed inverse document frequency, so a pair sharing one very rare
    term (a case number, an unusual surname) outranks a pair sharing several
    merely uncommon ones.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.term_bridges` AS
WITH pairs AS (
  SELECT
    a.file_id AS a_file_id, b.file_id AS b_file_id,
    ANY_VALUE(a.name) AS a_name, ANY_VALUE(b.name) AS b_name,
    ANY_VALUE(a.path) AS a_path, ANY_VALUE(b.path) AS b_path,
    COUNT(*) AS shared_terms,
    -- Inverse document frequency: rarer shared terms are worth more.
    ROUND(SUM(1.0 / a.docs_with_term), 3) AS score,
    ARRAY_AGG(a.term ORDER BY a.docs_with_term LIMIT 12) AS rarest_shared
  FROM `{project}.{INSIGHTS_DATASET}.doc_terms` a
  JOIN `{project}.{INSIGHTS_DATASET}.doc_terms` b
    ON a.term = b.term AND a.file_id < b.file_id
  GROUP BY a_file_id, b_file_id
)
SELECT
  a_name, b_name, a_path, b_path, shared_terms, score, rarest_shared,
  REGEXP_EXTRACT(a_path, r'^([^/]+)') != REGEXP_EXTRACT(b_path, r'^([^/]+)')
    AS crosses_folder
FROM pairs
WHERE shared_terms >= {min_shared}
""".strip()


def distinctive_terms_view_sql(project: str) -> str:
    """What each document is *about*, by its rarest frequent terms.

    A crude but effective topic label, and a fast way to scan a corpus you have
    not read.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.distinctive_terms` AS
SELECT
  name, path,
  ARRAY_AGG(term ORDER BY term_count / docs_with_term DESC LIMIT 12) AS terms
FROM `{project}.{INSIGHTS_DATASET}.doc_terms`
GROUP BY name, path
""".strip()


def timeline_view_sql(project: str) -> str:
    """Corpus activity over time, from file dates alone."""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.file_timeline` AS
SELECT
  DATE_TRUNC(DATE(modified_time), MONTH) AS month,
  IFNULL(REGEXP_EXTRACT(path, r'^([^/]+)'), '(root)') AS top_folder,
  kind,
  COUNT(*)        AS files,
  SUM(size_bytes) AS bytes
FROM `{project}.drive_raw.file_manifest`
WHERE modified_time IS NOT NULL
GROUP BY month, top_folder, kind
""".strip()


def headline_sql(project: str) -> str:
    """One row of the numbers worth seeing first."""
    return f"""
SELECT
  COUNT(*)                                        AS files,
  COUNT(DISTINCT content_hash)                    AS distinct_contents,
  COUNTIF(ingest_status = 'duplicate')            AS duplicate_files,
  ROUND(SUM(IF(ingest_status = 'duplicate', size_bytes, 0)) / 1073741824, 2)
                                                  AS duplicate_gib,
  ROUND(SUM(size_bytes) / 1073741824, 2)          AS total_gib,
  COUNTIF(kind = 'document')                      AS documents,
  COUNTIF(kind = 'tabular')                       AS tabular,
  COUNTIF(kind = 'media')                         AS media,
  COUNTIF(ingest_status = 'excluded')             AS excluded,
  COUNTIF(ingest_status = 'failed')               AS failed,
  MIN(DATE(modified_time))                        AS earliest,
  MAX(DATE(modified_time))                        AS latest
FROM `{project}.drive_raw.file_manifest`
""".strip()


def all_views(project: str) -> list[tuple[str, str]]:
    """Views in dependency order. `doc_terms` is a table others read."""
    return [
        ("census", census_view_sql(project)),
        ("duplicates", duplicates_view_sql(project)),
        ("storage", storage_view_sql(project)),
        ("name_clusters", name_clusters_view_sql(project)),
        ("file_timeline", timeline_view_sql(project)),
        ("doc_terms", term_index_sql(project)),
        ("term_bridges", term_bridges_view_sql(project)),
        ("distinctive_terms", distinctive_terms_view_sql(project)),
    ]
