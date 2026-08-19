"""Filename/MIME classification and table-family grouping.

The central idea: a Google Takeout / Fitbit export contains thousands of files
that are really *one table each, sharded by date*. `heart_rate_2026-04-05.csv`
and `heart_rate_2026-07-05.csv` are not two tables, they are two days of one
table. Grouping them into "families" is what turns 1000+ loose files into a few
dozen queryable tables.
"""

from __future__ import annotations

import posixpath
import re
from dataclasses import dataclass, field

# MIME types we can parse into rows.
TABULAR_MIMES = {
    "text/csv": "csv",
    "text/tab-separated-values": "tsv",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.google-apps.spreadsheet": "gsheet",
    "application/json": "json",
    "application/x-ndjson": "ndjson",
}

# MIME types we extract text from.
DOCUMENT_MIMES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/msword": "doc",
    "application/vnd.google-apps.document": "gdoc",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.google-apps.presentation": "gslides",
    "text/plain": "txt",
    "text/markdown": "md",
    "text/html": "html",
    "application/rtf": "rtf",
}

# Extensions win when Drive reports a useless MIME type (very common for
# Takeout uploads, which often arrive as application/octet-stream).
EXTENSION_OVERRIDES = {
    "csv": ("tabular", "csv"),
    "tsv": ("tabular", "tsv"),
    "xlsx": ("tabular", "xlsx"),
    "xlsm": ("tabular", "xlsx"),
    "xls": ("tabular", "xls"),
    "json": ("tabular", "json"),
    "ndjson": ("tabular", "ndjson"),
    "jsonl": ("tabular", "ndjson"),
    "pdf": ("document", "pdf"),
    "docx": ("document", "docx"),
    "doc": ("document", "doc"),
    "pptx": ("document", "pptx"),
    "txt": ("document", "txt"),
    "md": ("document", "md"),
    "html": ("document", "html"),
    "htm": ("document", "html"),
    "rtf": ("document", "rtf"),
}

FOLDER_MIME = "application/vnd.google-apps.folder"

MEDIA_PREFIXES = ("image/", "video/", "audio/", "font/")

# Trailing shard tokens stripped to find the family stem, longest-first so that
# `_2026-05-01` is consumed before the bare `_2026` rule can nibble at it.
_SHARD_PATTERNS = [
    r"[ _-]+\d{4}[-_]\d{2}[-_]\d{2}(?:[ _-]?\d{2}[-_:]\d{2}(?:[-_:]\d{2})?)?$",
    r"[ _-]+\d{4}[-_]\d{2}$",
    r"[ _-]+\d{8}$",
    r"[ _-]+\d{4}$",
    r"\s*\((\d+)\)$",
    r"[ _-]+copy$",
    r"[ _-]+final$",
    r"[ _-]+v\d+$",
    r"[ _-]+part[ _-]?\d+$",
    r"[ _-]+\d+of\d+$",
]

_DATE_IN_NAME = re.compile(r"(\d{4})[-_]?(\d{2})[-_]?(\d{2})")


def classify(name: str, mime_type: str) -> tuple[str, str]:
    """Return ``(kind, fmt)`` where kind is tabular/document/media/other/folder."""
    if mime_type == FOLDER_MIME:
        return "folder", "folder"

    ext = extension_of(name)
    # Drive's MIME is authoritative for native Google types; otherwise the
    # extension is more trustworthy than octet-stream.
    if mime_type.startswith("application/vnd.google-apps."):
        if mime_type in TABULAR_MIMES:
            return "tabular", TABULAR_MIMES[mime_type]
        if mime_type in DOCUMENT_MIMES:
            return "document", DOCUMENT_MIMES[mime_type]
        return "other", mime_type.rsplit(".", 1)[-1]

    if ext in EXTENSION_OVERRIDES:
        return EXTENSION_OVERRIDES[ext]
    if mime_type in TABULAR_MIMES:
        return "tabular", TABULAR_MIMES[mime_type]
    if mime_type in DOCUMENT_MIMES:
        return "document", DOCUMENT_MIMES[mime_type]
    if mime_type.startswith(MEDIA_PREFIXES):
        return "media", mime_type.split("/", 1)[0]
    return "other", ext or "unknown"


def extension_of(name: str) -> str:
    base = posixpath.basename(name)
    if "." not in base:
        return ""
    return base.rsplit(".", 1)[-1].lower()


def strip_extension(name: str) -> str:
    base = posixpath.basename(name)
    if "." in base and extension_of(base):
        return base.rsplit(".", 1)[0]
    return base


def family_stem(name: str) -> str:
    """Strip date/version shard suffixes to get the shared stem of a family."""
    stem = strip_extension(name)
    changed = True
    while changed:
        changed = False
        for pattern in _SHARD_PATTERNS:
            new = re.sub(pattern, "", stem, flags=re.IGNORECASE)
            if new != stem and new.strip(" _-"):
                stem = new
                changed = True
    return stem.strip(" _-")


def shard_date(name: str) -> str | None:
    """Best-effort ISO date pulled from a filename, for the ``_src_date`` column."""
    match = _DATE_IN_NAME.search(strip_extension(name))
    if not match:
        return None
    year, month, day = match.groups()
    if not (1970 <= int(year) <= 2100):
        return None
    if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31):
        return None
    return f"{year}-{month}-{day}"


def sanitize_table_name(stem: str, fallback: str = "unnamed") -> str:
    """Coerce an arbitrary filename stem into a legal BigQuery table id."""
    name = re.sub(r"[^0-9a-zA-Z_]+", "_", stem).strip("_").lower()
    name = re.sub(r"_{2,}", "_", name)
    if not name:
        name = fallback
    if name[0].isdigit():
        name = f"t_{name}"
    return name[:1024]


def sanitize_column_name(raw: str, position: int) -> str:
    """Coerce a CSV header cell into a legal BigQuery column id."""
    name = re.sub(r"[^0-9a-zA-Z_]+", "_", str(raw)).strip("_").lower()
    name = re.sub(r"_{2,}", "_", name)
    if not name:
        name = f"col_{position}"
    if name[0].isdigit() or name.startswith("_"):
        name = f"c_{name.lstrip('_')}"
    # BigQuery reserves the _TABLE_/_FILE_/_PARTITION prefixes.
    for reserved in ("_table_", "_file_", "_partition"):
        if name.startswith(reserved):
            name = f"c{name}"
    return name[:300]


@dataclass
class Family:
    """A set of Drive files that should land in one BigQuery table."""

    table: str
    stem: str
    fmt: str
    files: list[dict] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        return sum(int(f.get("size_bytes") or 0) for f in self.files)


def build_families(files: list[dict]) -> dict[str, Family]:
    """Group classified tabular file records into families keyed by table name.

    Files sharing a stem but differing in format stay separate, because a CSV
    and an XLSX of the same stem rarely share a schema.
    """
    families: dict[str, Family] = {}
    for record in files:
        if record.get("kind") != "tabular":
            continue
        stem = family_stem(record["name"])
        fmt = record.get("fmt") or extension_of(record["name"])
        table = sanitize_table_name(stem)
        # Spreadsheets and CSVs of the same stem get distinct tables.
        if fmt in {"xlsx", "xls", "gsheet"}:
            table = f"{table}_sheet"
        elif fmt in {"json", "ndjson"}:
            table = f"{table}_json"
        key = table
        if key not in families:
            families[key] = Family(table=table, stem=stem, fmt=fmt)
        families[key].files.append(record)
    return families
