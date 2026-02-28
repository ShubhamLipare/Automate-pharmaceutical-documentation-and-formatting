import os
from typing import List
from fastapi import UploadFile
from src.ingestion import DataIngestion
from utils.common import root_path

async def build_knowledge_base(session_id: str, files: List[UploadFile]):

    save_path = os.path.join(root_path(), "data", session_id, "uploads")
    os.makedirs(save_path, exist_ok=True)

    saved_files = []

    for file in files:
        file_path = os.path.join(save_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        saved_files.append(file_path)

    ingestion = DataIngestion(session_id=session_id)

    ingestion.build_retriever(
        uploaded_files=saved_files,
        chunk_size=1000,
        chunk_overlap=200,
        k=5
    )

    return "Knowledge base built successfully."