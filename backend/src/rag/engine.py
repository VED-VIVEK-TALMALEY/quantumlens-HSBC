# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from functools import lru_cache

from src.rag.retrieval_engine import RetrievalEngine


@lru_cache(maxsize=1)
def get_engine():
    return RetrievalEngine()