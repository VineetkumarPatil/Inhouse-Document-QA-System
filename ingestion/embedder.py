from typing import List

from sentence_transformers import SentenceTransformer


class TextEmbedder:
    """
    Wrapper around a SentenceTransformer model for generating text embeddings.
    Designed to be lightweight and suitable for CPU-based RAG pipelines.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.

        Args:
            model_name (str): The name or path of the SentenceTransformer model
                to load for embedding generation.
        """
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> List[float]:
        """
        Generate a normalized embedding vector for a single text input.

        Args:
            text (str): The input text to embed.

        Returns:
            List[float]: A normalized embedding vector representing the input text.
        """
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate normalized embedding vectors for a batch of text inputs.

        Args:
            texts (List[str]): A list of input texts to embed.

        Returns:
            List[List[float]]: A list of normalized embedding vectors,
            one for each input text.
        """
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return vectors.tolist()
