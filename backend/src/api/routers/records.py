## -------------------------------------------------------------------
## Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
##
## This project and its source code are strictly proprietary.
## Unauthorized copying, distribution, or use is strictly prohibited.
## -------------------------------------------------------------------

from fastapi import APIRouter

from src.api.services.record_service import (
    get_metric_record,
)

router = APIRouter()


@router.get("/record/{record_id}")
def record(record_id: int):
    return get_metric_record(record_id)