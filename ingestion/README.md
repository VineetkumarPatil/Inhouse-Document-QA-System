# Document Ingestion Pipeline

This module handles **document loading, chunking, and embedding generation**.

## Responsibilities

- Load documents from the local `documents/` directory
- Split documents into overlapping text chunks
- Generate embeddings for each chunk
- Store embeddings in the vector index (FAISS)

## Design Notes

- Ingestion occurs **once at application startup**
- Documents are treated as immutable during runtime
- Chunking strategy prioritizes retrieval accuracy over storage efficiency

## Intentional Constraints

- No dynamic uploads
- No streaming ingestion
- No background re-indexing

These constraints keep the ingestion pipeline simple and transparent,
and allow focus on RAG correctness.
