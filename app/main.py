from fastapi import FastAPI
from app.core.config import settings
from app.schema.models import IngestRequest, SearchRequest, SearchResult, SearchResponse
from app.services.embedder import embed_text
from app.services.chunker import chunk_text
from app.services.vector_store import VectorStore
from app.utils.index_factory import flat_index

app = FastAPI(
    title="LLM Semantic Search API",
    description="An API for ingesting documents and performing semantic search using LLM embeddings.",
    version="1.0.0"
    )

# Initialize the sentence transformer model and index
DIM = settings.dimension
index = flat_index(DIM)
# Attempt to load an existing persisted index and texts, falling back to a fresh index
store = VectorStore.load(index)

@app.post("/ingest", status_code=201)
async def ingest(request: IngestRequest):
    """Ingests by chunking and embedding them, then storing in the vector index."""
    all_chunks = []
    for doc in request.documents:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)

    vectors = embed_text(all_chunks)
    store.add(vectors, all_chunks)
    store.save()

    return {"chunks_indexed": len(all_chunks)}

@app.post("/search", response_model=SearchResponse, status_code=200)
async def search(request: SearchRequest):
    """Performs semantic search on the indexed documents."""
    query_vector = embed_text([request.query])[0]
    results = store.search(query_vector, top_k=request.top_k)

    return SearchResponse(results=results)

@app.get("/", status_code=200)
async def root():
    """Root endpoint providing basic information about the API."""
    return {
        "message": "Welcome to the LLM Semantic Search API. Use /ingest to add documents and /search to perform semantic searches."
    }
