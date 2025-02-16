import uuid
import typing as t

from fastapi import Depends, status

from src.app.chatbot import models, repository
from src.app.common.api.dependencies.repository import get_repository
from src.app.core import exception
from .chat import Chat


async def get_by_id(
    message_id: uuid.UUID,
    chat: Chat,
    chat_message_repo: repository.ChatMessageRepository = Depends(get_repository(repo_type=repository.ChatMessageRepository)),
):
    message = await chat_message_repo.get_by_id_or_raise(id=message_id)
    if message.chat_id != chat.id:
        raise exception.BaseAPIError(status_code=status.HTTP_403_FORBIDDEN, detail="Message does not belong to chat")
    return message


ChatMessage = t.Annotated[models.ChatMessageModel, Depends(get_by_id)]
