"""Split extracted text into embedding-sized chunks.

Embedding models cap input length, so a 200-page PDF cannot become one vector.
It also should not: a single vector over a whole document averages away the
specific passage you were searching for. Chunking on natural boundaries with a
little overlap keeps each vector about one idea, and keeps a match pointing at a
findable location in the source.
"""

from __future__ import annotations

import re

# ~2000 chars is roughly 500 tokens: comfortably inside every current embedding
# model's window, and large enough that a chunk carries real context.
TARGET_CHARS = 2000
OVERLAP_CHARS = 200
MIN_CHARS = 60  # below this a chunk is noise (page numbers, stray headers)

# Split on blank lines first, then sentence ends, then hard-wrap. Preferring
# paragraph breaks keeps related sentences in the same vector.
_PARAGRAPH = re.compile(r"\n\s*\n")
_SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\"'])")
_WHITESPACE = re.compile(r"[ \t]+")


def normalize(text: str) -> str:
    """Collapse the whitespace damage that PDF extraction leaves behind."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\xa0", " ").replace("​", "")
    text = _WHITESPACE.sub(" ", text)
    # Three or more newlines carry no more meaning than two.
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Join lines broken mid-sentence by hard-wrapping, but keep real breaks.
    text = re.sub(r"(?<=[a-z,;])\n(?=[a-z])", " ", text)
    return text.strip()


def split(text: str, target: int = TARGET_CHARS, overlap: int = OVERLAP_CHARS) -> list[str]:
    """Split text into overlapping chunks of about ``target`` characters."""
    text = normalize(text)
    if not text:
        return []
    if len(text) <= target:
        return [text]

    units = _units(text, target)

    chunks: list[str] = []
    current = ""
    for unit in units:
        if not current:
            current = unit
        elif len(current) + 1 + len(unit) <= target:
            current = f"{current}\n{unit}" if unit.startswith(("•", "-", "*")) else f"{current} {unit}"
        else:
            chunks.append(current)
            current = _tail(current, overlap) + " " + unit if overlap else unit
    if current:
        chunks.append(current)

    return [c.strip() for c in chunks if len(c.strip()) >= MIN_CHARS]


def _units(text: str, target: int) -> list[str]:
    """Break text into the largest pieces that still fit a chunk."""
    units: list[str] = []
    for paragraph in _PARAGRAPH.split(text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph) <= target:
            units.append(paragraph)
            continue
        # Too long: fall back to sentences.
        for sentence in _SENTENCE.split(paragraph):
            sentence = sentence.strip()
            if not sentence:
                continue
            if len(sentence) <= target:
                units.append(sentence)
            else:
                # Still too long (no punctuation at all -- transcripts, logs).
                units.extend(
                    sentence[i : i + target] for i in range(0, len(sentence), target)
                )
    return units


def _tail(text: str, overlap: int) -> str:
    """Last ``overlap`` chars of a chunk, trimmed to a word boundary."""
    if overlap <= 0 or len(text) <= overlap:
        return text
    tail = text[-overlap:]
    space = tail.find(" ")
    return tail[space + 1 :] if space != -1 else tail


def chunk_document(record: dict, text: str) -> list[dict]:
    """Turn one document's text into chunk rows ready for loading."""
    pieces = split(text)
    total = len(pieces)
    return [
        {
            "chunk_id": f"{record['file_id']}::{index:05d}",
            "file_id": record["file_id"],
            "name": record["name"],
            "path": record["path"],
            "chunk_index": index,
            "chunk_total": total,
            "char_count": len(piece),
            # The text column ML.GENERATE_EMBEDDING reads. Prefixing the source
            # name gives the vector a little document-level context, which
            # measurably helps retrieval on short chunks.
            "content": f"{record['name']}\n\n{piece}",
            "raw_content": piece,
        }
        for index, piece in enumerate(pieces)
    ]


def row_to_text(row: dict, table: str, max_chars: int = TARGET_CHARS) -> str:
    """Render a table row as prose so it can be embedded and searched.

    Telemetry rows are meaningless as text, which is why only non-telemetry
    tables get vectorized -- but a row from a spreadsheet of names, dates and
    notes is genuinely worth finding semantically.
    """
    parts = [f"Table: {table}"]
    for key, value in row.items():
        if key.startswith("_src_") or key == "_ingested_at":
            continue
        if value is None or value == "":
            continue
        text = str(value).strip()
        if not text or text.lower() in {"nan", "nat", "none"}:
            continue
        parts.append(f"{key.replace('_', ' ')}: {text}")
    return "\n".join(parts)[:max_chars]
