from typing import List, Tuple
import faiss
import numpy as np


class VectorStore:
    """
    In-memory FAISS vector store using cosine similarity.
    """

    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.texts: List[str] = []

    def add(self, embeddings: List[List[float]], texts: List[str]) -> None:
        if len(embeddings) != len(texts):
            raise ValueError("Embeddings and texts length mismatch")

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.texts.extend(texts)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        query_vector = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue
            results.append((self.texts[idx], float(score)))

        return results
