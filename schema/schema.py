from typing import Any,List,TypedDict

class PharmaState(TypedDict):
    raw_documents: List[str]
    retrieved_context: str
    compliance_summary: str
    formatted_output: str
    validation_status: str
