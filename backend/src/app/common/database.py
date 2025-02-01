__all__ = ["Base", "UUIDMixIn", "IntegerIDMixIn"]


import uuid
import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped as Mapped, mapped_column as mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions


class DBTable(DeclarativeBase):
    __table_args__ = {"extend_existing": True}
    metadata: sa.MetaData = sa.MetaData()

    created_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), index=True, nullable=False, server_default=sqlalchemy_functions.now(), sort_order=70
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=True, onupdate=sqlalchemy_functions.now(), sort_order=80
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(created_at={self.created_at!r})"


Base = DBTable


class UUIDMixIn(object):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, nullable=False, server_default=sa.text("gen_random_uuid()"), sort_order=-1
    )


class IntegerIDMixIn(object):
    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, autoincrement=True, sort_order=-1)
