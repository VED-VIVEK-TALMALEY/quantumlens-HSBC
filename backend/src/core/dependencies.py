# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from functools import lru_cache

from src.rag.rag_pipeline import ask
from warehouse.query_service import QueryService


@lru_cache
def get_query_service():
    return QueryService()


@lru_cache
def get_rag():
    return ask