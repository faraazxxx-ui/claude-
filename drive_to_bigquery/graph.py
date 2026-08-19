"""Cross the data against itself, then cross the crossings.

Vectors alone give you similarity search: ask a question, get passages. That is
still a *static* index -- it only answers what you thought to ask.

This layer makes the corpus reason about itself, in two passes:

  Pass 1 (crossing).  Every chunk is searched against every other chunk and the
      nearest neighbours in OTHER files are recorded as links. A passage in a
      probation letter and a row in a residency evaluation that talk about the
      same thing become an explicit edge, with no query typed by anyone.

  Pass 2 (crossing the crossings).  Entities are extracted from each chunk, then
      pushed *through* those edges. Two people who never appear in the same file
      but are each central to files that link to one another are surfaced as
      related. Timelines assemble across sources. Bridges -- single links that
      join otherwise separate clusters -- are ranked, because in practice a
      bridge is where the interesting thing is.

Everything is a view or an incremental table refreshed on a schedule, so the
picture moves as the Drive moves rather than being a snapshot.

The LLM-dependent statements are deliberately confined to `extract_entities_sql`
and `insight_feed_sql`. BigQuery's generative SQL surface moves faster than the
rest of it, so if a signature has drifted the fix is in one place.
"""

from __future__ import annotations

GRAPH_DATASET = "drive_graph"
INSIGHTS_DATASET = "drive_insights"

MENTIONS_TABLE = "entity_mentions"
ENTITIES_TABLE = "entities"
LINKS_TABLE = "cross_links"
EXTRACTOR_MODEL = "extractor"
STATE_TABLE = "pipeline_state"

# Gemini endpoint for extraction and summarisation. Rotates faster than
# anything else here; override with --text-model.
DEFAULT_TEXT_ENDPOINT = "gemini-2.5-flash"

# Neighbours recorded per chunk. Beyond ~8 the tail is noise and the link table
# grows quadratically for nothing.
NEIGHBOURS_PER_CHUNK = 8

# Cosine distance above which a "link" is not really a link. Tuned
# conservatively: 0.35 keeps genuine topical overlap and drops boilerplate.
MAX_LINK_DISTANCE = 0.35

ENTITY_TYPES = ("PERSON", "ORG", "DATE", "CASE_NUMBER", "LOCATION", "MEDICAL", "MONEY", "TOPIC")


def sql_literal(text: str) -> str:
    """Escape text for a single-quoted BigQuery string literal.

    Prompts are prose and prose contains apostrophes; one unescaped `'` in a
    prompt silently truncates the SQL statement into something that either fails
    or, worse, parses as something else.
    """
    return text.replace("\\", "\\\\").replace("'", "\\'")


# --------------------------------------------------------------- pass 1: links


def create_links_table_sql(project: str) -> str:
    return f"""
CREATE TABLE IF NOT EXISTS `{project}.{GRAPH_DATASET}.{LINKS_TABLE}` (
  link_id      STRING NOT NULL,
  a_vector_id  STRING,
  b_vector_id  STRING,
  a_file_id    STRING,
  b_file_id    STRING,
  a_name       STRING,
  b_name       STRING,
  a_path       STRING,
  b_path       STRING,
  a_kind       STRING,
  b_kind       STRING,
  a_excerpt    STRING,
  b_excerpt    STRING,
  distance     FLOAT64,
  linked_at    TIMESTAMP
)
PARTITION BY DATE(linked_at)
CLUSTER BY a_file_id, b_file_id
""".strip()


