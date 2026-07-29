# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from fastapi import APIRouter

from src.api.services.metric_service import (
    get_all_metrics,
    get_metric_by_id,
)

router = APIRouter()


@router.get("/metrics")
def metrics():

    return get_all_metrics()


@router.get("/metric/{metric_id}")
def metric(metric_id: int):

    return get_metric_by_id(metric_id)