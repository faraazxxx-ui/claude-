#!/usr/bin/env python3
"""
Life Intelligence Engine — File Cataloger
Recursively scans a source directory, fingerprints every file, and produces
a manifest.json for downstream processing. Supports incremental updates via
--existing-manifest to skip already-processed files.
"""

import argparse
import hashlib
import json
import mimetypes
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

# File type classification
TYPE_MAP = {
    ".pdf": "pdf",
    ".doc": "document", ".docx": "document", ".odt": "document", ".rtf": "document",
    ".txt": "text", ".md": "markdown", ".rst": "text", ".log": "text",
    ".csv": "spreadsheet", ".xlsx": "spreadsheet", ".xls": "spreadsheet", ".ods": "spreadsheet", ".tsv": "spreadsheet",
    ".py": "code", ".js": "code", ".ts": "code", ".java": "code", ".cpp": "code",
    ".c": "code", ".h": "code", ".rb": "code", ".go": "code", ".rs": "code",
    ".swift": "code", ".kt": "code", ".sh": "code", ".bash": "code", ".zsh": "code",
    ".html": "web", ".htm": "web", ".css": "code", ".xml": "web", ".json": "data",
    ".yaml": "data", ".yml": "data", ".toml": "data", ".ini": "data",
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".gif": "image",
    ".bmp": "image", ".tiff": "image", ".tif": "image", ".webp": "image",
    ".svg": "image", ".heic": "image", ".heif": "image",
    ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".flac": "audio",
    ".aac": "audio", ".ogg": "audio", ".wma": "audio",
    ".mp4": "video", ".mov": "video", ".avi": "video", ".mkv": "video",
    ".webm": "video", ".wmv": "video", ".flv": "video",
    ".zip": "archive", ".tar": "archive", ".gz": "archive", ".7z": "archive",
    ".rar": "archive", ".bz2": "archive",
    ".ipynb": "notebook",
    ".pptx": "presentation", ".ppt": "presentation", ".key": "presentation",
    ".enex": "evernote_export",
    ".epub": "ebook", ".mobi": "ebook",
    ".sql": "database", ".db": "database", ".sqlite": "database",
}

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".DS_Store", ".Trash", "venv", ".venv", ".env"}
SKIP_FILES = {".DS_Store", "Thumbs.db", "desktop.ini", ".gitignore"}


def file_hash(filepath: str, chunk_size: int = 8192) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def classify_file(filepath: str) -> str:
    """Classify file type by extension."""
    ext = Path(filepath).suffix.lower()
    return TYPE_MAP.get(ext, "unknown")


def get_preview(filepath: str, file_type: str, max_chars: int = 500) -> str:
    """Get a text preview of the file content where possible."""
    if file_type in ("text", "markdown", "code", "data", "web", "notebook"):
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                return f.read(max_chars).strip()
        except Exception:
            return ""
    return ""


def scan_directory(source: str) -> list:
    """Recursively scan directory and build file entries."""
    entries = []
    source_path = Path(source).resolve()

    for root, dirs, files in os.walk(source_path):
        # Skip hidden/system directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]

        for fname in files:
            if fname in SKIP_FILES or fname.startswith("."):
                continue

            fpath = os.path.join(root, fname)
            try:
                stat = os.stat(fpath)
                ftype = classify_file(fpath)
                rel_path = os.path.relpath(fpath, source_path)

                entry = {
                    "file_id": str(uuid.uuid4()),
                    "path": fpath,
                    "relative_path": rel_path,
                    "filename": fname,
                    "extension": Path(fname).suffix.lower(),
                    "file_type": ftype,
                    "size_bytes": stat.st_size,
                    "size_kb": round(stat.st_size / 1024, 2),
                    "hash": file_hash(fpath),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "preview": get_preview(fpath, ftype),
                    "is_new": True,
                    "processed": False,
                }
                entries.append(entry)
            except (PermissionError, OSError) as e:
                print(f"  SKIP (error): {fpath} — {e}", file=sys.stderr)

    return entries


def merge_with_existing(new_entries: list, existing_path: str) -> list:
    """Merge new entries with existing manifest, marking only truly new files."""
    with open(existing_path, "r") as f:
        existing = json.load(f)

    existing_hashes = {e["hash"] for e in existing.get("files", [])}
    existing_files = existing.get("files", [])

    # Mark existing files as not new
    for entry in existing_files:
        entry["is_new"] = False

    # Add only genuinely new files
    added = 0
    for entry in new_entries:
        if entry["hash"] not in existing_hashes:
            entry["is_new"] = True
            existing_files.append(entry)
            added += 1
        # else: already exists, skip

    print(f"  Existing files: {len(existing_hashes)}, New files added: {added}")
    return existing_files


def main():
    parser = argparse.ArgumentParser(description="Catalog files for Life Intelligence Engine")
    parser.add_argument("--source", required=True, help="Source directory to scan")
    parser.add_argument("--output", required=True, help="Output manifest.json path")
    parser.add_argument("--existing-manifest", help="Path to existing manifest for incremental update")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"ERROR: Source directory not found: {args.source}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    print(f"Scanning: {args.source}")
    entries = scan_directory(args.source)
    print(f"  Found {len(entries)} files")

    if args.existing_manifest and os.path.exists(args.existing_manifest):
        print(f"Merging with existing manifest: {args.existing_manifest}")
        entries = merge_with_existing(entries, args.existing_manifest)

    # Build type summary
    type_counts = {}
    total_size = 0
    for e in entries:
        ftype = e["file_type"]
        type_counts[ftype] = type_counts.get(ftype, 0) + 1
        total_size += e["size_bytes"]

    manifest = {
        "generated": datetime.now().isoformat(),
        "source_directory": os.path.abspath(args.source),
        "total_files": len(entries),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "new_files": sum(1 for e in entries if e.get("is_new")),
        "type_summary": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
        "files": entries,
    }

    with open(args.output, "w") as f:
        json.dump(manifest, f, indent=2, default=str)

    print(f"\nManifest written: {args.output}")
    print(f"  Total files: {manifest['total_files']}")
    print(f"  Total size: {manifest['total_size_mb']} MB")
    print(f"  New files: {manifest['new_files']}")
    print(f"  Type breakdown:")
    for ftype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"    {ftype}: {count}")


if __name__ == "__main__":
    main()
