from fastapi import FastAPI
from app.api.documents import router as doc_router
from app.api.query import router as query_router
from app.core.vector_store import init_vector_store

app = FastAPI(title="RAG Backend with Llama")

# Initialize vector store on startup
@app.on_event("startup")
async def startup_event():
    init_vector_store()

app.include_router(doc_router, prefix="/documents")
app.include_router(query_router, prefix="/query")

@app.get("/")
def root():
    return {"message": "RAG Backend Running 🚀"}
