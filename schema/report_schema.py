from pydantic import BaseModel,Field
from typing import List,Dict

class RiskItem(BaseModel):
    title: str = Field(..., description="Short title of the risk")
    description: str = Field(..., description="Detailed explanation of the risk")
    severity: str = Field(..., description="Low, Medium, or High")

class OpportunityItem(BaseModel):
    title: str = Field(..., description="Short title of the opportunity")
    description: str = Field(..., description="Detailed explanation")
    impact: str = Field(..., description="Low, Medium, or High")

class BusinessReport(BaseModel):
    executive_summary: str
    financial_insights: str
    risks: List[RiskItem]
    opportunities: List[OpportunityItem]
    final_recommendation: str
