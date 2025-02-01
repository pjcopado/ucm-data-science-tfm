from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.app.models import *
from src.app.core.rate_limiter import limiter
from src.app.core.config import settings
from src.app.core.middlewares import register_middlewares
from src.app.core.exception import BaseAPIError
from src.app.api import router


def initialize_backend_application() -> FastAPI:
    app = FastAPI(**settings.set_backend_app_attributes)

    register_middlewares(app)
    add_pagination(app)

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.exception_handler(BaseAPIError)
    async def custom_exception_handler(request: Request, exc: BaseAPIError) -> JSONResponse:
        return exc.response()

    app.include_router(router=router, prefix=settings.ROOT_PATH)

    return app


app: FastAPI = initialize_backend_application()
