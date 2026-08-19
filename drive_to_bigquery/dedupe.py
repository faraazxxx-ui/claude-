"""Content-hash deduplication, run before anything expensive.

Measured on the target Drive: 100 spreadsheet files are 31 distinct documents.
`PGY-3.xlsx` exists 9 times; a 240 MB textbook PDF exists twice. Roughly a 3x
duplication factor.

That matters far more than it first looks:

* Embedding cost is paid per copy, so ~3x the bill for no extra information.
* Worse, the cross-link layer would be swamped. Every duplicate pair sits at
  cosine distance ~0, so `file_bridges` and `indirect_relations` would rank
  identical-file matches above every genuine connection. The expensive layer
  would produce confident noise.

So dedup runs first, and only canonical copies are parsed, chunked and embedded.
Nothing is lost: every copy stays in the manifest, marked `duplicate` with a
pointer to its canonical file, so "where are all the copies of this" remains
answerable.

The hashing is cheap because of one observation: two files of *different* sizes
cannot be identical. Only files whose size collides with another file are ever
read.
"""

from __future__ import annotations

import hashlib
import logging
from collections import defaultdict
from pathlib import Path

log = logging.getLogger(__name__)

READ_CHUNK = 1024 * 1024

# Hashing reads the whole file. Above this, hash a head+tail sample plus the
# size instead -- enough to separate genuinely different large files without
# reading gigabytes off a network mount.
FULL_HASH_LIMIT = 64 * 1024 * 1024
SAMPLE_BYTES = 4 * 1024 * 1024


def hash_local(path: str, size: int | None = None) -> str | None:
    """Content hash of a local file, sampling very large ones."""
    try:
        file_size = size if size is not None else Path(path).stat().st_size
        digest = hashlib.md5(usedforsecurity=False)
        digest.update(str(file_size).encode())
        with open(path, "rb") as handle:
            if file_size <= FULL_HASH_LIMIT:
                while chunk := handle.read(READ_CHUNK):
                    digest.update(chunk)
            else:
                digest.update(handle.read(SAMPLE_BYTES))
                handle.seek(-SAMPLE_BYTES, 2)
                digest.update(handle.read(SAMPLE_BYTES))
                digest.update(b"sampled")
        return digest.hexdigest()
    except OSError as exc:
        log.debug("cannot hash %s: %s", path, exc)
        return None


def assign_hashes(files: list[dict]) -> None:
    """Fill in `content_hash` on each record, in place.

    Drive's own `md5Checksum` is used when present (API mode gives it for free).
    Otherwise, only size-colliding local files are read -- a file with a unique
    size is already known to be unique.
    """
    by_size: dict[int, list[dict]] = defaultdict(list)
    for record in files:
        existing = record.get("md5_checksum")
        if existing:
            record["content_hash"] = existing
            continue
        record["content_hash"] = None
        size = record.get("size_bytes")
        if size:
            by_size[int(size)].append(record)

    candidates = [r for group in by_size.values() if len(group) > 1 for r in group]
    if not candidates:
        return
    log.info(
        "hashing %d of %d files (only sizes that collide can be duplicates)",
        len(candidates),
        len(files),
    )
    for record in candidates:
        path = record.get("local_path")
        if path:
            record["content_hash"] = hash_local(path, record.get("size_bytes"))


def partition_duplicates(files: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split into ``(canonical, duplicates)`` by content hash.

    The canonical copy is the shallowest path, then the shortest, then the
    lexicographically first -- a stable rule that tends to pick the copy in the
    most sensible place rather than one buried in a nested backup tree.
    """
    groups: dict[str, list[dict]] = defaultdict(list)
    unhashed: list[dict] = []
    for record in files:
        digest = record.get("content_hash")
        if digest:
            groups[digest].append(record)
        else:
            unhashed.append(record)

    canonical: list[dict] = list(unhashed)
    duplicates: list[dict] = []
    for digest, group in groups.items():
        if len(group) == 1:
            canonical.append(group[0])
            continue
        group.sort(key=lambda r: (
            (r.get("path") or "").count("/"),
            len(r.get("path") or ""),
            r.get("path") or "",
        ))
        keeper, rest = group[0], group[1:]
        canonical.append(keeper)
        for record in rest:
            duplicates.append({
                **record,
                "duplicate_of": keeper["file_id"],
                "duplicate_of_path": keeper.get("path"),
            })
    return canonical, duplicates


def summarize(canonical: list[dict], duplicates: list[dict]) -> dict:
    wasted = sum(int(r.get("size_bytes") or 0) for r in duplicates)
    return {
        "total": len(canonical) + len(duplicates),
        "canonical": len(canonical),
        "duplicates": len(duplicates),
        "wasted_bytes": wasted,
        "factor": round((len(canonical) + len(duplicates)) / max(len(canonical), 1), 2),
    }


def top_duplicated(duplicates: list[dict], limit: int = 15) -> list[tuple[str, int, int]]:
    """``(name, copies, wasted_bytes)`` for the worst offenders."""
    counts: dict[str, list[dict]] = defaultdict(list)
    for record in duplicates:
        counts[record["name"]].append(record)
    rows = [
        (name, len(group) + 1, sum(int(r.get("size_bytes") or 0) for r in group))
        for name, group in counts.items()
    ]
    rows.sort(key=lambda row: -row[2])
    return rows[:limit]
