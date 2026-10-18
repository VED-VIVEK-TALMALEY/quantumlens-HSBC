# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from typing import Optional
from src.utils.logger import logger
from src.rag.rag_pipeline import ask
from src.rag.retrieval_engine import RetrievalEngine

_engine = None


def get_engine():

    global _engine

    if _engine is None:
        _engine = RetrievalEngine()

    return _engine


def ask_question(question: str, conversation_id: Optional[str] = None):

    logger.info(
        f"/ask (consolidated via orchestrator) : {question} [session: {conversation_id or 'default'}]"
    )

    try:
        from src.api.services.agent_service import process_question
        result = process_question(question, conversation_id=conversation_id)
        if isinstance(result, dict) and "question" not in result:
            result["question"] = question
        return result
    except Exception as exc:
        logger.warning(
            f"Multi-agent orchestrator error, falling back to direct RAG pipeline: {exc}"
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