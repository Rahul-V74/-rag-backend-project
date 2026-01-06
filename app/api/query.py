from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.retrieval import query_rag

router = APIRouter()

@router.post("/")
async def ask_question(req: QueryRequest):
    answer, sources = query_rag(req.question)
    return QueryResponse(answer=answer, sources=sources)
