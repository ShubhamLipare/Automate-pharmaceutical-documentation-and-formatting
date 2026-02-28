from typing import TypedDict, List, Optional
from schema.report_schema import BusinessReport


class GraphState(TypedDict):
    session_id: Optional[str]
    user_query: str
    session_path:str
    retrieved_chunks: List[str]

    research_notes: Optional[str]
    risk_analysis: Optional[str]
    opportunity_analysis: Optional[str]
    financial_analysis: Optional[str]

    human_feedback: Optional[str]
    approved: Optional[bool]

    final_report: Optional[BusinessReport]
    


