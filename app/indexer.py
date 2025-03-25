# app/indexer.py
from langchain_chroma import Chroma
from config import PERSIST_DIRECTORY

def index_documents(docs, embedding_model):
    """
    Indexes the given documents into a Chroma vector store.
    The documents (with metadata) are stored so that both content and metadata
    are available during search.
    """
    vectordb = Chroma(
        collection_name="pdf_collection",
        embedding_function=embedding_model,
        persist_directory=PERSIST_DIRECTORY
    )
    vectordb.add_documents(docs)
    return vectordb
