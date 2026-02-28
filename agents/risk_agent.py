from prompts.prompt import risk_prompt
from utils.model_loader import ModelLoader
from graph.state import GraphState
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
llm=ModelLoader().load_llm()

def risk_agent(state:GraphState):
    try:
        log.info("Inside Risk agent")
        research_notes=state.get("research_notes","")
        prompt=risk_prompt.format(research_notes=research_notes)
        state["risk_analysis"]=llm.invoke(prompt).content 
        response=state.get("risk_analysis")
        log.info(f"risk analysis:{response}")
        return state
    except Exception as e:
        log.error(f"Error while running risk agent:{e}")
        raise CustomException(e)