def build_links_sql(
    project: str,
    vectors_dataset: str,
    embeddings_table: str,
    neighbours: int = NEIGHBOURS_PER_CHUNK,
    max_distance: float = MAX_LINK_DISTANCE,
) -> str:
    """Search the embedding table against itself and keep cross-file neighbours.

    Two constraints make this useful rather than noise:

    * `a_file_id != b_file_id` -- neighbours within one document are just the
      document being locally coherent, which we already knew.
    * an ordered pair guard, so A-B and B-A collapse to one edge.
    """
    return f"""
CREATE OR REPLACE TABLE `{project}.{GRAPH_DATASET}.{LINKS_TABLE}`
PARTITION BY DATE(linked_at)
CLUSTER BY a_file_id, b_file_id
AS
WITH neighbours AS (
  SELECT
    query.vector_id   AS a_vector_id,
    base.vector_id    AS b_vector_id,
    query.file_id     AS a_file_id,
    base.file_id      AS b_file_id,
    query.name        AS a_name,
    base.name         AS b_name,
    query.path        AS a_path,
    base.path         AS b_path,
    query.source_kind AS a_kind,
    base.source_kind  AS b_kind,
    SUBSTR(query.content, 1, 400) AS a_excerpt,
    SUBSTR(base.content,  1, 400) AS b_excerpt,
    distance
  FROM VECTOR_SEARCH(
    TABLE `{project}.{vectors_dataset}.{embeddings_table}`, 'embedding',
    TABLE `{project}.{vectors_dataset}.{embeddings_table}`,
    query_column_to_search => 'embedding',
    top_k => {neighbours + 1},
    distance_type => 'COSINE'
  )
  WHERE query.file_id != base.file_id
    AND distance <= {max_distance}
)
SELECT
  TO_HEX(MD5(CONCAT(
    LEAST(a_vector_id, b_vector_id), '|', GREATEST(a_vector_id, b_vector_id)
  ))) AS link_id,
  ANY_VALUE(a_vector_id) AS a_vector_id,
  ANY_VALUE(b_vector_id) AS b_vector_id,
  ANY_VALUE(a_file_id)   AS a_file_id,
  ANY_VALUE(b_file_id)   AS b_file_id,
  ANY_VALUE(a_name)      AS a_name,
  ANY_VALUE(b_name)      AS b_name,
  ANY_VALUE(a_path)      AS a_path,
  ANY_VALUE(b_path)      AS b_path,
  ANY_VALUE(a_kind)      AS a_kind,
  ANY_VALUE(b_kind)      AS b_kind,
  ANY_VALUE(a_excerpt)   AS a_excerpt,
  ANY_VALUE(b_excerpt)   AS b_excerpt,
  MIN(distance)          AS distance,
  CURRENT_TIMESTAMP()    AS linked_at
FROM neighbours
GROUP BY link_id
""".strip()


# ------------------------------------------------------------ pass 2: entities


def create_extractor_model_sql(
    project: str, vectors_dataset: str, location: str, connection: str, endpoint: str
) -> str:
    return f"""
CREATE OR REPLACE MODEL `{project}.{vectors_dataset}.{EXTRACTOR_MODEL}`
REMOTE WITH CONNECTION `{project}.{location}.{connection}`
OPTIONS (ENDPOINT = '{endpoint}')
""".strip()


def create_mentions_table_sql(project: str) -> str:
    return f"""
CREATE TABLE IF NOT EXISTS `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` (
  mention_id   STRING NOT NULL,
  vector_id    STRING,
  file_id      STRING,
  name         STRING,
  path         STRING,
  source_kind  STRING,
  entity_text  STRING,
  entity_type  STRING,
  entity_norm  STRING,
  extracted_at TIMESTAMP
)
CLUSTER BY entity_norm, entity_type
""".strip()


