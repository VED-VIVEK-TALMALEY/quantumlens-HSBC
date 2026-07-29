# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

from src.utils.logger import logger
from warehouse.supabase_client import get_supabase

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