from src.utils.logger import logger
from src.warehouse.supabase_client import get_supabase

supabase = get_supabase()


def get_metric_record(record_id: int):

    logger.info(
        f"/record/{record_id}"
    )

    result = (
        supabase
        .table("metrics")
        .select("*")
        .eq(
            "id",
            record_id
        )
        .execute()
    )

    return result.data