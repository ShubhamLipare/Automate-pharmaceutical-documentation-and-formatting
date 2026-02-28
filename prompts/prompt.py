from langchain_core.prompts import PromptTemplate

research_prompt = PromptTemplate(
    input_variables=["user_query","retrieved_chunks","human_feedback","research_notes","memory_section"],
    template="""
        You are a professional research analyst.

        Your task:
        - Carefully analyze the user query.
        - Use ONLY the retrieved context to generate research notes.
        - Do NOT introduce external knowledge.
        - If the retrieved context does not contain relevant information to answer the query, respond with:
        "The retrieved context does not contain sufficient relevant information to answer the query."

        If human feedback is provided:
        - Review the previous research notes.
        - Adjust and improve the research notes according to the feedback.
        - Ensure the revised output still strictly uses retrieved context only.

        Consider Past memory section for previous context only.
        ----------------------
        User Query:
        {user_query}

        Retrieved Context:
        {retrieved_chunks}

        Human Feedback:
        {human_feedback}

        Previous research notes:
        {research_notes}

        Past memory section:
        {memory_section}
            """
    )

risk_prompt = PromptTemplate(
    input_variables=["research_notes"],
    template="""
    Based strictly on the research notes below:

    - Identify key risks explicitly supported by the notes.
    - Do NOT introduce new assumptions or external knowledge.
    - Categorize risks where possible (e.g., Strategic, Financial, Operational, Regulatory).
    - Explain why each risk exists using evidence from the research notes.
    - If no clear risks are present, state:
      "No explicit risks identified in the research notes."

    Research Notes:
    {research_notes}

    Provide detailed, structured risk analysis using bullet points.
    """
    )

report_prompt=PromptTemplate(
    input_variables=["research_notes","risk_analysis"],
    template="""
            Create a structured business report in STRICT JSON format
            matching EXACTLY this schema.
            Do NOT include any text outside the JSON.
            Do NOT add extra fields.
            Ensure valid JSON syntax.

            {{
            "executive_summary": "",
            "financial_insights": "",
            "risks": [
                {{
                "title": "",
                "description": "",
                "severity": ""
                }}
            ],
            "opportunities": [
                {{
                "title": "",
                "description": "",
                "impact": ""
                }}
            ],
            "final_recommendation": ""
            }}

            Rules:
            - Base the report strictly on research notes and risk analysis.
            - Do NOT introduce new external knowledge.
            - Keep insights factual and evidence-based.
            - If financial insights are not present in research notes, state "Not explicitly provided in research notes."
            Research:
            {research_notes}

            Risk Analysis:
            {risk_analysis}
            """
        )