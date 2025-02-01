import time
from typing import Callable, Awaitable

from fastapi import FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.app.core.config import settings


CallNextFn = Callable[[Request], Awaitable[Response]]


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallNextFn) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{1000 * process_time:.1f} ms"
        return response


def register_middlewares(app: FastAPI):
    app.add_middleware(ProcessTimeHeaderMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
        expose_headers=["X-Request-ID"],
    )
