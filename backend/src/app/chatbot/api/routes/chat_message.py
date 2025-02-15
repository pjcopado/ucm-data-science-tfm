from fastapi import APIRouter, Body, status, Depends, Request
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository
from src.app.chatbot.api import dependencies as deps
from src.app.chatbot import repository, schemas as sch, enums
from src.app.core import exception

router = APIRouter(prefix="/chats/{chat_id}/messages", tags=["chat"])


@router.get(
    "",
    summary="get all messages from chat",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.ChatMessageSch],
)
async def get_messages(
    chat: deps.Chat,
    repository: repository.ChatMessageRepository = Depends(get_repository(repo_type=repository.ChatMessageRepository)),
):
    stmt = await repository.get_all_stmt(chat_id=chat.id)
    return await sqla_paginate(repository.async_session, stmt)


@router.post(
    "",
    summary="create new message for chat",
    status_code=status.HTTP_200_OK,
    response_model=sch.ChatMessageSch,
)
async def create_message(
    request: Request,
    chat: deps.Chat,
    obj_in: sch.ChatMessageCreateSch = Body(...),
    repository: repository.ChatMessageRepository = Depends(get_repository(repo_type=repository.ChatMessageRepository)),
):
    return await repository.create(obj_in=obj_in, chat_id=chat.id)


@router.patch(
    "/{message_id}",
    summary="update question from chat",
    status_code=status.HTTP_200_OK,
    response_model=sch.ChatMessageSch,
)
async def update_message(
    message: deps.ChatMessage,
    obj_in: sch.ChatMessageUpdateSch = Body(...),
    repository: repository.ChatMessageRepository = Depends(get_repository(repo_type=repository.ChatMessageRepository)),
):
    if message.status != enums.ChatMessageResponseStatusEnum.COMPLETED:
        raise exception.BaseAPIError(status_code=status.HTTP_400_BAD_REQUEST, detail="Message is not completed")
    return await repository.update(obj_db=message, obj_in=obj_in)
