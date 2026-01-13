from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    embedding_model:str = Field(..., env="EMBEDDING_MODEL")
    faiss_index_path:str = Field(..., env="FAISS_INDEX_PATH")

    dimension: int = Field(..., env="DIMENSION")
    chunk_size: int = Field(..., env="CHUNK_SIZE")
    overlap: int = Field(..., env="OVERLAP")

    class Config:
        env_file = ".env"

settings = Settings()