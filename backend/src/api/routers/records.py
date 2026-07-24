from fastapi import APIRouter

from src.api.services.record_service import (
    get_metric_record,
)

router = APIRouter()


@router.get("/record/{record_id}")
def record(record_id: int):

    return get_metric_record(record_id)