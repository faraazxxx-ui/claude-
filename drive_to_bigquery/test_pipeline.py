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
import vectorize as vec
from classify import build_families, classify, family_stem, partition, shard_date
from parse import read_tabular, reconcile
from pipeline import add_provenance, coerce_types

FAILURES: list[str] = []


def check(name: str, condition: bool) -> None:
    print(f"  {'PASS' if condition else 'FAIL'}  {name}")
    if not condition:
        FAILURES.append(name)


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
    for name, sql in builders.items():
        check(f"{name}: balanced parens", sql.count("(") == sql.count(")"))
        check(f"{name}: fully rendered", "{" not in sql and "}" not in sql)
        check(f"{name}: non-empty", len(sql.strip()) > 20)

    # An INSERT whose column list and SELECT list disagree fails at runtime.
    for name in ["enqueue_chunks", "enqueue_metadata", "enqueue_rows", "embed_batch"]:
        columns = re.search(r"INSERT INTO[^(]*\(([^)]*)\)", builders[name], re.S).group(1)
        count = len([c for c in columns.split(",") if c.strip()])
        check(f"{name}: target column count sane", 10 <= count <= 11)

    check("embed filters failures", "ml_generate_embedding_status = ''" in builders["embed_batch"])
    check("query uses RETRIEVAL_QUERY", "RETRIEVAL_QUERY" in builders["search"])
    check("docs use RETRIEVAL_DOCUMENT", "RETRIEVAL_DOCUMENT" in builders["embed_batch"])


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
                                  "vectorize.py", "bq.py", "pipeline.py"]
                if (Path(tmp) / name).read_text().rstrip("\n")
                != (Path(cwd) / name).read_text().rstrip("\n")
            ]
        finally:
            os.chdir(cwd)
    check(f"embedded modules in sync{' (' + ', '.join(drifted) + ')' if drifted else ''}",
          not drifted)


def main() -> int:
    for suite in (test_exclusions, test_families, test_schema_drift,
                  test_chunking, test_sql, test_notebook):
        suite()
        print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
