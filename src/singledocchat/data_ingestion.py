import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException  
from utils.model_loader import ModelLoader
from datetime import datetime, timezone

class SingleDocumentIngestor:
    def __init__(self, data_dir:str = "data/single_document_chat", faiss_dir: str = "faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)

            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            self.model_loader = ModelLoader()

            self.log.info("SingleDocumentIngestor initialized successfully", temp_path = str(self.data_dir), faiss_path = str(self.faiss_dir))

        except Exception as e:
            print(f"Error initializing SingleDocumentIngestor: {e}")
            raise DocumentPortalException("Initialization error in SingleDocumentIngestor", sys)

    def ingest_files(self,uploaded_files):
        try:
            documents = []

            for uploaded_file in uploaded_files:
                unique_file_name = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.pdf"
                temp_path = self.data_dir / unique_file_name
                with open(temp_path, "wb") as f_out:
                    f_out.write(uploaded_file.getbuffer())
                self.log.info("PDF saved for ingestion", filename = uploaded_file.name)
                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)
            self.log.info("PDF files loaded", count = len(documents))
            return self._create_retriever(documents)


            
        except Exception as e:
            self.log.error("Document Ingestion Failed", error=str(e))
            raise DocumentPortalException("Error ingesting files", sys)
        
    def _create_retriever(self, documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)
            chunks = splitter.split_documents(documents)
            self.log.info("Documents split into chunks", count = len(chunks))

            embeddings = self.model_loader.load_embeddings()
            vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)

            # saving the FAISS index

            vectorstore.save_local(str(self.faiss_dir))
            self.log.info("FAISS index created and saved", path = str(self.faiss_dir))

            retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})
            self.log.info("Retriever created successfully")
            return retriever

        except Exception as e:
            self.log.error("Error creating retriever", error=str(e))
            raise DocumentPortalException("Error creating FAISS retriever", sys)