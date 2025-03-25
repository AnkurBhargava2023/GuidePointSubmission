# api/main.py
import os
import time
import asyncio
import concurrent.futures
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import uvicorn
from contextlib import asynccontextmanager

# Import our modules from the app package.
from app.pdf_loader import PDFLoader
from app.chunking import chunk_documents
from app.embeddings import get_embeddings_model
from app.indexer import index_documents
from app.search import Retriever
from langchain_chroma import Chroma
from config import PERSIST_DIRECTORY, TOP_K

# Global variables for our index (vectorstore) and retriever.
retriever = None
vectordb = None

# ThreadPoolExecutor for running blocking calls.
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

async def initialize_index(pdf_folder: str):
    """
    Initializes the index:
      1. Loads PDFs using PDFLoader.
      2. Chunks the loaded documents.
      3. Loads the embedding model.
      4. Loads (or indexes) documents into a Chroma vector store.
      5. Creates the Retriever.
    Returns the Retriever and vectorstore.
    """
    loader = PDFLoader(pdf_folder)
    loaded_docs = loader.load_pdfs()
    if not loaded_docs:
        raise Exception("No PDFs loaded.")

    chunked_docs = chunk_documents(loaded_docs)
    if not chunked_docs:
        raise Exception("Chunking produced no documents.")

    embedding_model = get_embeddings_model("BGE")

    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        vectordb_local = Chroma(
            collection_name="pdf_collection",
            embedding_function=embedding_model,
            persist_directory=PERSIST_DIRECTORY
        )
        print("Loaded existing vector database.")
    else:
        vectordb_local = index_documents(chunked_docs, embedding_model)
        print("Created new vector database and indexed documents.")

    retriever_local = Retriever(chunked_docs, vectorstore=vectordb_local)
    return retriever_local, vectordb_local

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever, vectordb
    pdf_folder = "/Users/ankurbhargava/Downloads/GuidePointFinalSubmission/Files"  # Adjust this folder path as needed.
    try:
        retriever, vectordb = await initialize_index(pdf_folder)
    except Exception as e:
        print(f"Error initializing index: {e}")
    yield
    # Optionally: include shutdown code here if needed.

app = FastAPI(
    title="PDF Q&A API",
    description="API for querying PDF index for question answering",
    version="1.0",
    lifespan=lifespan
)

# Pydantic request model.
class QueryRequest(BaseModel):
    query: str = Field(..., description="The search query or question.")
    search_type: str = Field("semantic", description="Search type: semantic, lexical, or hybrid.")

# Pydantic response models.
class DocumentResponse(BaseModel):
    title: str
    source: str
    content: str

class QueryResponse(BaseModel):
    documents: List[DocumentResponse]
    latency: float = Field(..., description="Query processing latency in seconds.")

@app.post("/query", response_model=QueryResponse)
async def query_index(request: QueryRequest):
    start_time = time.time()

    if not retriever or not vectordb:
        raise HTTPException(status_code=500, detail="Index not initialized.")

    search_type = request.search_type.lower()
    if search_type not in ["semantic", "lexical", "hybrid"]:
        raise HTTPException(status_code=400, detail="Invalid search type.")

    loop = asyncio.get_event_loop()
    try:
        if search_type == "semantic":
            results = await loop.run_in_executor(executor, retriever.semantic_search, request.query, TOP_K)
        elif search_type == "lexical":
            results = await loop.run_in_executor(executor, retriever.lexical_search, request.query, TOP_K)
        elif search_type == "hybrid":
            await loop.run_in_executor(executor, retriever.create_ensemble_retriever)
            results = await loop.run_in_executor(executor, retriever.hybrid_search, request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    docs_response = []
    for doc in results:
        title = doc.metadata.get("title", "Unknown") if hasattr(doc, "metadata") else "Unknown"
        source = doc.metadata.get("source", "Unknown") if hasattr(doc, "metadata") else "Unknown"
        content = doc.page_content
        snippet = content[:200] + "..." if len(content) > 200 else content
        docs_response.append(DocumentResponse(title=title, source=source, content=snippet))
    
    latency = time.time() - start_time
    return QueryResponse(documents=docs_response, latency=latency)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
