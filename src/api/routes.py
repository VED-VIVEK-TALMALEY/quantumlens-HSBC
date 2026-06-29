from fastapi import APIRouter

from src.api.schemas import (
    QuestionRequest,
    SearchRequest
)

from src.api.services import (
    ask_question,
    search_metrics
)

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


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