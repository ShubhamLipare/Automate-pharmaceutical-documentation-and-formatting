from fastapi import FastAPI
from backend_api.routes.ingestion import router as ingestion_router
from backend_api.routes.report import router as report_router

app = FastAPI(title="Agentic RAG API")

app.include_router(ingestion_router, prefix="/ingest", tags=["Ingestion"])
app.include_router(report_router, prefix="/report", tags=["Report"])
