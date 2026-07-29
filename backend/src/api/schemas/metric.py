# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from pydantic import BaseModel


class MetricResponse(BaseModel):
    metric_id: int
    metric_name: str
    abbreviation: str