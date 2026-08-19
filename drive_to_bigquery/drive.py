"""Drive enumeration and download.

Walks a folder tree (or the whole of My Drive) and yields one record per file,
carrying enough metadata to build the manifest table without a second pass.
"""

from __future__ import annotations

import io
import time

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
