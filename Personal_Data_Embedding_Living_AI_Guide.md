# The Living AI File: Complete Guide to Personal Data Extraction, Embedding & Self-Retraining

**Final Answer: The Complete Pipeline Architecture**

Your personal data becomes a "living AI file" through a 7-stage pipeline: **Extract → Format → Triage → Embed → Inject → Retrain → Sync**. The system continuously ingests data from all your sources (Google Drive, Gmail, iCloud, chat apps, social media, notes), formats it into BigQuery-compatible JSONL with `gs://` URIs, triages it across life domains, generates vector embeddings, and injects the context into every AI platform (Claude Projects, Gemini Gems, Copilot Enterprise Graph Connectors, Grok Collections) — with a self-retraining feedback loop that keeps the AI "alive" in your files.

---

## Table of Contents

1. [Stage 1: Data Extraction from All Sources](#stage-1-data-extraction-from-all-sources)
2. [Stage 2: BigQuery Format Requirements (The Exact URL Format)](#stage-2-bigquery-format-requirements)
3. [Stage 3: Life Domain Triage & Classification](#stage-3-life-domain-triage--classification)
4. [Stage 4: Vector Embedding Generation](#stage-4-vector-embedding-generation)
5. [Stage 5: Platform-Specific Injection](#stage-5-platform-specific-injection)
6. [Stage 6: Self-Retraining Architecture ("The AI Lives in the File")](#stage-6-self-retraining-architecture)
7. [Stage 7: Cross-Platform Memory Sync](#stage-7-cross-platform-memory-sync)
8. [Tools & Repositories Master List](#tools--repositories-master-list)
9. [Supporting Details Table](#supporting-details-table)

---

## Stage 1: Data Extraction from All Sources

### Step 1.1: Authentication Setup

Register applications and obtain credentials for each data source:

| Source | Auth Method | Endpoint/Access | Rate Limit |
|--------|------------|-----------------|------------|
| Google Drive | OAuth 2.0 (`drive.readonly` scope) | `GET https://www.googleapis.com/drive/v3/files` | 1,000,000 units/min/project |
| Gmail | OAuth 2.0 (`gmail.readonly` scope) | `GET https://gmail.googleapis.com/gmail/v1/users/{userId}/messages` | 250 units/user/sec |
| Notion | Integration Token (Bearer) | `GET https://api.notion.com/v1/blocks/{block_id}/children` | 3 requests/sec |
| Twitter/X | OAuth 2.0 or Data Archive | `GET /2/users/{id}/tweets` | 1500 req/15 min |
| Reddit | OAuth 2.0 | `GET /user/{username}/history` | 100 queries/min |
| Telegram | TDLib or Desktop Export | In-app "Export Telegram Data" | N/A (local) |
| Discord | Bot Token (NOT user token) | `GET /channels/{channel.id}/messages` | 50 req/sec |
| iCloud | Privacy data dump | https://privacy.apple.com | N/A (manual) |

### Step 1.2: Google Drive Extraction

```python
import subprocess, json

def list_folder(folder_id):
    params = json.dumps({
        "q": f"'{folder_id}' in parents and trashed = false",
        "fields": "files(id,name,mimeType,size,modifiedTime)",
        "pageSize": 1000
    })
    cmd = ["gws", "drive", "files", "list", "--params", params]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout).get("files", [])

# For Google Docs → export as plain text:
# gws drive files export --params '{"fileId": "ID", "mimeType": "text/plain"}' -o filename.txt

# For binary files (PDF, DOCX) → download directly:
# gws drive files get --params '{"fileId": "ID", "alt": "media"}' -o filename.pdf
```

### Step 1.3: Gmail Extraction

```python
# List all messages
# GET https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=500

# Fetch full message (RFC822 format for complete content)
# GET https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}?format=raw

# Parse with Python's email module:
import base64, email
raw_msg = base64.urlsafe_b64decode(response['raw'])
msg = email.message_from_bytes(raw_msg)
```

### Step 1.4: Chat & Social Media Archives

**Best approach: Request official data exports (GDPR/CCPA compliant)**

- **WhatsApp**: Settings → Chats → Export Chat (generates `.txt` + media)
- **Telegram**: Desktop → Settings → Advanced → Export Telegram Data (JSON/HTML)
- **Discord**: Settings → Privacy → Request All of My Data (JSON archive)
- **Twitter/X**: Settings → Your Account → Download an Archive (JSON)
- **Reddit**: Settings → Request Your Data (CSV/JSON)

### Step 1.5: Note-Taking Apps

```bash
# Obsidian: Direct filesystem access (Markdown files)
find ~/ObsidianVault -name "*.md" -exec cat {} \;

# Apple Notes: SQLite extraction
# Path: ~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite
# Requires parsing ZLIB-compressed protobuf blobs

# Notion: API recursive block fetching
# GET https://api.notion.com/v1/blocks/{block_id}/children
# Rate limit: 3 req/sec — use exponential backoff
```

### Step 1.6: Browser History

```bash
# Chrome (copy first — file is locked while browser runs)
cp ~/.config/google-chrome/Default/History /tmp/chrome_history.db
sqlite3 /tmp/chrome_history.db "SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10000;"

# Safari
cp ~/Library/Safari/History.db /tmp/safari_history.db
sqlite3 /tmp/safari_history.db "SELECT url, title, visit_count FROM history_items;"
```

---

## Stage 2: BigQuery Format Requirements

### The Exact URL Format BigQuery Requires

BigQuery loads data **exclusively from Google Cloud Storage** using `gs://` URIs:

```
gs://<bucket_name>/<object_path>
```

**Examples:**
```
gs://my-personal-data-bucket/knowledge_base/2024/notes.jsonl
gs://my-personal-data-bucket/embeddings/chunk_*.jsonl
gs://my-personal-data-bucket/exports/gmail_archive.avro
```

### Step 2.1: Supported Formats (Ranked by Performance)

| Format | Extension | Best For | Notes |
|--------|-----------|----------|-------|
| **Avro** | `.avro` | Best overall performance | Self-describing schema, preferred by Google |
| **Parquet** | `.parquet` | Columnar analytics | Excellent compression, fast queries |
| **JSONL** | `.jsonl` | Flexible nested data | Must be newline-delimited (NOT regular JSON) |
| **CSV** | `.csv` | Simple tabular data | Must be UTF-8, no nested fields |
| **ORC** | `.orc` | Hadoop ecosystem | Good compression |

### Step 2.2: The Exact JSON Schema for Personal Knowledge Base

```json
[
  {
    "name": "document_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "title",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "content",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "source_type",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "email | note | pdf | chat | social | browser"
  },
  {
    "name": "life_domain",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "career | finance | health | learning | personal | creative | relationships | home | digital | reference"
  },
  {
    "name": "metadata",
    "type": "RECORD",
    "mode": "NULLABLE",
    "fields": [
      {"name": "source", "type": "STRING", "mode": "NULLABLE"},
      {"name": "author", "type": "STRING", "mode": "NULLABLE"},
      {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
      {"name": "modified_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
      {"name": "tags", "type": "STRING", "mode": "REPEATED"},
      {"name": "importance_score", "type": "FLOAT", "mode": "NULLABLE"},
      {"name": "triage_category", "type": "STRING", "mode": "NULLABLE"}
    ]
  },
  {
    "name": "embeddings",
    "type": "FLOAT",
    "mode": "REPEATED",
    "description": "Vector embeddings array (768-3072 dimensions)"
  },
  {
    "name": "chunk_index",
    "type": "INTEGER",
    "mode": "NULLABLE"
  },
  {
    "name": "ingestion_timestamp",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  }
]
```

### Step 2.3: The Exact `bq load` Command

```bash
# Upload data to GCS first
gsutil cp ./knowledge_base_export.jsonl gs://my-personal-data-bucket/knowledge_base/

# Load into BigQuery with partitioning
bq --location=US load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --time_partitioning_type=MONTH \
  --time_partitioning_field=ingestion_timestamp \
  --clustering_fields=source_type,life_domain \
  --autodetect \
  myproject:personal_kb.documents \
  gs://my-personal-data-bucket/knowledge_base/knowledge_base_export.jsonl \
  ./schema.json
```

### Step 2.4: Critical BigQuery Constraints

- **URI format**: Must use `gs://` prefix. No double slashes after bucket name.
- **JSONL only**: Regular JSON arrays are NOT supported. Each line = one record.
- **Nested depth**: Maximum 15 levels of `RECORD` types.
- **Export limit**: `files.export` capped at 10 MB per file.
- **Partitions**: Maximum 4,000 partitions per table.
- **Wildcards**: `gs://bucket/data/*.jsonl` supported, but only one `*` per path.
- **IAM**: Requires `roles/bigquery.dataEditor` + `roles/storage.admin`.

---

## Stage 3: Life Domain Triage & Classification

### Step 3.1: Domain Taxonomy

| Domain | Description | Example Content | Triage Priority |
|--------|-------------|-----------------|-----------------|
| Career & Work | Professional life | Contracts, CVs, schedules | HIGH |
| Finance & Legal | Legal cases, financial records | Court filings, tax docs | CRITICAL |
| Health & Wellness | Medical records | FMLA docs, prescriptions | CRITICAL |
| Learning & Education | Courses, credentials | Certifications, papers | STANDARD |
| Personal & Identity | Immigration, identity | Visa docs, personal statements | HIGH |
| Creative & Projects | Side projects | Business plans, writing | STANDARD |
| Relationships & Social | Communications | Messages, testimonies | STANDARD |
| Home & Logistics | Housing, vehicles | Leases, insurance | HIGH |
| Digital & Technical | Tech, AI tools | ChatGPT exports, configs | REFERENCE |
| Reference & Archive | Saved materials | Policies, guides | ARCHIVE |

### Step 3.2: Automated Classification Pipeline

Use the parallel analysis approach from the Life Intelligence Engine:

```python
# Segment files into batches of 50
# For each segment, run 6-layer analysis:
# Layer 1: Content Inventory (what is this file?)
# Layer 2: Domain Classification (which life domain?)
# Layer 3: Entity Extraction (people, orgs, dates, amounts)
# Layer 4: Key Themes & Patterns
# Layer 5: Importance & Urgency Triage (score 1-10)
# Layer 6: Cross-Reference Signals (connections between docs)

# Output per document:
{
  "document_id": "uuid",
  "primary_domain": "finance_legal",
  "secondary_domains": ["career_work"],
  "importance_score": 8.5,
  "triage_category": "CRITICAL-LEGAL",
  "key_entities": ["IRS", "2024 Tax Return", "$45,000"],
  "cross_references": ["doc_uuid_123", "doc_uuid_456"]
}
```

---

## Stage 4: Vector Embedding Generation

### Step 4.1: Choose Your Embedding Model

| Model | Dimensions | Token Limit | Cost/1M Tokens | Best For |
|-------|-----------|-------------|----------------|----------|
| OpenAI `text-embedding-3-large` | 3072 | 8,191 | $0.13 | General purpose, highest quality |
| Cohere `embed-v3` | 1024 | 512 | $0.10 | Cheapest, multilingual |
| Google `text-embedding-004` | 768 | 2,048 | $0.15 | Google ecosystem integration |
| Voyage AI `voyage-3-large` | 1024 | 32,000 | $0.18 | Longest context, best for docs |

### Step 4.2: Chunking Strategy

**Recommended: Recursive chunking with semantic boundaries**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,           # tokens
    chunk_overlap=50,         # 10% overlap
    separators=["\n\n", "\n", ". ", " "],  # hierarchical splits
    length_function=len
)

chunks = splitter.split_text(document_text)
```

### Step 4.3: Generate Embeddings

```python
import openai

client = openai.OpenAI()

def embed_chunks(chunks):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=chunks  # batch up to 2048 chunks per call
    )
    return [item.embedding for item in response.data]
```

### Step 4.4: Metadata Schema for Each Chunk

```json
{
  "source_id": "uuid-string",
  "source_type": "email | note | pdf | chat | social",
  "author": "string",
  "created_at": "2024-01-15T10:30:00Z",
  "life_domain": "career_work",
  "tags": ["meeting", "project-alpha"],
  "chunk_index": 3,
  "importance_score": 7.5,
  "access_level": "private"
}
```

---

## Stage 5: Platform-Specific Injection

### 5A: Claude Projects (Anthropic)

**The concept**: Upload files to a Claude Project. Claude references them on every conversation turn within that project. The AI "lives in" those files.

**Limits**: 30 MB/file (UI), 500 MB/file (API). 200K context window total.

**Supported formats**: PDF, DOCX, CSV, TXT, HTML, JSON, XLSX, EPUB, RTF, images (JPEG/PNG/GIF/WebP)

```bash
# Step 1: Upload file via Files API (beta)
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@/path/to/knowledge_base.pdf"

# Response: {"id": "file_011CNha8iCJcU1wXNR6q4V8w", ...}

# Step 2: Reference in conversation
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "messages": [{
      "role": "user",
      "content": [{
        "type": "document",
        "source": {"type": "file", "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"}
      }, {
        "type": "text",
        "text": "Based on my knowledge base, what should I prioritize this week?"
      }]
    }]
  }'
```

### 5B: Gemini Gems & NotebookLM (Google)

**The concept**: Upload documents to NotebookLM (up to 50 sources per notebook) or create a custom Gem with persistent instructions and grounding documents.

**Limits**: 500,000 words or 500 MB per source. 2 GB per file via API. 50 sources per notebook.

**Supported formats**: PDF, Google Docs, TXT, CSV, Markdown, MP4, MP3, WAV, images

```python
# Step 1: Upload to Google Cloud Storage for persistence
# (Files via standard Gemini File API expire after 48 hours)
gsutil cp knowledge_base.pdf gs://my-gemini-bucket/docs/

# Step 2: Grant Gemini API access to your bucket
# Grant "Storage Object Viewer" role to:
# generativelanguage.googleapis.com service agent

# Step 3: Reference GCS URI in Gemini API call
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# Upload file (temporary - 48hr expiry)
uploaded = genai.upload_file("knowledge_base.pdf")

# Or reference GCS URI (persistent)
response = model.generate_content([
    {"file_data": {"file_uri": "gs://my-gemini-bucket/docs/knowledge_base.pdf", "mime_type": "application/pdf"}},
    "Based on my knowledge base, what should I prioritize?"
])
```

### 5C: Microsoft Copilot Enterprise (Graph Connectors)

**The concept**: Feed external data into Microsoft Graph via custom Graph Connectors. The Semantic Index vectorizes everything. Copilot then reasons over it using RAG — "the AI lives in the file."

**Limits**: 512 MB per file for semantic indexing. Requires Microsoft 365 E3/E5 + Copilot license.

```bash
# Step 1: Register app in Microsoft Entra admin center
# Grant: ExternalConnection.ReadWrite.All, ExternalItem.ReadWrite.All

# Step 2: Create external connection
curl -X POST https://graph.microsoft.com/v1.0/external/connections \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "id": "personalKnowledgeBase",
    "name": "Personal Knowledge Base",
    "description": "My triaged personal data"
  }'

# Step 3: Define schema with semantic labels
curl -X PATCH https://graph.microsoft.com/v1.0/external/connections/personalKnowledgeBase/schema \
  -d '{
    "baseType": "microsoft.graph.externalItem",
    "properties": [
      {"name": "title", "type": "String", "isSearchable": true, "isRetrievable": true, "labels": ["title"]},
      {"name": "content", "type": "String", "isSearchable": true, "isRetrievable": true},
      {"name": "url", "type": "String", "isRetrievable": true, "labels": ["url"]},
      {"name": "domain", "type": "String", "isSearchable": true, "isRetrievable": true}
    ]
  }'

# Step 4: Ingest external items (your triaged documents)
curl -X PUT https://graph.microsoft.com/v1.0/external/connections/personalKnowledgeBase/items/doc_001 \
  -d '{
    "acl": [{"type": "everyone", "value": "everyone", "accessType": "grant"}],
    "properties": {
      "title": "Q4 Project Plan",
      "content": "Full document text here...",
      "url": "https://mysite.com/docs/q4-plan",
      "domain": "career_work"
    },
    "content": {
      "type": "text",
      "value": "Full searchable content for Semantic Index..."
    }
  }'

# Step 5: Enable inline results in Microsoft 365 admin center
# Admin → Search & intelligence → Customizations → Enable connector
```

### 5D: Grok Collections (xAI)

**The concept**: Upload files to Grok Collections for persistent, semantically-searchable memory across sessions.

**Limits**: 100 MB per file for Collections. 48 MB for standard chat attachments.

**Supported formats**: TXT, MD, CSV, JSON, code files, PDFs

```python
from xai_sdk import Client
from xai_sdk.chat import user, file
import os

client = Client(api_key=os.getenv("XAI_API_KEY"))

# Step 1: Upload file to Collection
with open("knowledge_base.txt", "rb") as f:
    uploaded_file = client.files.upload(f.read(), filename="knowledge_base.txt")

# Step 2: Query with file context (Grok uses attachment_search tool automatically)
chat = client.chat.create(model="grok-4")
chat.append(user("What should I prioritize this week?", file(uploaded_file.id)))
response = chat.send()
```

---

## Stage 6: Self-Retraining Architecture ("The AI Lives in the File")

This is the key innovation — making the embedded data **continuously improve itself** through feedback loops.

### Step 6.1: The Feedback Loop Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERACTION                       │
│  Query → AI Response → User Feedback (accept/reject)    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  EVALUATION LAYER                         │
│  • Response quality scoring (relevance, accuracy)        │
│  • Retrieval precision measurement                       │
│  • Embedding drift detection                             │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  RETRAINING LAYER                         │
│  • Re-chunk poorly performing documents                  │
│  • Re-embed with updated metadata weights                │
│  • Update importance scores based on usage               │
│  • Prune stale/unused embeddings                         │
│  • Add new data from latest interactions                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  VECTOR DB REFRESH                        │
│  • Incremental re-indexing (not full rebuild)            │
│  • Upsert updated vectors                               │
│  • Delete pruned vectors                                 │
│  • Update metadata (importance, freshness scores)        │
└─────────────────────────────────────────────────────────┘
```

### Step 6.2: Implement with LangGraph (Self-Correcting RAG)

```python
from langgraph.graph import MessagesState, StateGraph

# Define the self-correcting workflow
graph_builder = StateGraph(MessagesState)

def generate(state):
    """Generate initial response from retrieved context"""
    docs = retriever.invoke(state["query"])
    response = llm.invoke(f"Context: {docs}\n\nQuery: {state['query']}")
    return {"response": response, "docs": docs}

def reflect(state):
    """Critique the response for accuracy and completeness"""
    critique = llm.invoke(f"""
    Evaluate this response:
    - Is it grounded in the provided context?
    - Are there hallucinations?
    - What's missing?
    Response: {state['response']}
    Context: {state['docs']}
    """)
    return {"critique": critique, "needs_improvement": "issues found" in critique}

def improve(state):
    """Generate improved response based on critique"""
    improved = llm.invoke(f"""
    Original: {state['response']}
    Critique: {state['critique']}
    Generate an improved response addressing the critique.
    """)
    return {"response": improved}

def update_embeddings(state):
    """Update vector DB based on interaction quality"""
    # Boost importance of documents that led to accepted responses
    # Demote documents that led to rejected responses
    for doc in state["docs"]:
        if state["user_accepted"]:
            vector_db.update_metadata(doc.id, {"importance_score": doc.importance + 0.1})
        else:
            vector_db.update_metadata(doc.id, {"importance_score": doc.importance - 0.1})

graph_builder.add_node("generate", generate)
graph_builder.add_node("reflect", reflect)
graph_builder.add_node("improve", improve)
graph_builder.add_node("update_embeddings", update_embeddings)

graph_builder.add_edge("generate", "reflect")
graph_builder.add_conditional_edges("reflect", lambda s: "improve" if s["needs_improvement"] else "update_embeddings")
graph_builder.add_edge("improve", "update_embeddings")
```

### Step 6.3: Scheduled Re-Indexing Pipeline

```bash
# Run daily at 2 AM — re-embed documents with updated importance scores
# Detect embedding drift (cosine similarity between old and new embeddings)
# If drift > 0.15, trigger full re-embedding for that document

# Cron job:
0 2 * * * python3 /home/ubuntu/scripts/reindex_pipeline.py

# The script:
# 1. Scan for new files added since last run
# 2. Check interaction logs for documents with changed importance
# 3. Re-embed only changed/new documents (incremental, not full rebuild)
# 4. Upsert to vector DB
# 5. Sync updated context files to all AI platforms
```

### Step 6.4: Reinforcement Learning for Retrieval

```python
import torch
import torch.nn as nn

class PolicyNetwork(nn.Module):
    """Learns which documents are most relevant for which queries"""
    def __init__(self, input_dim=768, hidden_dim=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim * 2, hidden_dim),  # query + doc embeddings
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)  # relevance score
        )
    
    def forward(self, query_embedding, doc_embedding):
        combined = torch.cat([query_embedding, doc_embedding], dim=-1)
        return self.net(combined)

# Train on user feedback:
# reward = 1.0 if user accepted response, -0.5 if rejected
# Update policy network weights to prefer better document selections
```

---

## Stage 7: Cross-Platform Memory Sync

### Step 7.1: Self-Hosted Shared Memory Server

Deploy a single ChromaDB instance that ALL your AI tools connect to:

```bash
# Deploy ChromaDB
docker run -d -p 8000:8000 chromadb/chroma:1.5.9

# Secure with Tailscale for cross-device access
tailscale up --hostname=memory-server

# All AI agents connect via:
# http://memory-server.tailnet:8000
```

### Step 7.2: CLI Memory Interface

```bash
# Search memory from any AI agent
claude-mem search "project deadlines this week"

# Add new memory from conversation
claude-mem add-fact "Meeting with Sarah moved to Thursday 3pm"

# Add narrative context
claude-mem add-narrative "Completed the BigQuery migration. All personal data now partitioned by life domain."
```

### Step 7.3: Cross-Platform Sync Flow

```
ChromaDB (Source of Truth)
    │
    ├── → Claude Projects (export top-K relevant docs per project)
    ├── → Gemini Gems (sync via GCS bucket)
    ├── → Copilot Enterprise (push via Graph Connector API)
    ├── → Grok Collections (upload via xAI SDK)
    └── → BigQuery (full warehouse backup with embeddings)
```

### Step 7.4: Browser Extension for Real-Time Sync

Install **AI Context Flow** (Chrome extension) to automatically sync memory across ChatGPT, Claude, Gemini, Perplexity, and Grok using organized memory buckets — no manual export/import needed.

---

## Tools & Repositories Master List

| Tool | GitHub/URL | Stars | Purpose |
|------|-----------|-------|---------|
| **Khoj** | https://github.com/khoj-ai/khoj | 20k+ | AI second brain with semantic search |
| **Mem0** | https://github.com/mem0ai/mem0 | 25k+ | Universal memory layer for AI agents |
| **AnythingLLM** | https://github.com/Mintplex-Labs/anything-llm | 30k+ | Full-stack AI app for document chat |
| **LangChain** | https://github.com/langchain-ai/langchain | 100k+ | LLM application framework |
| **LlamaIndex** | https://github.com/run-llama/llama_index | 40k+ | Data framework for LLM apps |
| **ChromaDB** | https://github.com/chroma-core/chroma | 18k+ | Open-source vector database |
| **Self-Hosted Memory** | https://github.com/Crypt0Shmipt0/Self-Hosted-Unlimited-Agent-Memory-For-Claude-Codex-Gemini-Grok | New | Cross-LLM shared memory |
| **Obsidian Copilot** | https://github.com/logancyang/obsidian-copilot | 5k+ | In-vault AI assistant |
| **dlt** | https://github.com/dlt-hub/dlt | 5k+ | Data load tool for BigQuery |
| **DiscordChatExporter** | https://github.com/Tyrrrz/DiscordChatExporter | 8k+ | Export Discord messages |
| **LifeOS** | https://github.com/danielmiessler/LifeOS | 2k+ | Life Operating System on Claude Code |
| **AI Context Flow** | Chrome Web Store | N/A | Cross-platform memory sync extension |
| **RTK** | Rust binary | N/A | Context compression (60-90% reduction) |
| **txtai** | https://github.com/neuml/txtai | 10k+ | All-in-one embeddings database |

---

## Supporting Details Table

| Dimension | Details | Critical Notes |
|-----------|---------|----------------|
| **BigQuery URI Format** | `gs://bucket/path/file.jsonl` | Must use `gs://` prefix, no double slashes, wildcards allowed |
| **BigQuery Load Command** | `bq load --source_format=NEWLINE_DELIMITED_JSON` | Must be JSONL (one record per line), NOT JSON arrays |
| **BigQuery Partitioning** | `--time_partitioning_type=MONTH` | Max 4,000 partitions/table; use MONTH for personal data |
| **Claude File Limit** | 30 MB (UI) / 500 MB (API) | Files API is beta; requires `anthropic-beta` header |
| **Gemini File Limit** | 2 GB per file (API) | Standard File API expires in 48hrs; use GCS for persistence |
| **Copilot Enterprise** | 512 MB per file | Requires E3/E5 + Copilot license; Graph Connector setup |
| **Grok Collections** | 100 MB per file | Uses `attachment_search` tool; semantic search built-in |
| **Embedding Model Choice** | OpenAI 3072d / Cohere 1024d / Google 768d / Voyage 1024d | Changing models = re-embed entire dataset |
| **Chunking Strategy** | Recursive, 512 tokens, 50 token overlap | Semantic chunking best for personal notes |
| **Self-Retraining Trigger** | Cosine drift > 0.15 OR importance score change > 20% | Incremental re-index, never full rebuild |
| **Cross-Platform Sync** | ChromaDB + Tailscale + CLI | Single source of truth, push to all platforms |
| **Feedback Loop** | Accept/reject → importance score ±0.1 | Policy network learns optimal retrieval over time |
| **Data Export Formats** | GDPR archives (JSON/CSV), API exports, SQLite queries | Always request official archives first |
| **Rate Limits (Critical)** | Notion: 3/sec, Gmail: 250 units/sec, Drive: 1M units/min | Exponential backoff mandatory |
| **Authentication** | OAuth 2.0 for Google/Microsoft; API keys for AI platforms | Store in environment variables, never hardcode |

---

## Quick-Start Checklist

- [ ] 1. Set up Google Cloud project + GCS bucket
- [ ] 2. Register OAuth apps (Google, Microsoft, Notion)
- [ ] 3. Request data archives (WhatsApp, Telegram, Discord, Twitter, Reddit)
- [ ] 4. Run extraction scripts for each source
- [ ] 5. Format all data as JSONL with the schema above
- [ ] 6. Upload to GCS: `gsutil cp *.jsonl gs://bucket/`
- [ ] 7. Load into BigQuery: `bq load ...`
- [ ] 8. Run Life Domain triage (parallel analysis)
- [ ] 9. Generate embeddings (OpenAI text-embedding-3-large recommended)
- [ ] 10. Deploy ChromaDB as shared memory server
- [ ] 11. Upload to Claude Projects (Files API)
- [ ] 12. Upload to Gemini (GCS URI method for persistence)
- [ ] 13. Create Graph Connector for Copilot Enterprise
- [ ] 14. Upload to Grok Collections
- [ ] 15. Set up daily re-indexing cron job
- [ ] 16. Install AI Context Flow browser extension
- [ ] 17. Configure Tailscale for cross-device memory access
- [ ] 18. Deploy LangGraph self-correcting pipeline
- [ ] 19. Monitor embedding drift and retrieval quality
- [ ] 20. The AI now "lives in your files" — continuously learning

---

*Generated by Manus AI — Wide Research across 8 parallel lanes using YouTube Video Research, Internet Skill Finder, GitHub Gem Seeker, Manus API, Life Intelligence Engine, and Prompt Optimizer methodologies.*
