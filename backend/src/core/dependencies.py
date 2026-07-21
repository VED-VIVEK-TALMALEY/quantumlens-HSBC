from functools import lru_cache

from src.rag.rag_pipeline import ask
from src.warehouse.query_service import QueryService


@lru_cache
def get_query_service():
    return QueryService()


@lru_cache
def get_rag():
    return ask