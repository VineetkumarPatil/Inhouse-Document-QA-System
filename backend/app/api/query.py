from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/query", tags=["RAG"])


class QueryRequest(BaseModel):
    question: str


@router.post("")
def query_rag(request: QueryRequest, req: Request):
    try:
        rag_service = req.app.state.rag_service
        return rag_service.query(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
