__all__ = ("BaseAPIError",)

import re

import pydantic
from starlette import status
from fastapi.responses import JSONResponse


class BaseError(pydantic.BaseModel):
    code: str = pydantic.Field(..., description="Error code (internal)")
    detail: str = pydantic.Field(..., description="Error message or description")


class BaseAPIError(Exception):
    """Base error for custom API exceptions"""

    _status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    _code: str = "INTERNAL"
    _detail: str = "Generic error"
    _headers: dict = {}
    model = BaseError

    def __init__(self, detail: str = None, status_code: int = None, code: str = None, headers: dict = None):
        self.status_code = status_code or self._status_code
        self.code = code or self._code
        self.detail = detail or self._detail
        self.data = self.model(code=self._code, detail=self.detail)
        self.headers = headers or self._headers

    def __str__(self):
        return self.detail

    def response(self):
        return JSONResponse(content=self.data.model_dump(), status_code=self.status_code, headers=self.headers)


class DatabaseIntegrityError(BaseAPIError):
    """
    Throw an exception when the data can not be inserted into the database.
    """

    _status_code = status.HTTP_400_BAD_REQUEST
    _code = "INTEGRITY_ERROR"

    def __init__(self, detail: str):
        try:
            detail = re.search(r"Key \(.{,100}\).{,100}", str(detail)).group()
        except:
            pass
        super().__init__(detail=detail)
