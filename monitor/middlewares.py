import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from logger import MyLogger

logger = MyLogger("api")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        pre_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        logger.debug(f"收到{request.method}请求："
                     f"REQ_ID: {request_id} "
                     f"URL:{request.url} "
                     f"PARAMS:{request.query_params}")

        response = await call_next(request)

        logger.debug(f"结束{request.method}请求："
                     f"REQ_ID: {request_id} "
                     f"耗时: {(time.perf_counter() - pre_time) * 1000}ms")
        response.headers["X-Request-ID"] = request_id
        return response
