from pydantic import BaseModel


class MetricResponse(BaseModel):
    metric_id: int
    metric_name: str
    abbreviation: str