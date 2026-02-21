from utils.config_loader import load_config
from utils.model_loader import ModelLoader
from utils.common import *
import os
import json
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import CustomException
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import hashlib
from src.document_loader import DocumentLoader

class FaissManager:
    def __init__(self):
        self.index_path=os.path.join(root_path(),"faiss_index")
        os.makedirs(self.index_path,exist_ok=True)
        self.meta_path = os.path.join(self.index_path,"ingested_meta.json")
        self._meta={"rows": {}}
        self.embedding_model=ModelLoader().load_embedding_model()
        self.vectorestore=None

        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self._meta = json.load(f)

    def _exists(self):
        return os.path.exists(self.index_path) and os.path.exists(os.path.join(self.index_path,"index.faiss"))
    
    @staticmethod
    def _deduplicate(texts:str,md):
        src=md.get("source") or md.get("file_path")
        page=md.get("page")
        id=md.get("chunk_id")
        if src is not None:
            return f"{src}::{page if page is not None else ''}::{id if id is not None else ''}"
        return hashlib.sha256(texts.encode("utf-8")).hexdigest()
    
    def _save_meta(self):
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self._meta, f, indent=4)

    def load_or_create_index(self,documents):
        log.info(f"Checking for existing FAISS index at {self.index_path}")
        if self._exists():
            log.info("Loading existing FAISS index.")
            self.vectorestore=FAISS.load_local(str(self.index_path), self.embedding_model,allow_dangerous_deserialization=True)
            return self.vectorestore
        if not documents:
            raise CustomException("No documents provided to create FAISS index.")
        log.info("Creating new FAISS index.")
        self.vectorestore=FAISS.from_documents(documents=documents, embedding=self.embedding_model)
        # Update metadata for initial documents
        for doc in documents:
            key = self._deduplicate(doc.page_content, doc.metadata)
            if key not in self._meta["rows"]:
                self._meta["rows"][key] = True
        self._save_meta()
        self.vectorestore.save_local(str(self.index_path))
        return self.vectorestore
    
    def add_documents(self, documents):
        log.info(f"Adding documents to FAISS index at {self.index_path}")
        log.info(f"documents to add: {len(documents)}")
        new_docs=[]
        if not self.vectorestore:
            raise CustomException("No FAISS index loaded.")
        for doc in documents:
            key=self._deduplicate(doc.page_content, doc.metadata)
            if key in self._meta["rows"]:
                log.info(f"Skipping duplicate document with key: {key}")
                continue
            self._meta["rows"][key]=True
            new_docs.append(doc)
        if new_docs:
            self.vectorestore.add_documents(new_docs)
            self.vectorestore.save_local(str(self.index_path))
            self._save_meta()
            log.info(f"Added {len(new_docs)} new documents to FAISS index.") 

class DataIngestion:
    def __init__(self):
        self.session_id = generate_session_id()
        self.session_path = os.path.join(root_path(),"data",self.session_id)
        #self.uploads_path = self.session_path / "uploads"
        self.uploads_path = os.path.join(root_path(),"data","uploads")
        self.doc_loader=DocumentLoader()
        self.loaded_doc_path=os.path.join(root_path(),"data",self.session_id,"loaded_doc")

    def chunk_and_store(self,documents,chunk_size,chunk_overlap):
        try:
            log.info(f"Chunking documents for session {self.session_id} with chunk size {chunk_size} and overlap {chunk_overlap}.")
            chunked_docs_path = os.path.join(self.session_path,"chunked_docs")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
            chunks = text_splitter.split_documents(documents)
            #adding chunk id to metadata for each chunk
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = i
            #saving chunked docs in local
            os.makedirs(chunked_docs_path, exist_ok=True)
            with open(os.path.join(chunked_docs_path,"chunked_docs.txt"), "w", encoding="utf-8") as f:
                for i, doc in enumerate(chunks):
                    f.write(f"{'*'*40} chunk {i+1} {'*'*40}\n")
                    f.write(doc.page_content + "\n")
            log.info(f"Successfully chuncked data into {len(chunks)} chunks in session {self.session_id}.")
            return chunks
        except CustomException as ce:
            log.error(f"Data ingestion failed: {ce}")
            raise CustomException("Data ingestion process failed.", ce) from ce
        
    def build_retriever(self,uploaded_files,chunk_size,chunk_overlap,k):
        try:
            log.info(f"Starting retriever build for session {self.session_id} with {len(uploaded_files)} files.")
            saved_files = save_uploaded_file(uploaded_files, self.uploads_path)
            documents = self.doc_loader.load_doc(saved_files,self.loaded_doc_path)
            chunks = self.chunk_and_store(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            fm = FaissManager()
            vs=fm.load_or_create_index(chunks)
            fm.add_documents(chunks)
            log.info(f"Retriever built successfully for session {self.session_id}.")
            #return vs.as_retriever(search_type="similarity", search_kwargs={"k":k})
        
        except CustomException as ce:
            log.error(f"Building retriever failed: {ce}")
            raise CustomException("Building retriever failed.", ce) from ce
        

class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()
if __name__ == "__main__":
    ingestion = DataIngestion()
    file_path=Path(r"C:\Users\Shubham\Downloads\Attention Is All You Need.pdf")
    dummy_file=DummyFile(file_path)
    retriever = ingestion.build_retriever([dummy_file], chunk_size=1000, chunk_overlap=200, k=5)
    print(f"Processed in session: {ingestion.session_id}")