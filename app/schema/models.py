from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    documents: List[str]

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    score: float
    text: str
    source: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]