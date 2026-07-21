from datetime import datetime
from fastapi.encoders import jsonable_encoder


def success_response(
    data=None,
    message="Success",
):
    return {
        "success": True,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "data": jsonable_encoder(data),
    }


def error_response(
    message,
):
    return {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
    }