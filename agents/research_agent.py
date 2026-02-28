from graph.state import GraphState
from utils.model_loader import ModelLoader
from prompts.prompt import research_prompt
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from memory.sqlite_memory import SqliteMemory
llm=ModelLoader().load_llm()
memory=SqliteMemory()

def research_agent(state:GraphState):
    try:
        log.info("Inside research agent")
        retrieved_chunks=state.get("retrieved_chunks","")
        user_query=state.get("user_query","")
        human_feedback=state.get("human_feedback","")
        research_notes=state.get("research_notes","")

        #getting previous conversation for user query
        past_conversation=memory.fetch_similar_queries(user_query)
        memory_section=""
        for record in past_conversation:
            memory_section+=f"""
            past query:{record[0]}
            past notes:{record[1]}
            past feedback:{record[2]}
            """
        prompt=research_prompt.format(
            user_query=user_query,
            retrieved_chunks=retrieved_chunks,
            human_feedback=human_feedback,
            research_notes=research_notes,
            memory_section=memory_section)
        state["research_notes"]=llm.invoke(prompt).content 
        respose=state.get("research_notes")
        log.info(f"research notes:{respose}")

        #clear hhuman feedback if present to avoid infinite loop
        if state.get("human_feedback"):
            state["human_feedback"]=None
        return state
    except Exception as e:
        log.error(f"Error while running research agent:{e}")
        raise CustomException(e)