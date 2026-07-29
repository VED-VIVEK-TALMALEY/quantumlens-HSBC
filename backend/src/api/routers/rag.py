# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from fastapi import APIRouter

from src.api.schemas.rag import (
    QuestionRequest,
    SearchRequest,
)

from src.api.services.rag_service import (
    ask_question,
    search_metrics,
)

router = APIRouter()


@router.post("/ask")
def ask_ai(request: QuestionRequest):

    return ask_question(
        request.question
    )


@router.post("/search")
def search(request: SearchRequest):

    return search_metrics(
        request.query,
        request.top_k
    )