"""Client for the isolated embedding microservice with seamless local fallback."""
import requests
from src.config.settings import settings
from src.utils.logger import logger

_local_model = None


def _get_local_model():
    global _local_model
    if _local_model is None:
        from sentence_transformers import SentenceTransformer
        _local_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _local_model


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    try:
        response = requests.post(
            f"{settings.EMBEDDING_SERVICE_URL}/embed",
            json={"texts": texts},
            timeout=(2, min(5.0, settings.EMBEDDING_SERVICE_TIMEOUT)),
        )
        response.raise_for_status()
        payload = response.json()
        vectors = payload.get("embeddings")
        if isinstance(vectors, list) and len(vectors) == len(texts):
            if all(isinstance(v, list) for v in vectors):
                return vectors
    except Exception as exc:
        logger.warning(
            "Embedding service at %s unreachable (%s), falling back to local SentenceTransformer",
            settings.EMBEDDING_SERVICE_URL,
            exc,
        )

    # Local in-process fallback for tests and standalone operation
    model = _get_local_model()
    embeddings = model.encode(texts, show_progress_bar=False).tolist()
    return embeddings