def extract_entities_sql(
    project: str, vectors_dataset: str, batch_rows: int = 2000
) -> str:
    """Pull entities out of chunks with Gemini, one batch at a time.

    The prompt demands strict JSON and the result is parsed with SAFE.PARSE_JSON,
    so a malformed response yields no rows for that chunk instead of failing the
    statement. Chunks already extracted are skipped, which makes this resumable
    and cheap to re-run as new files arrive.

    NOTE: this is one of two statements using BigQuery's generative SQL surface
    and it has not been executed against a live project. If `ML.GENERATE_TEXT`
    has drifted, this function and `insight_feed_sql` are the only places to fix.
    """
    prompt = sql_literal(
        "Extract named entities from the text. Return ONLY minified JSON, with no "
        "markdown fence, shaped exactly like this: "
        '{"entities":[{"text":"","type":""}]} '
        "where type is one of " + "|".join(ENTITY_TYPES) + ". "
        "Copy the exact surface form from the text into the text field. "
        "Omit generic words, pronouns, and anything uncertain. "
        "Return at most 25 entities. Text:"
    ) + "\\n\\n"
    return f"""
INSERT INTO `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}`
  (mention_id, vector_id, file_id, name, path, source_kind,
   entity_text, entity_type, entity_norm, extracted_at)
WITH generated AS (
  SELECT
    vector_id, file_id, name, path, source_kind,
    SAFE.PARSE_JSON(
      REGEXP_REPLACE(ml_generate_text_llm_result, r'^```(?:json)?|```$', '')
    ) AS payload
  FROM ML.GENERATE_TEXT(
    MODEL `{project}.{vectors_dataset}.{EXTRACTOR_MODEL}`,
    (
      SELECT
        e.vector_id, e.file_id, e.name, e.path, e.source_kind,
        CONCAT('{prompt}', SUBSTR(e.content, 1, 6000)) AS prompt
      FROM `{project}.{vectors_dataset}.embeddings` e
      WHERE e.source_kind IN ('document_chunk', 'table_row')
        AND NOT EXISTS (
          SELECT 1 FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` m
          WHERE m.vector_id = e.vector_id
        )
      LIMIT {batch_rows}
    ),
    STRUCT(0.0 AS temperature, 1024 AS max_output_tokens,
           TRUE AS flatten_json_output)
  )
)
flattened AS (
  SELECT
    g.vector_id, g.file_id, g.name, g.path, g.source_kind,
    JSON_VALUE(entity, '$.text')        AS entity_text,
    UPPER(JSON_VALUE(entity, '$.type')) AS entity_type
  FROM generated g
  CROSS JOIN UNNEST(JSON_QUERY_ARRAY(g.payload, '$.entities')) AS entity
  WHERE g.payload IS NOT NULL
)
SELECT
  TO_HEX(MD5(CONCAT(vector_id, '|', entity_text, '|', entity_type))) AS mention_id,
  vector_id, file_id, name, path, source_kind,
  entity_text,
  entity_type,
  -- Join key: casefolded, punctuation dropped, whitespace runs collapsed, so
  -- "Dr. Rahman" and "dr rahman" resolve to the same entity.
  TRIM(REGEXP_REPLACE(LOWER(entity_text), r'[^a-z0-9]+', ' ')) AS entity_norm
  , CURRENT_TIMESTAMP() AS extracted_at
FROM flattened
WHERE entity_text IS NOT NULL
  AND LENGTH(TRIM(entity_text)) BETWEEN 2 AND 200
  AND entity_type IN ({", ".join(f"'{t}'" for t in ENTITY_TYPES)})
""".strip()


def pending_extraction_sql(project: str, vectors_dataset: str) -> str:
    return f"""
SELECT COUNT(*) AS n
FROM `{project}.{vectors_dataset}.embeddings` e
WHERE e.source_kind IN ('document_chunk', 'table_row')
  AND NOT EXISTS (
    SELECT 1 FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` m
    WHERE m.vector_id = e.vector_id
  )
""".strip()


