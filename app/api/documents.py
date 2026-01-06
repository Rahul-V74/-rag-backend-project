from fastapi import APIRouter, UploadFile
import os
from app.services.ingestion import process_document

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile):
    filepath = f"{UPLOAD_DIR}/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(await file.read())

    chunks = process_document(filepath, file.filename)
    return {"status": "uploaded", "chunks": chunks}
