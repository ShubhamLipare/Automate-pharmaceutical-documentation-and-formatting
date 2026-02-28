from graph.state import GraphState
from langchain_community.vectorstores import FAISS
from utils.common import root_path
from utils.model_loader import ModelLoader
import os
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from src.ingestion import DataIngestion


def retriever_node(state: GraphState):
    try:
        log.info(f"retriver state:{state}")
        index_path = os.path.join(root_path(),"data",state.get("session_id"), "faiss_index")
        embedding_model = ModelLoader().load_embedding_model()
        log.info(f"loading local faiss index from path {index_path}")
        vs = FAISS.load_local(
            index_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )
        retriever = vs.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(state["user_query"])
        chunks = [doc.page_content for doc in docs]
        state["retrieved_chunks"]=chunks
        return state
    except Exception as e:
        log.error(f"Error while running retrive node agent:{e}")
        raise CustomException(e)