def build_entities_sql(project: str) -> str:
    """Roll mentions up into resolved entities.

    `entity_norm` is the join key, so "Dr. Rahman" and "dr rahman" collapse. The
    most frequent surface form becomes the display name.
    """
    return f"""
CREATE OR REPLACE TABLE `{project}.{GRAPH_DATASET}.{ENTITIES_TABLE}`
CLUSTER BY entity_type, entity_norm
AS
WITH ranked_forms AS (
  SELECT
    entity_norm, entity_type, entity_text,
    COUNT(*) AS form_count,
    ROW_NUMBER() OVER (
      PARTITION BY entity_norm, entity_type ORDER BY COUNT(*) DESC, entity_text
    ) AS rn
  FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}`
  WHERE entity_norm != ''
  GROUP BY entity_norm, entity_type, entity_text
)
SELECT
  m.entity_norm,
  m.entity_type,
  ANY_VALUE(f.entity_text)          AS display_name,
  COUNT(*)                          AS mention_count,
  COUNT(DISTINCT m.file_id)         AS file_count,
  COUNT(DISTINCT m.source_kind)     AS kind_count,
  ARRAY_AGG(DISTINCT m.name IGNORE NULLS ORDER BY m.name LIMIT 25) AS files,
  CURRENT_TIMESTAMP()               AS refreshed_at
FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` m
JOIN ranked_forms f
  ON f.entity_norm = m.entity_norm AND f.entity_type = m.entity_type AND f.rn = 1
WHERE m.entity_norm != ''
GROUP BY m.entity_norm, m.entity_type
""".strip()


# ---------------------------------------------------------------- the insights


def entity_timeline_view_sql(project: str) -> str:
    """Every dated appearance of an entity, from any source.

    Dates come from three places: a shard date on the source file, a DATE-typed
    entity extracted from the same chunk, and the file's modified time as a last
    resort. Crossing an entity against time across sources is what turns a pile
    of files into a chronology.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.entity_timeline` AS
WITH
-- One date per chunk, not one row per DATE entity in it. Joining the mentions
-- table to itself unaggregated would multiply every mention by its chunk's date
-- count.
chunk_dates AS (
  SELECT vector_id, MIN(SAFE.PARSE_DATE('%Y-%m-%d', entity_text)) AS in_text_date
  FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}`
  WHERE entity_type = 'DATE'
  GROUP BY vector_id
)
SELECT
  m.entity_norm, m.entity_type, m.entity_text,
  COALESCE(
    cd.in_text_date,
    SAFE_CAST(man.shard_date AS DATE),
    DATE(man.modified_time)
  ) AS event_date,
  CASE
    WHEN cd.in_text_date IS NOT NULL  THEN 'in_text'
    WHEN man.shard_date IS NOT NULL   THEN 'filename'
    ELSE 'file_mtime'
  END AS date_source,
  m.name AS file_name, m.path, m.source_kind, m.file_id, m.vector_id
FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` m
LEFT JOIN `{project}.drive_raw.file_manifest` man ON man.file_id = m.file_id
LEFT JOIN chunk_dates cd ON cd.vector_id = m.vector_id
WHERE m.entity_type != 'DATE'
  AND COALESCE(cd.in_text_date, SAFE_CAST(man.shard_date AS DATE),
               DATE(man.modified_time)) IS NOT NULL
""".strip()


def cooccurrence_view_sql(project: str) -> str:
    """Entities that appear in the same chunk -- the direct crossing."""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.entity_cooccurrence` AS
SELECT
  a.entity_norm  AS entity_a,
  b.entity_norm  AS entity_b,
  a.entity_type  AS type_a,
  b.entity_type  AS type_b,
  COUNT(*)                        AS together_count,
  COUNT(DISTINCT a.file_id)       AS file_count,
  ARRAY_AGG(DISTINCT a.name IGNORE NULLS ORDER BY a.name LIMIT 10) AS files
FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` a
JOIN `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` b
  ON a.vector_id = b.vector_id
 AND a.entity_norm < b.entity_norm   -- one row per unordered pair
