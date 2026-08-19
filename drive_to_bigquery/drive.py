"""Drive enumeration and download.

Two modes, yielding identically shaped records so everything downstream is
mode-agnostic:

* ``walk`` / ``download`` -- the Drive API, for a service account or ADC.
* ``walk_local`` / ``read_local`` -- an already-mounted Drive (Colab's
  ``drive.mount``, or Drive for Desktop). Files are ordinary paths, so there is
  no pagination, no per-file API call, and no download quota. This is by far the
  cheaper mode for a Drive with thousands of files.
"""

from __future__ import annotations

import datetime as dt
import io
import json
import os
import time
from pathlib import Path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from classify import FOLDER_MIME, classify, extension_of, family_stem, shard_date

FIELDS = (
    "nextPageToken,files(id,name,mimeType,size,md5Checksum,createdTime,"
    "modifiedTime,parents,trashed,shortcutDetails)"
)

# Google-native formats have no bytes to download; they must be exported.
EXPORT_MIMES = {
    "application/vnd.google-apps.spreadsheet": (
        "text/csv",
        "csv",
    ),
    "application/vnd.google-apps.document": (
        "text/plain",
        "txt",
    ),
    "application/vnd.google-apps.presentation": (
        "text/plain",
        "txt",
    ),
}

RETRYABLE_STATUS = {403, 429, 500, 502, 503, 504}


def _retry(call, attempts: int = 5, what: str = "drive call"):
    """Retry a Drive request through rate limits with exponential backoff."""
    delay = 2.0
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return call()
        except HttpError as exc:  # pragma: no cover - network dependent
            status = getattr(exc.resp, "status", None)
            if status not in RETRYABLE_STATUS or attempt == attempts - 1:
                raise
            last = exc
            time.sleep(delay)
            delay *= 2
    raise RuntimeError(f"{what} failed after {attempts} attempts: {last}")


def walk(service, root_id: str | None = None, include_trashed: bool = False):
    """Yield file records under ``root_id`` (whole My Drive when None).

    Breadth-first so that a partial run still covers whole folders, and so the
    path column can be built incrementally without a second lookup.
    """
    if root_id:
        root_meta = _retry(
            lambda: service.files()
            .get(fileId=root_id, fields="id,name,mimeType", supportsAllDrives=True)
            .execute(),
            what=f"get root {root_id}",
        )
        queue = [(root_id, root_meta.get("name", "/"))]
        seen_folders = {root_id}
    else:
        queue = [("root", "")]
        seen_folders = {"root"}

    while queue:
        folder_id, folder_path = queue.pop(0)
        page_token = None
        while True:
            query = f"'{folder_id}' in parents"
            if not include_trashed:
                query += " and trashed = false"

            def _list(token=page_token, q=query):
                return (
                    service.files()
                    .list(
                        q=q,
                        fields=FIELDS,
                        pageSize=1000,
                        pageToken=token,
                        supportsAllDrives=True,
                        includeItemsFromAllDrives=True,
                    )
                    .execute()
                )

            response = _retry(_list, what=f"list {folder_id}")

            for item in response.get("files", []):
                name = item.get("name", "")
                mime = item.get("mimeType", "")
                path = f"{folder_path}/{name}" if folder_path else name

                if mime == FOLDER_MIME:
                    if item["id"] not in seen_folders:
                        seen_folders.add(item["id"])
                        queue.append((item["id"], path))
                    continue

                # Shortcuts point elsewhere; the target is enumerated on its own.
                if mime == "application/vnd.google-apps.shortcut":
                    continue

                kind, fmt = classify(name, mime)
                yield {
                    "file_id": item["id"],
                    "name": name,
                    "path": path,
                    "mime_type": mime,
                    "extension": extension_of(name),
                    "size_bytes": int(item["size"]) if item.get("size") else None,
                    "md5_checksum": item.get("md5Checksum"),
                    "created_time": item.get("createdTime"),
                    "modified_time": item.get("modifiedTime"),
                    "parent_id": (item.get("parents") or [None])[0],
                    "kind": kind,
                    "fmt": fmt,
                    "family_stem": family_stem(name) if kind == "tabular" else None,
                    "shard_date": shard_date(name),
                }

            page_token = response.get("nextPageToken")
            if not page_token:
                break


