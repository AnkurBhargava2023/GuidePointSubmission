# app/search.py
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from config import TOP_K, BM25_WEIGHT, VECTOR_WEIGHT

class Retriever:
    def __init__(self, documents, vectorstore=None):
        self.documents = documents  # List of Document objects.
        self.vectorstore = vectorstore

    def semantic_search(self, query, top_k=TOP_K):
        """
        Performs semantic search using the vectorstore.
        """
        results = self.vectorstore.similarity_search(query, k=top_k)
        return results

    def lexical_search(self, query, top_k=TOP_K):
        """
        Performs BM25-based lexical search.
        """
        bm25_retriever = BM25Retriever.from_documents(self.documents)
        bm25_retriever.k = top_k
        results = bm25_retriever.get_relevant_documents(query)
        return results

    def create_ensemble_retriever(self):
        """
        Creates an ensemble retriever combining BM25 and vector-based retrievers.
        """
        bm25_retriever = BM25Retriever.from_documents(self.documents)
        bm25_retriever.k = TOP_K
        self.hybrid = EnsembleRetriever(
            retrievers=[bm25_retriever, self.vectorstore.as_retriever()],
            weights=[BM25_WEIGHT, VECTOR_WEIGHT]
        )

    def hybrid_search(self, query):
        """
        Performs hybrid search (combining semantic and lexical).
        """
        return self.hybrid.get_relevant_documents(query)
