from functools import lru_cache

from src.rag.retrieval_engine import RetrievalEngine


@lru_cache(maxsize=1)
def get_engine():
    return RetrievalEngine()