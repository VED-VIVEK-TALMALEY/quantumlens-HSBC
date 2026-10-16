"""Client for the isolated embedding microservice."""
import requests
from src.config.settings import settings


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    response = requests.post(
        f"{settings.EMBEDDING_SERVICE_URL}/embed",
        json={"texts": texts},
        timeout=(5, settings.EMBEDDING_SERVICE_TIMEOUT),
    )
    response.raise_for_status()
    payload = response.json()
    vectors = payload.get("embeddings")
    if not isinstance(vectors, list) or len(vectors) != len(texts):
        raise RuntimeError("Embedding service returned an invalid vector count")
    if vectors and any(not isinstance(vector, list) for vector in vectors):
        raise RuntimeError("Embedding service returned a malformed vector")
    return vectors
