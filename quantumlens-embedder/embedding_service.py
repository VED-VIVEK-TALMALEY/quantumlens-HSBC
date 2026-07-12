from sentence_transformers import SentenceTransformer

from config import MODEL_NAME


class EmbeddingService:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        print("Model loaded successfully.")

    def embed(self, texts: list[str]) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()