from fastapi import APIRouter

from src.api.services import (
    ask_question,
    search_metrics,
    get_all_metrics,
    get_metric_by_id,
)

from src.api.schemas import (
    QuestionRequest,
    SearchRequest
)

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.get("/metrics")
def metrics():

    return get_all_metrics()


@router.get("/metric/{metric_id}")
def metric(metric_id: int):

    return get_metric_by_id(metric_id)


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