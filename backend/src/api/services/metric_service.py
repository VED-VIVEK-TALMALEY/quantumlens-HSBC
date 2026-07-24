from src.utils.logger import logger
from src.warehouse.supabase_client import get_supabase

supabase = get_supabase()


def get_all_metrics():

    logger.info(
        "/metrics requested"
    )

    result = (
        supabase
        .table("metrics")
        .select(
            "metric_id,metric_name,abbreviation"
        )
        .order("metric_id")
        .execute()
    )

    unique_metrics = {}

    for row in result.data:

        if row["metric_id"] not in unique_metrics:

            unique_metrics[row["metric_id"]] = row

    return list(unique_metrics.values())


def get_metric_by_id(metric_id: int):

    logger.info(
        f"/metric/{metric_id}"
    )

    result = (
        supabase
        .table("metrics")
        .select(
            "id,metric_id,metric_name,abbreviation,sheet_name,row_number"
        )
        .eq(
            "metric_id",
            metric_id
        )
        .execute()
    )

    return result.data