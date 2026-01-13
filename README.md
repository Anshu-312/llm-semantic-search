# LLM Semantic Search

A lightweight FastAPI service for ingesting documents, creating embeddings with SentenceTransformers, indexing them in FAISS, and performing semantic search.

**Key features**
- Document chunking with overlap for context preservation.
- Embeddings via SentenceTransformers (`app/services/embedder.py`).
- FAISS index (flat/IVF/HNSW variants in `app/utils/index_factory.py`).
- Persistent FAISS index + associated texts so search survives restarts (`app/services/vector_store.py`).
- Simple REST API: `/ingest` and `/search` implemented in `app/main.py`.

Getting started
---------------
Prerequisites
- Python 3.10+
- A working virtual environment

Install
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Environment
Create a `.env` file at the project root with these variables (example values):

```
EMBEDDING_MODEL=all-MiniLM-L6-v2
FAISS_INDEX_PATH=./data/faiss.index
DIMENSION=384
CHUNK_SIZE=500
OVERLAP=50
```

Run the API
```powershell
uvicorn app.main:app --reload
```

API usage
---------
1) Ingest documents
- Create a JSON payload file `payload.json`:
```json
{
	"documents": [
		"A. Preserving Semantic Continuity\\nEmbeddings are sensitive to context..."
	]
}
```

- On Windows PowerShell use `curl.exe` (PowerShell's `curl` is an alias):
```powershell
curl.exe -X POST "http://localhost:8000/ingest" -H "accept: application/json" -H "Content-Type: application/json" --data-binary "@payload.json"
```

- Or in bash (Linux/macOS):
```bash
curl -X POST "http://localhost:8000/ingest" -H "accept: application/json" -H "Content-Type: application/json" --data-binary @payload.json
```

2) Search
- Create `search_payload.json`:
```json
{
	"query": "where is the cat sitting?",
	"top_k": 5
}
```

- PowerShell (use `curl.exe`):
```powershell
curl.exe -X POST "http://localhost:8000/search" -H "accept: application/json" -H "Content-Type: application/json" --data-binary "@search_payload.json"
```

- Bash example (one-liner JSON):
```bash
curl -X POST "http://localhost:8000/search" -H "accept: application/json" -H "Content-Type: application/json" -d '{"query":"where is the cat sitting?","top_k":5}'
```

Persistence & internals
-----------------------
- The FAISS index is stored at the path set by `FAISS_INDEX_PATH`.
- The repository also persists chunk texts to a file next to the index: `<FAISS_INDEX_PATH>.texts.json` so `VectorStore` can map search indices back to original chunk text. See [app/services/vector_store.py](app/services/vector_store.py).
- Startup loads an existing FAISS index and texts if they exist. See [app/main.py](app/main.py).

Notes & suggestions
-------------------
- `EMBEDDING_MODEL` must match the embedding dimension (`DIMENSION`) you set.
- Consider adding source metadata (filename/page-id) during ingest to surface `source` in `SearchResult`.
- Add tests for ingest/search and CI workflow to validate regressions.

Important files
- [app/main.py](app/main.py)
- [app/services/embedder.py](app/services/embedder.py)
- [app/services/vector_store.py](app/services/vector_store.py)
- [app/services/chunker.py](app/services/chunker.py)
- [app/utils/index_factory.py](app/utils/index_factory.py)
- [payload.json](payload.json) (example created during debugging)

Next steps you might want me to do
- Persist and include `source` metadata on ingest and return it in search results.
- Add unit tests for the chunker and vector store.
- Add a small CLI for batch ingesting files from `data/`.

License
-------
MIT
