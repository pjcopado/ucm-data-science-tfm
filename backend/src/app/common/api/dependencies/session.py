import typing

import loguru
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.app.core.database import async_db
from src.app.core import exception


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    session = async_db.async_session()
    try:
        yield session
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise exception.DatabaseIntegrityError(detail=str(e))
    except Exception as e:
        loguru.logger.info(e)
        await session.rollback()
        raise
    finally:
        await session.close()
