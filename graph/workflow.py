from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from langgraph.graph import StateGraph,END
from graph.state import GraphState
from agents.report_generate_agent import report_agent
from agents.risk_agent import risk_agent
from agents.research_agent import research_agent
from agents.retriever_node import retriever_node

def human_review_node(state):
    try:
        log.info("\n=========== HUMAN REVIEW ===========\n")
        log.info("Research Notes:\n")
        log.info(state["research_notes"])
        log.info("\nRisk Analysis:\n")
        log.info(state["risk_analysis"])

        if state.get("human_feedback"):
            return {
                "approved": False
            }
        return {
            "approved": True
        }
    except Exception as e:
        log.error(f"Error while taking human review:{e}")
        raise CustomException(e)
    
def review_router(state:GraphState):
    if state.get("approved"):
        return "report_agent"
    else:
        return "research_agent"
    
def build_graph():
    try:
        graph=StateGraph(GraphState)
        #nodes
        graph.add_node("retriever", retriever_node)
        graph.add_node("research_agent",research_agent)
        graph.add_node("risk_agent", risk_agent)
        graph.add_node("human_review", human_review_node)
        graph.add_node("report_agent", report_agent)

        #edegs
        graph.set_entry_point("retriever")
        graph.add_edge("retriever", "research_agent")
        graph.add_edge("research_agent","risk_agent")
        graph.add_edge("risk_agent","human_review")
        graph.add_conditional_edges(
            "human_review",
            review_router,
            {
                "report_agent":"report_agent",
                "research_agent":"research_agent"
            }
        )
        graph.add_edge("report_agent",END)
        return graph.compile()
    except Exception as e:
        log.error(f"Error while buidling graph:{e}")
        raise CustomException(e)
