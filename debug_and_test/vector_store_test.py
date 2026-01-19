from ingestion.embedder import TextEmbedder
from ingestion.vector_store import VectorStore

# Initialize components
embedder = TextEmbedder()
store = VectorStore(embedding_dim=384)

# Sample documents
docs = [
    "Retrieval Augmented Generation combines search with text generation.",
    "Fine-tuning modifies model weights using labeled data.",
    "Vector databases store embeddings for similarity search.",
]

# Embed and store documents
doc_embeddings = embedder.embed_batch(docs)
store.add(doc_embeddings, docs)

# Query
query = "How does RAG work?"
query_embedding = embedder.embed(query)

results = store.search(query_embedding, top_k=2)

print("Top results:")
for text, score in results:
    print(f"- {text} (score={score:.4f})")
