from typing import List, Tuple

import faiss  # type: ignore[import-untyped]
import numpy as np


class VectorStore:
    """
    In-memory vector store backed by FAISS using cosine similarity
    (via inner product on normalized vectors).
    """

    def __init__(self, embedding_dim: int):
        """
        Initialize the FAISS vector store.

        Args:
            embedding_dim (int): Dimensionality of the embedding vectors
                that will be stored in the index.
        """
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.texts: List[str] = []

    def add(self, embeddings: List[List[float]], texts: List[str]) -> None:
        """
        Add embedding vectors and their corresponding texts to the store.

        Args:
            embeddings (List[List[float]]): A list of embedding vectors.
            texts (List[str]): A list of text chunks corresponding to
                each embedding.

        Raises:
            ValueError: If the number of embeddings does not match
                the number of texts.
        """
        if len(embeddings) != len(texts):
            raise ValueError("Embeddings and texts length mismatch")

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.texts.extend(texts)

    def search(
        self, query_embedding: List[float], top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Search for the most similar text chunks to a query embedding.

        Args:
            query_embedding (List[float]): The embedding vector of the query.
            top_k (int): The maximum number of results to return.

        Returns:
            List[Tuple[str, float]]: A list of (text, similarity_score) tuples
            ordered by descending similarity.
        """
        query_vector = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue
            results.append((self.texts[idx], float(score)))

        return results
