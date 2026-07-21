import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("quantumlens")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        start = time.perf_counter()

        logger.info(
            "[%s] %s %s",
            request_id,
            request.method,
            request.url.path,
        )

        response = await call_next(request)

        duration = round((time.perf_counter() - start) * 1000, 2)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration} ms"

        logger.info(
            "[%s] Completed %s (%sms)",
            request_id,
            response.status_code,
            duration,
        )

        return response