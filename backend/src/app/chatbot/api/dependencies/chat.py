import uuid
import typing as t

from fastapi import Depends

from src.app.common.api.dependencies.repository import get_repository
from src.app.chatbot import models, repository


async def get_by_id(
    chat_id: uuid.UUID,
    chat_repo: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
):
    return await chat_repo.get_by_id_or_raise(id=chat_id)


Chat = t.Annotated[models.ChatModel, Depends(get_by_id)]
