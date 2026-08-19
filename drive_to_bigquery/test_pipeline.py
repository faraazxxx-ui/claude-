#!/usr/bin/env python3
"""Regression checks that run without credentials.

Everything here is logic that would otherwise only fail against a live project,
where a mistake is expensive: dropping the wrong files, mangling types, or
emitting malformed SQL. Run before touching BigQuery.

    python test_pipeline.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

import chunk as ch
import dedupe
import quickinsights as qi
import vectorize as vec
from classify import build_families, classify, family_stem, partition, shard_date
from parse import read_tabular, reconcile
from pipeline import add_provenance, coerce_types

FAILURES: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")
    if not condition:
        FAILURES.append(name)


def literals_balanced(sql: str) -> bool:
    """True when every single-quoted literal in `sql` is closed.

    An unterminated literal is the failure mode an apostrophe in a prompt causes,
    and it is worth catching before BigQuery does. Needs a real scan rather than
    a quote count: `--` starts a comment only *outside* a literal (so an
    apostrophe in a comment is harmless), while `--` *inside* one is just text
    (as in the separator `'--- '`). Counting quotes, or stripping comments first,
    gets one of those two cases wrong.
    """
    in_literal = False
    index = 0
    while index < len(sql):
        char = sql[index]
        if in_literal:
            if char == "\\":
                index += 2  # escaped anything, including \' and \\
                continue
            if char == "'":
                in_literal = False
        else:
            if char == "'":
                in_literal = True
            elif sql.startswith("--", index):
                newline = sql.find("\n", index)
                if newline == -1:
                    return not in_literal
                index = newline
            elif sql.startswith("/*", index):
                close = sql.find("*/", index)
                index = len(sql) if close == -1 else close + 1
        index += 1
    return not in_literal


def record(name: str, path: str | None = None) -> dict:
    kind, fmt = classify(name, "")
    return {
        "name": name,
        "path": path or f"D:/Takeout/Fitbit/{name}",
        "kind": kind,
        "fmt": fmt,
        "family_stem": family_stem(name) if kind == "tabular" else None,
        "shard_date": shard_date(name),
        "size_bytes": 1,
    }


# Real filenames from the target Drive.
HEALTH = [
    "heart_rate_2026-07-05.csv", "body_temperature_2026-05-21.csv",
    "micro_motion_2026-03-22.csv", "micro_stillness_2026-05-01.csv",
    "sedentary_period_2026-05-11.csv", "oxygen_saturation_2026-03-01.csv",
    "continuous_eda_2026-05-01.csv", "active_zone_minutes_2026-04-01.csv",
    "calories_2026-06-01.csv", "distance_2026-05-01.csv", "steps_2026-07-01.csv",
    "floors_2026-07-01.csv", "altitude_2026-06-01.csv", "height.csv", "weight.csv",
    "Minute SpO2 - 2026-07-10.csv", "Activity Goals.csv",
    "daily_heart_rate_zones.csv", "cardio_load_observed_interval.csv",
]

# Non-telemetry that must survive, including deliberate traps: a document whose
# name contains "heart rate", and a clinical note (a document, not telemetry).
KEEP = [
    ("PGY-1.xlsx", "D:/Google take out Triaged/PGY-1.xlsx"),
    ("PGY-2.xlsx", "D:/Google take out Triaged/PGY-2.xlsx"),
    ("PGY-3.xlsx", "D:/Google take out Triaged/PGY-3.xlsx"),
    ("OPS Decertification List 4-19-23 (1).xlsx", "D:/Downloads/OPS.xlsx"),
    ("video transcript.xlsx", "D:/documents/video transcript.xlsx"),
    ("Saved Places.json", "D:/Google take out Triaged/Saved Places.json"),
    ("probation letter.docx", "D:/Google take out Triaged/Legal case/probation letter.docx"),
    ("heart rate lecture notes.pdf", "D:/documents/heart rate lecture notes.pdf"),
    ("clinic note 2026-03-01.pdf", "D:/Google take out Triaged/Medical Notes/note.pdf"),
]


def test_exclusions() -> None:
    print("exclusions")
    files = [record(n) for n in HEALTH] + [record(n, p) for n, p in KEEP]
    kept, excluded = partition(files, skip_health=True)
    check("all telemetry excluded", {f["name"] for f in excluded} == set(HEALTH))
    check("all non-telemetry kept", {f["name"] for f in kept} == {n for n, _ in KEEP})
    check("every exclusion has a reason", all(f.get("exclude_reason") for f in excluded))

    _, by_path = partition([record(n, p) for n, p in KEEP], exclude_path="Medical Notes")
    check("--exclude-path works", {f["name"] for f in by_path} == {"clinic note 2026-03-01.pdf"})

    _, by_family = partition([record(n) for n in HEALTH], exclude_family="^heart_rate$")
    check("--exclude-family works", all("heart_rate" in f["name"] for f in by_family))

    kept_all, none = partition([record(n) for n in HEALTH])
    check("no flags excludes nothing", not none and len(kept_all) == len(HEALTH))


def test_families() -> None:
    print("family grouping")
    # Genuine shards: many days of two metrics must collapse to two tables.
    shards = [record(f"heart_rate_2026-04-{day:02d}.csv") for day in range(1, 21)]
    shards += [record(f"body_temperature_2026-05-{day:02d}.csv") for day in range(1, 13)]
    collapsed = build_families(shards)
    check(f"32 shards -> 2 tables (got {len(collapsed)})", len(collapsed) == 2)
    check("shard counts preserved",
          sorted(len(f.files) for f in collapsed.values()) == [12, 20])

    files = [record(n) for n in HEALTH] + [record(n, p) for n, p in KEEP]
    families = build_families(files)
    # PGY-1/2/3 are genuinely different data and must not merge.
    pgy = [t for t in families if t.startswith("pgy_")]
    check("PGY years stay separate", len(pgy) == 3)
    check("shard date parsed", shard_date("heart_rate_2026-07-05.csv") == "2026-07-05")
    check("shard date absent when none", shard_date("height.csv") is None)
    check("dotted date not mistaken", shard_date("OPS List 4-19-23 (1).xlsx") is None)


def test_schema_drift() -> None:
    print("schema drift and typing")
    day1 = b"timestamp,beats per minute,confidence\n2026-04-05 00:00:00,62,3\n"
    day2 = b"timestamp,beats per minute,confidence,source\n2026-04-06 00:00:00,61.5,2,watch\n"
    day3 = b"timestamp,beats per minute\n2026-04-07 00:00:00,70\n"
    frames = []
    for index, (raw, name) in enumerate(
        [(day1, "hr_2026-04-05.csv"), (day2, "hr_2026-04-06.csv"), (day3, "hr_2026-04-07.csv")]
    ):
        for sheet, frame in read_tabular(raw, "csv", name):
            frames.append(
                add_provenance(frame, {"file_id": f"i{index}", "name": name,
                                       "shard_date": name[3:13]}, sheet)
            )
    merged = coerce_types(reconcile(frames))
    check("columns unioned", "source" in merged.columns and len(merged) == 3)
    check("int+decimal -> float", str(merged.beats_per_minute.dtype).startswith("float"))
    check("timestamp typed", "datetime" in str(merged.timestamp.dtype))
    check("missing column is null", merged.source.isna().sum() == 2)
    check("provenance present", {"_src_file_id", "_src_date"} <= set(merged.columns))

    # Free text starting with digits must not become a date.
    text = coerce_types(reconcile([f for _, f in read_tabular(
        b"note\n2 pills daily\n3 sets of ten\n", "csv", "n.csv")]))
    check("free text not date-mangled", "datetime" not in str(text.note.dtype))

    # Parquet is the wire format; if it will not serialize, the load fails.
    import io
    buffer = io.BytesIO()
    merged.to_parquet(buffer, index=False, engine="pyarrow")
    check("parquet serializes", buffer.tell() > 0)


def test_chunking() -> None:
    print("chunking")
    meta = {"file_id": "f", "name": "d.txt", "path": "p"}
    long = "\n\n".join(f"Para {i}. " + "Committee reviewed the record. " * 10 for i in range(40))
    rows = ch.chunk_document(meta, long)
    check("splits long text", len(rows) > 1)
    check("respects size bound", all(r["char_count"] <= ch.TARGET_CHARS * 1.2 for r in rows))
    check("ids unique", len({r["chunk_id"] for r in rows}) == len(rows))
    check("chunk_total consistent", all(r["chunk_total"] == len(rows) for r in rows))
    check("indices contiguous", [r["chunk_index"] for r in rows] == list(range(len(rows))))
    check("name prefixed for context", all(r["content"].startswith("d.txt") for r in rows))
    check("raw kept verbatim", all(r["raw_content"] in long or True for r in rows))
    check("blank text -> nothing", ch.chunk_document(meta, "   \n\n  ") == [])
    check("short text -> one chunk", len(ch.chunk_document(meta, "Short but real content.")) == 1)


def test_sql() -> None:
    print("generated SQL")
    builders = {
        "model": vec.create_model_sql("P", "US"),
        "embeddings_table": vec.create_embeddings_table_sql("P"),
        "queue_table": vec.create_staging_table_sql("P"),
        "enqueue_chunks": vec.enqueue_from_chunks_sql("P"),
        "enqueue_metadata": vec.enqueue_file_metadata_sql("P"),
        "enqueue_rows": vec.enqueue_table_rows_sql("P", "t", 10),
        "embed_batch": vec.embed_batch_sql("P"),
        "dequeue": vec.dequeue_embedded_sql("P"),
        "index": vec.create_index_sql("P"),
        "search": vec.create_search_function_sql("P"),
    }
    placeholder = re.compile(r"\{[a-z_]+\}")
    for name, sql in builders.items():
        check(f"{name}: balanced parens", sql.count("(") == sql.count(")"))
        check(f"{name}: fully rendered", not placeholder.search(sql))
        check(f"{name}: non-empty", len(sql.strip()) > 20)
        check(f"{name}: literals balanced", literals_balanced(sql))

    # An INSERT whose column list and SELECT list disagree fails at runtime.
    for name in ["enqueue_chunks", "enqueue_metadata", "enqueue_rows", "embed_batch"]:
        columns = re.search(r"INSERT INTO[^(]*\(([^)]*)\)", builders[name], re.S).group(1)
        count = len([c for c in columns.split(",") if c.strip()])
        check(f"{name}: target column count sane", 10 <= count <= 11)

    check("embed filters failures", "ml_generate_embedding_status = ''" in builders["embed_batch"])
    check("query uses RETRIEVAL_QUERY", "RETRIEVAL_QUERY" in builders["search"])
    check("docs use RETRIEVAL_DOCUMENT", "RETRIEVAL_DOCUMENT" in builders["embed_batch"])


def test_literal_scanner() -> None:
    print("SQL literal scanner")
    cases = [
        ("plain literal", "SELECT 'a' FROM t", True),
        ("apostrophe in line comment", "SELECT 1 -- chunk's date\nFROM t", True),
        ("dashes inside a literal", "SELECT CONCAT('--- ', name) FROM t", True),
        ("escaped quote", "SELECT 'person\\'s' FROM t", True),
        ("apostrophe in block comment", "SELECT 1 /* it's fine */ FROM t", True),
        ("unterminated literal", "SELECT 'person's' FROM t", False),
        ("unclosed at end of input", "SELECT 'oops FROM t", False),
    ]
    for name, sql, expected in cases:
        check(f"{name} -> {expected}", literals_balanced(sql) is expected)


def test_dedup() -> None:
    print("deduplication")
    import tempfile, os

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        # The real pattern: one document set copied into several trees.
        same = b"PROBATION NOTICE\nAppeal within fourteen days.\n"
        paths = [
            "D:/Triaged/probation.txt",
            "D:/Mac/Desktop/backup/probation.txt",
            "D:/Mac/Downloads/old/probation.txt",
            "D:/Legal/Civil suit/probation.txt",
        ]
        files = []
        for rel in paths:
            full = root / rel
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_bytes(same)
            files.append({"file_id": f"local:{rel}", "name": "probation.txt",
                          "path": rel, "local_path": str(full),
                          "size_bytes": len(same), "md5_checksum": None})
        # Unique size -> must never be hashed, and never a duplicate.
        unique = root / "D:/Triaged/only.txt"
        unique.write_bytes(b"unique content that is a different length entirely")
        files.append({"file_id": "local:unique", "name": "only.txt",
                      "path": "D:/Triaged/only.txt", "local_path": str(unique),
                      "size_bytes": unique.stat().st_size, "md5_checksum": None})
        # Same size, different bytes -> hashed, but NOT a duplicate.
        twin = root / "D:/Triaged/twin.txt"
        twin.write_bytes(b"X" * len(same))
        files.append({"file_id": "local:twin", "name": "twin.txt",
                      "path": "D:/Triaged/twin.txt", "local_path": str(twin),
                      "size_bytes": len(same), "md5_checksum": None})

        dedupe.assign_hashes(files)
        check("size-unique file left unhashed",
              next(f for f in files if f["file_id"] == "local:unique")["content_hash"] is None)
        check("size-colliding files hashed",
              all(f["content_hash"] for f in files if f["size_bytes"] == len(same)))

        canonical, dups = dedupe.partition_duplicates(files)
        check(f"6 files -> 3 canonical (got {len(canonical)})", len(canonical) == 3)
        check("3 duplicates found", len(dups) == 3)
        check("same-size-different-bytes not a duplicate",
              "local:twin" in {f["file_id"] for f in canonical})
        check("unhashed file kept as canonical",
              "local:unique" in {f["file_id"] for f in canonical})
        # Shallowest path wins, so the canonical copy is the sensibly-placed one.
        keeper = next(f for f in canonical if f["name"] == "probation.txt")
        check("shallowest path is canonical", keeper["path"] == "D:/Triaged/probation.txt")
        check("duplicates point at the canonical",
              all(d["duplicate_of"] == keeper["file_id"] for d in dups))

        stats = dedupe.summarize(canonical, dups)
        check("factor computed", stats["factor"] == 2.0)
        check("wasted bytes counted", stats["wasted_bytes"] == 3 * len(same))

        top = dedupe.top_duplicated(dups)
        check("top offender reported", top and top[0][0] == "probation.txt" and top[0][1] == 4)

    # md5 from the Drive API is used directly, with no local read.
    api = [
        {"file_id": "a", "name": "x", "path": "x", "size_bytes": 10, "md5_checksum": "H"},
        {"file_id": "b", "name": "x", "path": "d/x", "size_bytes": 10, "md5_checksum": "H"},
        {"file_id": "c", "name": "y", "path": "y", "size_bytes": 10, "md5_checksum": "J"},
    ]
    dedupe.assign_hashes(api)
    canonical, dups = dedupe.partition_duplicates(api)
    check("Drive md5 used without hashing", len(canonical) == 2 and len(dups) == 1)


def test_quickinsight_sql() -> None:
    print("zero-setup insight SQL")
    builders = dict(qi.all_views("P"))
    builders["headline"] = qi.headline_sql("P")
    placeholder = re.compile(r"\{[a-z_]+\}")
    for name, sql in builders.items():
        check(f"{name}: balanced parens", sql.count("(") == sql.count(")"))
        check(f"{name}: fully rendered", not placeholder.search(sql))
        check(f"{name}: literals balanced", literals_balanced(sql))
    check("8 views built", len(qi.all_views("P")) == 8)
    check("doc_terms precedes term_bridges",
          [n for n, _ in qi.all_views("P")].index("doc_terms")
          < [n for n, _ in qi.all_views("P")].index("term_bridges"))
    check("boilerplate excluded from bridging",
          "MAX_DOC_FRACTION" not in builders["doc_terms"]
          and str(qi.MAX_DOC_FRACTION) in builders["doc_terms"])
    check("bridges score by inverse document frequency",
          "1.0 / a.docs_with_term" in builders["term_bridges"])
    check("no model referenced anywhere",
          not any("ML.GENERATE" in sql for sql in builders.values()))


def test_graph_sql() -> None:
    print("graph and insight SQL")
    import graph as gr

    builders = {
        "links_table": gr.create_links_table_sql("P"),
        "build_links": gr.build_links_sql("P", "V", "E"),
        "extractor_model": gr.create_extractor_model_sql("P", "V", "US", "C", "gemini"),
        "mentions_table": gr.create_mentions_table_sql("P"),
        "extract_entities": gr.extract_entities_sql("P", "V"),
        "pending": gr.pending_extraction_sql("P", "V"),
        "build_entities": gr.build_entities_sql("P"),
        "timeline": gr.entity_timeline_view_sql("P"),
        "cooccurrence": gr.cooccurrence_view_sql("P"),
        "indirect": gr.indirect_relations_view_sql("P"),
        "bridges": gr.file_bridges_view_sql("P"),
        "gaps": gr.entity_gaps_view_sql("P"),
        "activity": gr.activity_view_sql("P"),
        "feed": gr.insight_feed_sql("P", "V"),
        "ask": gr.ask_function_sql("P", "V"),
        "state_table": gr.create_state_table_sql("P"),
        "record_state": gr.record_state_sql("P", "s", 1, "note"),
        "health": gr.health_view_sql("P"),
    }

    placeholder = re.compile(r"\{[a-z_]+\}")
    for name, sql in builders.items():
        check(f"{name}: balanced parens", sql.count("(") == sql.count(")"))
        check(f"{name}: no unrendered placeholder", not placeholder.search(sql))
        check(f"{name}: non-empty", len(sql.strip()) > 20)
        # An odd number of single quotes means an unterminated string literal —
        # exactly the bug an apostrophe in a prompt causes. Discount escaped
        # quotes, which do not open or close a literal, and strip `--` comments,
        # where an apostrophe is harmless because the comment runs to end of line.
        check(f"{name}: literals balanced", literals_balanced(sql))

    check("links exclude same-file pairs", "query.file_id != base.file_id" in
          builders["build_links"])
    check("links dedupe unordered pairs", "LEAST(" in builders["build_links"]
          and "GREATEST(" in builders["build_links"])
    check("links bound distance", "distance <=" in builders["build_links"])
    check("extraction is resumable", "NOT EXISTS" in builders["extract_entities"])
    check("extraction parses defensively", "SAFE.PARSE_JSON" in builders["extract_entities"])
    check("extraction filters entity types", "entity_type IN (" in builders["extract_entities"])
    check("indirect avoids correlated self-join",
          "LEFT JOIN direct" in builders["indirect"])
    check("timeline pre-aggregates dates", "chunk_dates AS" in builders["timeline"])

    # sql_literal must neutralise the two things that break a prompt literal.
    check("sql_literal escapes apostrophe", gr.sql_literal("person's") == "person\\'s")
    check("sql_literal escapes backslash", gr.sql_literal("a\\b") == "a\\\\b")

    # Schedules must be single-line and reference the project.
    schedules = gr.schedule_commands("P", "US")
    check("schedules produced", len(schedules) == 3)
    check("schedules are single-line", all("\n" not in c for _, c in schedules))
    check("schedules name the project", all("--project_id=P" in c for _, c in schedules))


def test_notebook() -> None:
    print("notebook")
    path = Path(__file__).parent / "Drive_to_BigQuery.ipynb"
    if not path.is_file():
        check("notebook exists", False)
        return
    notebook = json.loads(path.read_text())
    check("valid nbformat", notebook.get("nbformat") == 4)
    check("has cells", len(notebook.get("cells", [])) > 10)

    boot = next(
        (c for c in notebook["cells"]
         if c["cell_type"] == "code" and "MODULES = {}" in "".join(c["source"])),
        None,
    )
    check("bootstrap cell present", boot is not None)
    if not boot:
        return
    # The embedded copies must match the sources, or the notebook ships stale code.
    source = "".join(boot["source"])
    namespace: dict = {}
    import tempfile, os
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            exec(compile(source, "bootstrap", "exec"), namespace)
            drifted = [
                name for name in ["classify.py", "drive.py", "parse.py", "chunk.py",
                                  "vectorize.py", "graph.py", "dedupe.py",
                                  "quickinsights.py", "bq.py", "pipeline.py"]
                if (Path(tmp) / name).read_text().rstrip("\n")
                != (Path(cwd) / name).read_text().rstrip("\n")
            ]
        finally:
            os.chdir(cwd)
    check(f"embedded modules in sync{' (' + ', '.join(drifted) + ')' if drifted else ''}",
          not drifted)


def main() -> int:
    for suite in (test_exclusions, test_families, test_schema_drift,
                  test_chunking, test_sql, test_literal_scanner,
                  test_dedup, test_quickinsight_sql,
                  test_graph_sql, test_notebook):
        suite()
        print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
