import typing

import loguru
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database_ext import async_db


async def get_async_session_ext() -> typing.AsyncGenerator[AsyncSession, None]:
    session = async_db.async_session()
    try:
        yield session
    except Exception as e:
        loguru.logger.info(e)
        raise
    finally:
        await session.close()
