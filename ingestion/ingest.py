from pathlib import Path
from ingestion.loader import DocumentLoader
from ingestion.chunker import TextChunker
from ingestion.embedder import TextEmbedder
from ingestion.vector_store import VectorStore


class DocumentIngestor:
    """
    Ingests all TXT files from a directory.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        docs_dir: str = "documents",
        chunk_size: int = 500,
        overlap: int = 100,
    ):
        self.docs_dir = Path(docs_dir)
        self.loader = DocumentLoader()
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        self.embedder = TextEmbedder()
        self.vector_store = vector_store

    def ingest_all(self) -> int:
        """
        Load, chunk, embed, and store all TXT files.
        Returns total chunks ingested.
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