WHERE a.entity_norm != '' AND b.entity_norm != ''
GROUP BY entity_a, entity_b, type_a, type_b
HAVING together_count >= 2
""".strip()


def indirect_relations_view_sql(project: str) -> str:
    """Crossing the crossings.

    Entities that never share a chunk, but sit at either end of a semantic link
    between two different files. This is the one view that can tell you something
    no single document contains -- the relationship exists only in the geometry
    between documents.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.indirect_relations` AS
WITH bridged AS (
  SELECT
    LEAST(ma.entity_norm, mb.entity_norm)    AS entity_a,
    GREATEST(ma.entity_norm, mb.entity_norm) AS entity_b,
    ma.entity_type AS type_a,
    mb.entity_type AS type_b,
    l.a_name, l.b_name, l.distance
  FROM `{project}.{GRAPH_DATASET}.{LINKS_TABLE}` l
  JOIN `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` ma ON ma.vector_id = l.a_vector_id
  JOIN `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` mb ON mb.vector_id = l.b_vector_id
  WHERE ma.entity_norm != '' AND mb.entity_norm != ''
    AND ma.entity_norm != mb.entity_norm
),
-- Materialise the co-occurring pairs once. Doing this as a correlated NOT EXISTS
-- would re-run a mentions self-join per candidate row.
direct AS (
  SELECT DISTINCT
    LEAST(x.entity_norm, y.entity_norm)    AS entity_a,
    GREATEST(x.entity_norm, y.entity_norm) AS entity_b
  FROM `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` x
  JOIN `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` y
    ON x.vector_id = y.vector_id AND x.entity_norm != y.entity_norm
  WHERE x.entity_norm != '' AND y.entity_norm != ''
)
SELECT
  b.entity_a, b.entity_b, b.type_a, b.type_b,
  COUNT(*)          AS bridge_count,
  MIN(b.distance)   AS closest_distance,
  ARRAY_AGG(DISTINCT b.a_name IGNORE NULLS ORDER BY b.a_name LIMIT 5) AS from_files,
  ARRAY_AGG(DISTINCT b.b_name IGNORE NULLS ORDER BY b.b_name LIMIT 5) AS to_files
FROM bridged b
LEFT JOIN direct d
  ON d.entity_a = b.entity_a AND d.entity_b = b.entity_b
-- Only *indirect*: the pair must never share a chunk anywhere.
WHERE d.entity_a IS NULL
GROUP BY b.entity_a, b.entity_b, b.type_a, b.type_b
HAVING bridge_count >= 2
""".strip()


def file_bridges_view_sql(project: str) -> str:
    """File pairs joined by many links -- where two parts of the Drive meet.

    Ranked by link count and closeness. A high-scoring pair of files from
    unrelated folders is usually the most interesting thing in the corpus.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.file_bridges` AS
SELECT
  a_name, b_name,
  ANY_VALUE(a_path) AS a_path,
  ANY_VALUE(b_path) AS b_path,
  ANY_VALUE(a_kind) AS a_kind,
  ANY_VALUE(b_kind) AS b_kind,
  COUNT(*)      AS link_count,
  MIN(distance) AS closest_distance,
  AVG(distance) AS mean_distance,
  -- Different top-level folders means the link crosses a boundary in how the
  -- Drive is organised, which is where a surprise usually lives.
  REGEXP_EXTRACT(ANY_VALUE(a_path), r'^([^/]+)') !=
  REGEXP_EXTRACT(ANY_VALUE(b_path), r'^([^/]+)') AS crosses_folder,
  ARRAY_AGG(STRUCT(a_excerpt, b_excerpt, distance)
            ORDER BY distance LIMIT 3) AS examples
FROM `{project}.{GRAPH_DATASET}.{LINKS_TABLE}`
GROUP BY a_name, b_name
HAVING link_count >= 2
""".strip()


def entity_gaps_view_sql(project: str) -> str:
    """Entities that show up in one kind of source but not another.

    A person named all over your documents but absent from every spreadsheet, or
    the reverse, is either a data gap or a finding. Either way it is worth seeing.
    """
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.entity_gaps` AS
SELECT
  e.entity_norm, e.entity_type, e.display_name,
  e.mention_count, e.file_count,
  COUNTIF(m.source_kind = 'document_chunk') AS in_documents,
  COUNTIF(m.source_kind = 'table_row')      AS in_tables,
  COUNTIF(m.source_kind = 'file_metadata')  AS in_filenames,
  CASE
    WHEN COUNTIF(m.source_kind = 'table_row') = 0
     AND COUNTIF(m.source_kind = 'document_chunk') > 0 THEN 'documents_only'
    WHEN COUNTIF(m.source_kind = 'document_chunk') = 0
     AND COUNTIF(m.source_kind = 'table_row') > 0      THEN 'tables_only'
    ELSE 'both'
  END AS coverage
FROM `{project}.{GRAPH_DATASET}.{ENTITIES_TABLE}` e
JOIN `{project}.{GRAPH_DATASET}.{MENTIONS_TABLE}` m
  ON m.entity_norm = e.entity_norm AND m.entity_type = e.entity_type
GROUP BY e.entity_norm, e.entity_type, e.display_name, e.mention_count, e.file_count
""".strip()


