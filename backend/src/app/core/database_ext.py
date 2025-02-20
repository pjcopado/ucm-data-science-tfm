import pydantic
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import Pool, QueuePool, AsyncAdaptedQueuePool

from .config import settings


class SyncDatabaseExt:
    def __init__(self):
        URL = f"postgresql://{settings.EXTERNAL_POSTGRES_USERNAME}:{settings.EXTERNAL_POSTGRES_PASSWORD}@{settings.EXTERNAL_POSTGRES_HOST}:{settings.EXTERNAL_POSTGRES_PORT}/{settings.EXTERNAL_POSTGRES_DB}"
        self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(url=URL).unicode_string()
        self.engine = create_engine(
            url=self.postgres_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=QueuePool,
        )
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.pool: Pool = self.engine.pool


sync_db: SyncDatabaseExt = SyncDatabaseExt()


class AsyncDatabaseExt:
    def __init__(self):
        URL = f"postgresql+asyncpg://{settings.EXTERNAL_POSTGRES_USERNAME}:{settings.EXTERNAL_POSTGRES_PASSWORD}@{settings.EXTERNAL_POSTGRES_HOST}:{settings.EXTERNAL_POSTGRES_PORT}/{settings.EXTERNAL_POSTGRES_DB}"
        self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(url=URL).unicode_string()
        self.async_engine = create_async_engine(
            url=self.postgres_uri,
            echo=settings.IS_DB_ECHO_LOG,
            future=True,
            pool_pre_ping=True,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=AsyncAdaptedQueuePool,
        )
        self.async_session = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


async_db: AsyncDatabaseExt = AsyncDatabaseExt()
