# app/embeddings.py
import tensorflow_hub as hub
from langchain_huggingface import HuggingFaceEmbeddings

class UniversalSentenceEncoder:
    def __init__(self):
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

    def embed(self, texts):
        return self.model(texts).numpy()

def get_embeddings_model(model_name):
    if model_name == "USE":
        return UniversalSentenceEncoder()
    elif model_name == "BGE":
        return HuggingFaceEmbeddings(model_name="BAAI/bge-base-en")
    else:
        raise ValueError("Unsupported model")
