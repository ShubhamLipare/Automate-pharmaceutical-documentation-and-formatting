from prompts.prompt import report_prompt
from utils.model_loader import ModelLoader
from graph.state import GraphState
import json
from schema.report_schema import BusinessReport
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
llm=ModelLoader().load_llm()

def report_agent(state:GraphState):
    try:
        structured_llm=llm.with_structured_output(BusinessReport)
        log.info("Inside report agent")
        research_notes=state.get("research_notes","")
        risk_analysis=state.get("risk_analysis","")
        prompt=report_prompt.format(research_notes=research_notes,risk_analysis=risk_analysis)
        response = structured_llm.invoke(prompt)
        log.info(f"Final response:{response}")
        log.info("Generating json respose")
        state["final_report"]=response
        return state
    except Exception as e:
        log.error(f"Error while running report agent:{e}")
        raise CustomException(e)


