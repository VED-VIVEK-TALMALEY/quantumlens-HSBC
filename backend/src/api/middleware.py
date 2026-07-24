import time

from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.logger import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        elapsed = round(time.time() - start, 3)

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{elapsed}s"
        )

        return response