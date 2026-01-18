from typing import List
from sentence_transformers import SentenceTransformer


class TextEmbedder:
    """
    CPU-friendly embedding model for RAG.
    Uses all-MiniLM-L6-v2 (384 dimensions).
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> List[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()
