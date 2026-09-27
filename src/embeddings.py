from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

model_name = EMBEDDING_MODEL


class EmbeddingModel:

    def __init__(self, model_name: str = model_name):
        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded.")

    def encode(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True
        )