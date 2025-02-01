from typing import Generic, Type, TypeVar
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from src.app.common.database import Base
from src.app.core.exception import BaseAPIError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]

    def __init__(self, async_session: SQLAlchemyAsyncSession):
        self.async_session = async_session

    async def get_all_stmt(self):
        stmt = sa.select(self.model)
        return stmt.order_by(self.model.created_at.asc())

    async def get_all(self):
        stmt = await self.get_all_stmt()
        query = await self.async_session.execute(stmt)
        return query.scalars().all()

    async def get_by_id(self, id: UUID | int | str) -> ModelType | None:
        stmt = sa.select(self.model).where(self.model.id == id)
        query = await self.async_session.execute(stmt)
        return query.scalar()

    async def get_by_id_or_raise(self, id: UUID | int | str) -> ModelType:
        record = await self.get_by_id(id)
        if not record:
            raise BaseAPIError(status_code=400, detail=f"{self.model.__name__} with {id=} does not exist")
        return record

    async def get_by_attributes(self, **kwargs) -> ModelType | None:
        stmt = sa.select(self.model)
        for attr, value in kwargs.items():
            stmt = stmt.where(getattr(self.model, attr) == value)
        stmt = stmt.order_by(self.model.created_at.asc())
        query = await self.async_session.execute(stmt)
        return query.scalar()

    async def create(self, *, obj_in: CreateSchemaType | dict, **kwargs) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_dict = obj_in
        else:
            obj_in_dict = obj_in.model_dump()
        obj_db = self.model(**obj_in_dict, **kwargs)
        self.async_session.add(obj_db)
        await self.async_session.flush()
        await self.async_session.commit()
        await self.async_session.refresh(obj_db)
        return obj_db

    async def update(
        self,
        *,
        obj_db: ModelType,
        obj_in: UpdateSchemaType | dict,
        **kwargs,
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        update_data = {**update_data, **kwargs}
        for field, value in update_data.items():
            if hasattr(obj_db, field) and not isinstance(value, dict):
                setattr(obj_db, field, value)
        await self.async_session.commit()
        await self.async_session.refresh(obj_db)
        return obj_db

    async def delete(self, *, obj_db: ModelType) -> ModelType:
        await self.async_session.delete(obj_db)
        await self.async_session.commit()
        return obj_db
