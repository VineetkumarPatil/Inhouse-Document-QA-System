from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(prefix="/query", tags=["RAG"])


class QueryRequest(BaseModel):
    """
    Request model for submitting a query to the RAG system.
    """

    question: str


@router.post("")
def query_rag(request: QueryRequest, req: Request):
    """
    Handle a query request using the RAG service.

    This endpoint retrieves the RAG service from the application state,
    processes the user's question, and returns the generated response.

    Args:
        request (QueryRequest): The incoming request containing the user's question.
        req (Request): The FastAPI request object used to access application state.

    Returns:
        Any: The response produced by the RAG service for the given question.

    Raises:
        HTTPException: If an unexpected error occurs during query processing.
    """
    try:
        rag_service = req.app.state.rag_service
        return rag_service.query(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
