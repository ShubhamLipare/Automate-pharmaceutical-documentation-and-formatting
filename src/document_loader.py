from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from utils.config_loader import load_config
from utils.model_loader import ModelLoader
from utils.common import *
from langchain_community.document_loaders import PyMuPDFLoader,Docx2txtLoader,CSVLoader,TextLoader
import os
import re


class DocumentLoader:
    SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".csv", ".txt"]

    def __init__(self):
        self.root_path=root_path()
 
    def load_doc(self,files):
        try:
            documents=[]
            for file in files:
                extension=os.path.splitext(file)[1].lower()
                log.info(f"file:{file},ext:{extension}")
                if extension not in self.SUPPORTED_EXTENSIONS:
                    raise CustomException(f"Unsupported filetype {extension}. SUPPORTED:{self.SUPPORTED_EXTENSIONS} ")              
                log.info(f"Loading document:{file}")

                if extension == ".pdf":
                    loader = PyMuPDFLoader(file)
                elif extension == ".docx":
                    loader = Docx2txtLoader(file)
                elif extension == ".csv":
                    loader = CSVLoader(file)
                elif extension == ".txt":
                    loader = TextLoader(file)

                documents.extend(loader.load())

            #saving loaded document for validation on local
            loaded_doc_path=os.path.join(self.root_path,"data","loaded_doc")
            os.makedirs(loaded_doc_path,exist_ok=True)
            file_path=os.path.join(loaded_doc_path,"loaded_doc.txt")
            with open(file_path,"w",encoding="utf-8") as f:
                for i, doc in enumerate(documents):
                    f.write(f"{'*'*40} Document {i+1} {'*'*40}\n")
                    f.write(doc.page_content + "\n")

            log.info("Document loaded successfully.")
            return documents
        except Exception as e:
            log.error(f"Error while loading document, {e}")
            raise CustomException(f"Error while loading document, {e}")

class DummyFile:
    def __init__(self,file_path):
        self.name=Path(file_path).name
        self.file_path=file_path 
    def getbuffer(self):
        return open(self.file_path,"rb").read()
     
if __name__ == "__main__":
    doc_loader = DocumentLoader()
    file_path=Path(r"C:\Users\Shubham\Downloads\Attention Is All You Need.pdf")
    dummy_file=DummyFile(file_path)
    save_path=os.path.join(root_path(),"data","saved_files")
    files=save_uploaded_file([dummy_file],save_path)
    doc_loader.load_doc(files)






