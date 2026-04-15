# Life Intelligence Engine: GitHub Gems Integration Guide

This guide documents the battle-tested open-source tools recommended for the Life Intelligence Engine pipeline, what they replace, and how to integrate them. Each tool was identified through the `/github-gem-seeker` skill and evaluated against the quality tiers.

---

## Tier 1: Core Pipeline Replacements

These tools replace the brittle, custom-built parsers in the original pipeline with production-grade alternatives.

### Unstructured.io

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/Unstructured-IO/unstructured](https://github.com/Unstructured-IO/unstructured) |
| **Stars** | 10,000+ |
| **Tier** | Excellent |
| **Replaces** | Custom PyMuPDF, python-docx, openpyxl, and HTML parsing scripts |
| **Purpose** | Universal document ETL. A single library that partitions and extracts text, tables, and metadata from dozens of formats (PDF, DOCX, PPTX, EML, HTML, images with OCR, and more). |

**Installation:**
```bash
sudo uv pip install --system "unstructured[all-docs]"
```

**Usage in this pipeline:**
```python
from unstructured.partition.auto import partition

# Automatically detects file type and extracts structured elements
elements = partition(filename="path/to/document.pdf")
for element in elements:
    print(f"Type: {type(element).__name__}, Text: {element.text[:200]}")
```

**Integration point:** Replaces the entire `extract_and_tokenize.py` script. Instead of maintaining separate parsers for each file type, Unstructured.io handles routing automatically. This eliminates the fragile format-specific code and provides superior extraction quality, especially for complex layouts and tables.

---

### Marker

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/VikParuchuri/marker](https://github.com/VikParuchuri/marker) |
| **Stars** | 20,000+ |
| **Tier** | Excellent |
| **Replaces** | PyMuPDF text extraction, cloud OCR services |
| **Purpose** | State-of-the-art PDF-to-Markdown conversion. Outperforms most commercial OCR engines. Preserves formatting, tables, headers, and document structure. |

**Installation:**
```bash
sudo uv pip install --system marker-pdf
```

**Usage in this pipeline:**
```python
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict

models = create_model_dict()
converter = PdfConverter(artifact_dict=models)
rendered = converter("path/to/document.pdf")
markdown_text = rendered.markdown
```

**Integration point:** Used as the primary PDF processor in Pass 2 (Extraction). For any `application/pdf` file, Marker is attempted first. If it fails (e.g., for encrypted PDFs), Unstructured.io serves as the fallback. This combination ensures near-100% PDF extraction coverage.

---

## Tier 2: Analysis and Intelligence Tools

These tools power the semantic analysis, entity resolution, and knowledge graph construction.

### sentence-transformers

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/UKPLab/sentence-transformers](https://github.com/UKPLab/sentence-transformers) |
| **Stars** | 15,000+ |
| **Tier** | Excellent |
| **Replaces** | Folder-based segmentation (the original pipeline grouped files by folder, not by meaning) |
| **Purpose** | Generates high-quality vector embeddings of text chunks for semantic clustering. |

**Installation:**
```bash
sudo uv pip install --system sentence-transformers
```

**Usage in this pipeline:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = ["This is a legal filing about UHS", "Employment contract for PGY-1"]
embeddings = model.encode(texts)
# Use embeddings with HDBSCAN or K-Means for clustering
```

**Integration point:** Used in Pass 4 (Semantic Clustering). Each extracted text chunk is embedded, then clustered using HDBSCAN. This replaces the arbitrary folder-based segmentation with meaning-based grouping, ensuring that related documents are analyzed together regardless of their file system location.

---

### thefuzz

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/seatgeek/thefuzz](https://github.com/seatgeek/thefuzz) |
| **Stars** | 9,000+ |
| **Tier** | Solid |
| **Replaces** | The non-existent entity resolution in the original pipeline |
| **Purpose** | Fuzzy string matching for entity deduplication. Resolves variations like "Dr. Rahman" and "Faraaz Rahman" into a single canonical entity. |

**Installation:**
```bash
sudo uv pip install --system thefuzz python-Levenshtein
```

**Usage in this pipeline:**
```python
from thefuzz import fuzz, process

entities = ["Dr. Rahman", "Faraaz Rahman", "Mohammed F. Rahman", "Dr. Ali"]
# Find matches above 80% similarity
for entity in entities:
    matches = process.extract(entity, entities, scorer=fuzz.token_sort_ratio)
    high_matches = [(m, score) for m, score, _ in matches if score > 80 and m != entity]
    if high_matches:
        print(f"{entity} -> {high_matches}")
```

**Integration point:** Used in Pass 8 (Cleanup and Entity Resolution). After all entities are extracted across all segments, thefuzz performs pairwise comparison to identify and merge duplicates. The result is the canonical Entity Registry with resolved aliases.

---

### dedupe

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/dedupeio/dedupe](https://github.com/dedupeio/dedupe) |
| **Stars** | 4,000+ |
| **Tier** | Solid |
| **Replaces** | Manual entity resolution for complex cases |
| **Purpose** | ML-based deduplication and entity resolution on structured data. More powerful than thefuzz for large datasets with multiple fields. |

**Installation:**
```bash
sudo uv pip install --system dedupe
```

**Integration point:** Used as an advanced complement to thefuzz when the entity registry grows beyond simple string matching. Dedupe can train on labeled examples to learn complex matching rules across multiple fields (name, role, organization, context).

---

## Tier 3: Media Processing Tools

These tools handle the 1,600+ unprocessed audio, video, and image files.

### Tesseract OCR

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract) |
| **Stars** | 60,000+ |
| **Tier** | Legendary |
| **Replaces** | Missing OCR capability in the original pipeline |
| **Purpose** | Extract text from images, screenshots, and scanned documents. |

**Installation:**
```bash
sudo apt-get install -y tesseract-ocr
sudo uv pip install --system pytesseract
```

**Usage in this pipeline:**
```python
import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open("screenshot.png"))
```

**Integration point:** Used in Pass 2 for the 1,033 unprocessed images, especially the C1-C53 text message screenshot series. Also used by Unstructured.io as a backend for image-based document extraction.

---

### FFmpeg

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) |
| **Stars** | 45,000+ |
| **Tier** | Legendary |
| **Replaces** | Nothing (audio/video was completely skipped) |
| **Purpose** | Universal media processing. Convert audio/video formats, extract audio tracks from video for transcription. |

**Installation:**
```bash
sudo apt-get install -y ffmpeg
```

**Usage in this pipeline:**
```bash
# Extract audio from video for transcription
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav
# Then transcribe
manus-speech-to-text audio.wav
```

**Integration point:** Pre-processing step before audio transcription. Converts the 582 audio files into a format compatible with the transcription utility.

---

### Sandbox Built-in Utilities

These are already available in the sandbox and require no installation:

| Utility | Command | Purpose |
| :--- | :--- | :--- |
| **Speech-to-Text** | `manus-speech-to-text file.mp3` | Transcribe audio files to text |
| **Video Analysis** | `manus-analyze-video file.mp4 "transcribe"` | Analyze and transcribe video content |

---

## Tier 4: Knowledge Graph and RAG

These tools enable the advanced knowledge graph and retrieval-augmented generation capabilities.

### RAGFlow

| Property | Value |
| :--- | :--- |
| **GitHub** | [github.com/infiniflow/ragflow](https://github.com/infiniflow/ragflow) |
| **Stars** | 30,000+ |
| **Tier** | Excellent |
| **Replaces** | The static report output (transforms it into a queryable system) |
| **Purpose** | Open-source RAG engine for building a live, queryable knowledge base from documents. |

**Integration point:** After the 9-pass pipeline completes, RAGFlow can be deployed as a persistent service that indexes all extracted content. This transforms the Second Brain from a static archive into a live intelligence system where you can ask natural language questions and get source-cited answers.

---

## Tool Selection Matrix

| Pipeline Pass | Primary Tool | Fallback Tool | Purpose |
| :--- | :--- | :--- | :--- |
| Pass 1: Inventory | `gws` CLI | `rclone` | File crawling and manifest generation |
| Pass 2: Extraction (PDF) | Marker | Unstructured.io | PDF to structured text |
| Pass 2: Extraction (Other) | Unstructured.io | Custom parsers | Universal document parsing |
| Pass 2: Extraction (Images) | Tesseract OCR | Marker | Image text extraction |
| Pass 2: Extraction (Audio) | `manus-speech-to-text` | FFmpeg + Whisper | Audio transcription |
| Pass 2: Extraction (Video) | `manus-analyze-video` | FFmpeg + transcription | Video analysis |
| Pass 4: Clustering | sentence-transformers + HDBSCAN | K-Means | Semantic grouping |
| Pass 8: Entity Resolution | thefuzz | dedupe | Entity deduplication |
| Post-Pipeline: RAG | RAGFlow | LlamaIndex | Live querying |

---

> **Credit:** Every tool listed here is an open-source project maintained by dedicated developers. If any of these tools helped you, consider giving them a star on GitHub to support the maintainers.