def activity_view_sql(project: str) -> str:
    """What changed lately, across every dataset. The 'is it alive' view."""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.recent_activity` AS
SELECT
  DATE(modified_time) AS day,
  kind,
  COUNT(*)            AS files,
  SUM(size_bytes)     AS bytes,
  COUNTIF(ingest_status = 'loaded')   AS loaded,
  COUNTIF(ingest_status = 'failed')   AS failed,
  COUNTIF(ingest_status = 'excluded') AS excluded
FROM `{project}.drive_raw.file_manifest`
WHERE modified_time IS NOT NULL
GROUP BY day, kind
""".strip()


def insight_feed_sql(project: str, vectors_dataset: str, top_n: int = 40) -> str:
    """Have Gemini write up the strongest cross-file bridges in plain language.

    This is the readable end of the pipeline: rather than making you interpret
    cosine distances, each bridge gets a sentence on what the two passages share
    and whether it looks meaningful.

    NOTE: the second of the two unverified generative statements. See
    `extract_entities_sql`.
    """
    instruction = sql_literal(
        "Two passages from different files in the same Drive were matched as "
        "semantically similar. In at most two sentences, say concretely what they "
        "share, then end with the single word MEANINGFUL or COINCIDENTAL. Be "
        "blunt: most matches are coincidental boilerplate and should be called "
        "that rather than dressed up."
    )
    return f"""
CREATE OR REPLACE TABLE `{project}.{INSIGHTS_DATASET}.insight_feed`
AS
SELECT
  a_name, b_name, distance, crosses_folder,
  ml_generate_text_llm_result AS assessment,
  REGEXP_CONTAINS(UPPER(ml_generate_text_llm_result), r'MEANINGFUL') AS looks_meaningful,
  CURRENT_TIMESTAMP() AS generated_at
FROM ML.GENERATE_TEXT(
  MODEL `{project}.{vectors_dataset}.{EXTRACTOR_MODEL}`,
  (
    SELECT
      a_name, b_name, closest_distance AS distance, crosses_folder,
      CONCAT(
        '{instruction}',
        '\\n\\nFILE A (', a_name, '):\\n', examples[OFFSET(0)].a_excerpt,
        '\\n\\nFILE B (', b_name, '):\\n', examples[OFFSET(0)].b_excerpt
      ) AS prompt
    FROM `{project}.{INSIGHTS_DATASET}.file_bridges`
    WHERE ARRAY_LENGTH(examples) > 0
    ORDER BY crosses_folder DESC, link_count DESC, closest_distance
    LIMIT {top_n}
  ),
  STRUCT(0.2 AS temperature, 256 AS max_output_tokens, TRUE AS flatten_json_output)
)
""".strip()


def ask_function_sql(project: str, vectors_dataset: str) -> str:
    """Retrieval-augmented question answering over the whole Drive, in one call.

    Semantic search fetches the passages; Gemini answers from them and is told to
    cite filenames and to admit when the corpus does not contain the answer.
    """
    return f"""
CREATE OR REPLACE TABLE FUNCTION `{project}.{INSIGHTS_DATASET}.ask`(
  question STRING, passages INT64
)
AS (
  WITH hits AS (
    SELECT base.name AS name, base.content AS content, distance
    FROM VECTOR_SEARCH(
      TABLE `{project}.{vectors_dataset}.embeddings`, 'embedding',
      (
        SELECT ml_generate_embedding_result AS embedding
        FROM ML.GENERATE_EMBEDDING(
          MODEL `{project}.{vectors_dataset}.embedder`,
          (SELECT question AS content),
          STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_QUERY' AS task_type)
        )
      ),
      top_k => passages, distance_type => 'COSINE'
    )
  ),
  context AS (
    SELECT STRING_AGG(
      CONCAT('--- ', name, ' ---\\n', SUBSTR(content, 1, 2000)), '\\n\\n'
      ORDER BY distance
    ) AS body
    FROM hits
  )
  SELECT
    question,
    ml_generate_text_llm_result AS answer,
    (SELECT ARRAY_AGG(DISTINCT name) FROM hits) AS sources
  FROM ML.GENERATE_TEXT(
    MODEL `{project}.{vectors_dataset}.{EXTRACTOR_MODEL}`,
    (
      SELECT CONCAT(
        'Answer the question using only the excerpts below. Cite the filenames ',
        'you relied on. If the excerpts do not contain the answer, say so ',
        'plainly rather than guessing.\\n\\nQUESTION: ', question,
        '\\n\\nEXCERPTS:\\n', body
      ) AS prompt
      FROM context
    ),
    STRUCT(0.2 AS temperature, 1024 AS max_output_tokens, TRUE AS flatten_json_output)
  )
);
""".strip()


# -------------------------------------------------------------------- keep it live


def create_state_table_sql(project: str) -> str:
    """Watermarks, so refreshes do incremental work instead of full rebuilds."""
    return f"""
CREATE TABLE IF NOT EXISTS `{project}.{GRAPH_DATASET}.{STATE_TABLE}` (
  stage       STRING NOT NULL,
  watermark   TIMESTAMP,
  rows_seen   INT64,
  note        STRING,
  updated_at  TIMESTAMP
)
""".strip()


def record_state_sql(project: str, stage: str, rows: int, note: str = "") -> str:
    safe_note = note.replace("'", "''")
    return f"""
MERGE `{project}.{GRAPH_DATASET}.{STATE_TABLE}` T
USING (SELECT '{stage}' AS stage) S
ON T.stage = S.stage
WHEN MATCHED THEN UPDATE SET
  watermark = CURRENT_TIMESTAMP(), rows_seen = {rows},
  note = '{safe_note}', updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT
  (stage, watermark, rows_seen, note, updated_at)
  VALUES ('{stage}', CURRENT_TIMESTAMP(), {rows}, '{safe_note}', CURRENT_TIMESTAMP())
""".strip()


def health_view_sql(project: str) -> str:
    """One view answering 'is this thing actually current?'"""
    return f"""
CREATE OR REPLACE VIEW `{project}.{INSIGHTS_DATASET}.pipeline_health` AS
SELECT
  stage,
  watermark            AS last_run,
  rows_seen,
  note,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), watermark, HOUR) AS hours_since,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), watermark, HOUR) > 48 AS stale
FROM `{project}.{GRAPH_DATASET}.{STATE_TABLE}`
""".strip()


def schedule_commands(project: str, location: str) -> list[tuple[str, str]]:
    """`bq query --schedule` commands that keep the derived layer refreshing.

    The ingest step still has to run somewhere with Drive access; everything
    downstream of the vector table is pure SQL and BigQuery can drive it on a
    timer with no machine of yours involved.
    """
    def cmd(name: str, schedule: str, sql: str) -> tuple[str, str]:
        one_line = " ".join(sql.split())
        return (
            name,
            f"bq query --use_legacy_sql=false --project_id={project} "
            f"--location={location} --schedule='{schedule}' "
            f"--display_name='drive:{name}' "
            f'"{one_line}"',
        )

    return [
        cmd("links", "every 24 hours", build_links_sql(project, "drive_vectors", "embeddings")),
        cmd("entities", "every 24 hours", build_entities_sql(project)),
        cmd("insight_feed", "every 24 hours", insight_feed_sql(project, "drive_vectors")),
    ]