# A mounted Drive represents Google-native files as small JSON stub files with
# these extensions. The stub holds the real file id but none of the data, so the
# bytes still have to be exported through the API.
STUB_EXTENSIONS = {
    "gsheet": "application/vnd.google-apps.spreadsheet",
    "gdoc": "application/vnd.google-apps.document",
    "gslides": "application/vnd.google-apps.presentation",
    "gdraw": "application/vnd.google-apps.drawing",
    "gform": "application/vnd.google-apps.form",
}

# Mount bookkeeping that is not user data.
SKIP_NAMES = {".shortcut-targets-by-id", ".file-revisions-by-id", ".Trash", ".DS_Store"}


def _stub_file_id(path: Path) -> str | None:
    """Pull the Drive file id out of a mounted .gsheet/.gdoc stub."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None
    # Stubs carry either {"doc_id": ...} or {"url": "...open?id=FILE_ID"}.
    if isinstance(payload, dict):
        if payload.get("doc_id"):
            return str(payload["doc_id"])
        url = payload.get("url") or ""
        if "id=" in url:
            return url.split("id=", 1)[1].split("&", 1)[0]
    return None


def walk_local(root: str, include_hidden: bool = False):
    """Yield file records from a mounted Drive directory tree.

    Native Google files are surfaced with their real Drive id and MIME type so
    that ``read_local`` can export them through the API; everything else is read
    straight off disk.
    """
    root_path = Path(root).expanduser().resolve()
    if not root_path.is_dir():
        raise NotADirectoryError(f"{root_path} is not a directory")

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Prune in place so os.walk does not descend into them.
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_NAMES and (include_hidden or not d.startswith("."))
        ]
        for filename in filenames:
            if filename in SKIP_NAMES:
                continue
            if not include_hidden and filename.startswith("."):
                continue

            full = Path(dirpath) / filename
            try:
                stat = full.stat()
            except OSError:
                continue

            relative = full.relative_to(root_path).as_posix()
            ext = extension_of(filename)

            if ext in STUB_EXTENSIONS:
                mime = STUB_EXTENSIONS[ext]
                file_id = _stub_file_id(full) or f"local:{relative}"
                size = None  # the stub's size is meaningless
            else:
                mime = ""
                file_id = f"local:{relative}"
                size = stat.st_size

            kind, fmt = classify(filename, mime)
            yield {
                "file_id": file_id,
                "name": filename,
                "path": relative,
                "local_path": str(full),
                "mime_type": mime,
                "extension": ext,
                "size_bytes": size,
                "md5_checksum": None,
                "created_time": _iso(stat.st_ctime),
                "modified_time": _iso(stat.st_mtime),
                "parent_id": Path(dirpath).name,
                "kind": kind,
                "fmt": fmt,
                "family_stem": family_stem(filename) if kind == "tabular" else None,
                "shard_date": shard_date(filename),
            }


def _iso(timestamp: float) -> str:
    return dt.datetime.fromtimestamp(timestamp, dt.timezone.utc).isoformat()


def read_local(record: dict, service=None) -> tuple[bytes, str]:
    """Read a mounted file's bytes, exporting native Google files via the API.

    ``service`` is only needed for native files; plain files never touch the API.
    """
    mime = record.get("mime_type") or ""
    if mime in EXPORT_MIMES:
        if service is None:
            raise RuntimeError(
                f"{record['name']} is a native Google file and needs a Drive "
                "service to export; pass credentials or skip it"
            )
        return download(service, record["file_id"], mime)
    return Path(record["local_path"]).read_bytes(), ""


def download(service, file_id: str, mime_type: str) -> tuple[bytes, str]:
    """Fetch a file's bytes. Returns ``(data, effective_format)``.

    Google-native files are exported; everything else is downloaded verbatim.
    """
    if mime_type in EXPORT_MIMES:
        export_mime, fmt = EXPORT_MIMES[mime_type]
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
    else:
        fmt = ""
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)

    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request, chunksize=8 * 1024 * 1024)
    done = False
    while not done:
        _, done = _retry(downloader.next_chunk, what=f"download {file_id}")
    return buffer.getvalue(), fmt
