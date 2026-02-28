from graph.workflow import build_graph
from src.ingestion import DataIngestion
from pathlib import Path
from memory.sqlite_memory import SqliteMemory

class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()
if __name__ == "__main__":
    file_path=Path(r"C:\Users\Shubham\Downloads\company-research-paper-example.pdf")
    ingestion = DataIngestion()
    dummy_file=DummyFile(file_path)
    retriever = ingestion.build_retriever([dummy_file], 1000, 200, 5)
    print("Buiding graph")
    app = build_graph()
    initial_state = {
        "user_query": """Generate detailed research notes on Volkswagen Group's operational strategy.
                        Identify key strategic and regulatory risks.
                        Provide a final executive-level report with recommendations.""",
        "session_path": ingestion.session_path
    }
    result = app.invoke(initial_state)
    #SqliteMemory.save_submission(result)
    print("\n\n========= FINAL REPORT =========\n")
    print(result["final_report"])