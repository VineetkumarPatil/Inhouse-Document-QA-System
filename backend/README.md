# Backend API Layer

This module implements the **FastAPI-based orchestration layer** for the Inhouse Document QA System.

## Responsibilities

- Expose the `/query` API endpoint
- Validate incoming user questions
- Orchestrate the RAG pipeline:
  - embedding
  - retrieval
  - context assembly
  - prompt construction
  - LLM inference
- Enforce timeout and failure handling for CPU-based inference

## Key Characteristics

- API-first design (no UI assumptions)
- Stateless request handling
- Deterministic behavior
- Explicit error handling

## What This Layer Does *Not* Do

- Does not perform document ingestion
- Does not manage vector storage lifecycle
- Does not contain model weights or inference logic

This separation keeps the API layer thin and predictable.
