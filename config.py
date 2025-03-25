# config.py
PERSIST_DIRECTORY = "./chroma_db"

# Hybrid search weights for BM25 and vector search.
BM25_WEIGHT = 0.5
VECTOR_WEIGHT = 0.5

# Number of top results to return.
TOP_K = 5

# Chunking parameters.
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50