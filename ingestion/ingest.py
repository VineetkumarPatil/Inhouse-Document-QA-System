from pathlib import Path

from ingestion.chunker import TextChunker
from ingestion.embedder import TextEmbedder
from ingestion.loader import DocumentLoader
from ingestion.vector_store import VectorStore


class DocumentIngestor:
    """
    Orchestrates the ingestion of text documents by loading files,
    splitting them into chunks, generating embeddings, and storing
    them in a vector store.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        docs_dir: str = "documents",
        chunk_size: int = 500,
        overlap: int = 100,
    ):
        """
        Initialize the DocumentIngestor.

        Args:
            vector_store (VectorStore): The vector store instance used to
            persist embeddings and associated text chunks.

            docs_dir (str): Path to the directory containing TXT documents.
            chunk_size (int): Maximum number of words per text chunk.
            overlap (int): Number of overlapping words between chunks.
        """
        self.docs_dir = Path(docs_dir)
        self.loader = DocumentLoader()
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        self.embedder = TextEmbedder()
        self.vector_store = vector_store

    def ingest_all(self) -> int:
        """
        Load, chunk, embed, and store all TXT files in the documents directory.

        Returns:
            int: The total number of text chunks ingested across all documents.

        Raises:
            FileNotFoundError: If the documents directory does not exist.
        """
        if not self.docs_dir.exists():
            raise FileNotFoundError(f"Documents folder not found: {self.docs_dir}")

        total_chunks = 0

        for file_path in self.docs_dir.glob("*.txt"):
            text = self.loader.load(str(file_path))
            chunks = self.chunker.chunk(text)
            embeddings = self.embedder.embed_batch(chunks)
            self.vector_store.add(embeddings, chunks)
            total_chunks += len(chunks)

        return total_chunks
