from fastapi import APIRouter
from pydantic import BaseModel
from backend_api.services.workflow_service import run_workflow

router = APIRouter()

class QueryRequest(BaseModel):
    session_id: str
    user_query: str
    human_feedback: str | None = None


@router.post("/")
def generate_report(request: QueryRequest):
    result = run_workflow(request)
    return result