import streamlit as st
import requests
import uuid

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Agentic RAG System", layout="wide")

# ===============================
# SESSION INITIALIZATION
# ===============================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "username" not in st.session_state:
    st.session_state["username"] = None

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "reports_history" not in st.session_state:
    st.session_state["reports_history"] = []

if "current_query" not in st.session_state:
    st.session_state["current_query"] = None

# ===============================
# LOGIN SCREEN
# ===============================
if not st.session_state["authenticated"]:

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # Simple demo authentication
        if username and password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["session_id"] = str(uuid.uuid4())
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.title("⚙️ Controls")
    st.write(f"Logged in as: **{st.session_state['username']}**")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ===============================
# MAIN UI
# ===============================
st.title("📊 Agentic RAG Research Assistant")

# ===============================
# Upload Section
# ===============================
st.subheader("📂 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF, DOCX, CSV, TXT",
    type=["pdf", "docx", "csv", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Build Knowledge Base"):
        with st.spinner("Uploading and building knowledge base..."):

            files = [
                ("files", (file.name, file.getvalue(), file.type))
                for file in uploaded_files
            ]

            response = requests.post(
                f"{API_BASE}/ingest",
                files=files,
                data={
                    "session_id": st.session_state["session_id"],
                    "username": st.session_state["username"]
                }
            )

            if response.status_code == 200:
                st.success("Knowledge base built successfully.")
            else:
                st.error(response.text)

# ===============================
# Query Section
# ===============================
st.subheader("🔎 Ask a Question")

query = st.text_area("Enter your research query")

if st.button("Generate Report"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Running multi-agent workflow..."):

            st.session_state["current_query"] = query

            payload = {
                "session_id": st.session_state["session_id"],
                "user_query": query,
                "human_feedback": None
            }

            response = requests.post(
                f"{API_BASE}/report",
                json=payload
            )

            if response.status_code == 200:
                st.session_state["reports_history"].append(response.json())
            else:
                st.error(response.text)

# ===============================
# Display Report History
# ===============================
if st.session_state["reports_history"]:

    st.subheader("📑 Report Versions")

    for idx, report in enumerate(st.session_state["reports_history"]):
        with st.expander(f"Report Version {idx + 1}", expanded=(idx == len(st.session_state["reports_history"]) - 1)):

            st.markdown("### Executive Summary")
            st.write(report["executive_summary"])

            st.markdown("### Financial Insights")
            st.write(report["financial_insights"])

            st.markdown("### Risks")
            for risk in report["risks"]:
                st.write(f"- **{risk['title']}** ({risk['severity']})")
                st.write(f"  {risk['description']}")

            st.markdown("### Opportunities")
            for opp in report["opportunities"]:
                st.write(f"- **{opp['title']}** ({opp['impact']})")
                st.write(f"  {opp['description']}")

            st.markdown("### Final Recommendation")
            st.write(report["final_recommendation"])

# ===============================
# Human-in-the-Loop Section
# ===============================
if st.session_state["reports_history"]:

    st.subheader("🧑‍💼 Provide Feedback")

    with st.form("feedback_form", clear_on_submit=True):

        feedback = st.text_area("Suggest improvements")

        submitted = st.form_submit_button("Refine Report")

        if submitted:

            if not feedback.strip():
                st.warning("Please provide feedback before refining.")
            else:
                with st.spinner("Refining report..."):

                    payload = {
                        "session_id": st.session_state["session_id"],
                        "user_query": st.session_state["current_query"],
                        "human_feedback": feedback
                    }

                    response = requests.post(
                        f"{API_BASE}/report",
                        json=payload
                    )

                    if response.status_code == 200:
                        st.session_state["reports_history"].append(response.json())
                        st.success("Report refined successfully.")
                        st.rerun()
                    else:
                        st.error(response.text)