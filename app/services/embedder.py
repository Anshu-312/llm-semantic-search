from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model = SentenceTransformer(settings.embedding_model)

def embed_text(texts: list[str]):
    return _model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()