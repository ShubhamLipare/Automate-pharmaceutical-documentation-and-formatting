from src.db import init_db
from schema.report_schema import *
sample = {
    "executive_summary": "Company facing moderate risk.",
    "financial_insights": "Revenue grew 5%.",
    "risks": [
        {
            "title": "High Debt",
            "description": "Debt ratio increasing.",
            "severity": "High"
        }
    ],
    "opportunities": [
        {
            "title": "New Markets",
            "description": "Expansion into Asia.",
            "impact": "Medium"
        }
    ],
    "final_recommendation": "Proceed with caution."
}

report=BusinessReport(**sample)
print(report)

