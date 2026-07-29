# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from src.utils.logger import logger
from src.rag.rag_pipeline import ask
from src.rag.retrieval_engine import RetrievalEngine

_engine = None


def get_engine():

    global _engine

    if _engine is None:
        _engine = RetrievalEngine()

    return _engine


def ask_question(question: str):

    logger.info(
        f"/ask : {question}"
    )

    return ask(question)


def search_metrics(
    query: str,
    top_k: int = 5
):

    logger.info(
        f"/search : {query}"
    )

    engine = get_engine()

    return engine.search(
        query=query,
        top_k=top_k
    )