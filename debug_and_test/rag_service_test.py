from backend.app.services.rag_service import RAGService
from ingestion.embedder import TextEmbedder
from ingestion.vector_store import VectorStore

# Setup vector store
docs = [
    "Retrieval Augmented Generation improves LLM answers by adding external knowledge.",
    "FAISS is used for efficient vector similarity search.",
    "Embeddings convert text into numerical vectors.",
]

embedder = TextEmbedder()
store = VectorStore(embedding_dim=384)
store.add(embedder.embed_batch(docs), docs)

# Setup RAG
rag = RAGService(vector_store=store)

# Query
result = rag.query("What is Retrieval Augmented Generation?")

print("Answer:\n", result["answer"])
print("\nContext used:")
for c in result["context"]:
    print("-", c)
