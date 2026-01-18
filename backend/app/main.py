from fastapi import FastAPI

from ingestion.vector_store import VectorStore
from ingestion.ingest import DocumentIngestor
from backend.app.api.query import router as query_router
from backend.app.services.rag_service import RAGService


def create_app() -> FastAPI:
    app = FastAPI(
        title="In-house Document QA System",
        version="1.0.0",
    )

    # Create shared vector store
    vector_store = VectorStore(embedding_dim=384)

    # Ingest documents at startup
    ingestor = DocumentIngestor(vector_store=vector_store)
    chunks = ingestor.ingest_all()
    print(f"[Startup] Ingested {chunks} document chunks")

    # Attach RAG service to app state
    app.state.rag_service = RAGService(vector_store=vector_store)

    # Routes
    app.include_router(query_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
