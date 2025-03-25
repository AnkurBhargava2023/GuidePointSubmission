# app/pdf_loader.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import os

class PDFLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load_pdfs(self):
        documents = []
        for file in os.listdir(self.folder_path):
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(self.folder_path, file)
                loader = PyPDFLoader(file_path)
                loaded_docs = loader.load()  # Returns list of Document objects.
                for doc in loaded_docs:
                    # Assign metadata: title from filename and source as full file path.
                    doc.metadata["title"] = os.path.splitext(file)[0]
                    doc.metadata["source"] = file_path
                documents.extend(loaded_docs)
        return documents
