# AnythingLLM — where RAG breaks

Interactive guide: **[Where RAG Breaks](https://claude.ai/code/artifact/aba631e3-b766-4b27-8e86-c9f3d28b9b49)**
Source: [`where-rag-breaks.html`](where-rag-breaks.html) — self-contained, no build step.

---

## First, the correction

AnythingLLM **Pro** is a desktop add-on — dictation, screen-capture Q&A,
autocomplete. It touches nothing in RAG. Every retrieval setting below is free.

## The seven fixes, in order of yield

| # | Failure | Fix |
|---|---|---|
| 1 | Uploading ≠ embedding | Select file → **Move to Workspace**, wait for it to finish |
| 2 | Retrieval gate closed | ⚙ → Vector Database: Threshold **No restriction**, Search **Accuracy Optimized**, Snippets **4–6** |
| 3 | Chunks too small to hold an idea | Embedder model → **nomic-embed-text-v1**, then re-embed |
| 4 | Wrong chat mode | **Query** = documents only · **Chat** = documents + model knowledge · **Agent** = tools |
| 5 | Whole-document task | Don't embed — **attach** or **pin** |
| 6 | Changed embedder or vector DB | Delete every document, re-embed from scratch |
| 7 | `fetch failed` | Unblock `huggingface.co`, `api.huggingface.co`, `cdn.anythingllm.com` · Windows VC++ Redistributable v14.x · CPU needs AVX2 |

## Numbers the docs don't state

Read from `Mintplex-Labs/anything-llm`, not from docs.anythingllm.com.

`server/utils/TextSplitter/index.js`
- default chunk size **1,000**, overlap **20**
- `determineMaxChunkSize()` silently clamps to the embedder's ceiling

`server/utils/EmbeddingEngines/native/constants.js` — max chunk length, characters

| Model | Ceiling | Concurrency |
|---|---|---|
| `Xenova/all-MiniLM-L6-v2` *(default)* | 1,000 | 25 |
| `MintplexLabs/multilingual-e5-small` | 1,000 | 5 |
| `Xenova/nomic-embed-text-v1` | **16,000** | 5 |

This is fix 3. Sixteen times the room per chunk, same product, one dropdown.

## Two facts that cost the most to learn late

- **Embedder and vector database are system-wide**, not per-workspace. Changing
  either is a rebuild, not a settings change.
- **Retrieval competes.** Every unrelated document in a workspace crowds out the
  right one. Split by subject early.

## Verify, don't trust

Ask something whose answer you know is in the file, then open the citations under
the response. If the cited chunks don't contain the answer, the problem is
retrieval — not the model.

---

Menu names track the v1.15 release line. Statements are either from
docs.anythingllm.com or marked as read from source above; where the docs are
silent, this says so rather than guessing.
