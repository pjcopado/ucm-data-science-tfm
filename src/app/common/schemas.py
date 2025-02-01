import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrmBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
    )


class TimestampModelMixin(OrmBaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UUIDModelMixin(OrmBaseModel):
    id: UUID


class IntegerIDModelMixin(OrmBaseModel):
    id: int
