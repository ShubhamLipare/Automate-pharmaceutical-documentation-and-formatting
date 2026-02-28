from fastapi import APIRouter, UploadFile, File, Form
from backend_api.services.ingestion_service import build_knowledge_base
from typing import List

router = APIRouter()

@router.post("/")
async def ingest_documents(
    session_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    result = await build_knowledge_base(session_id, files)
    return {"message": result}