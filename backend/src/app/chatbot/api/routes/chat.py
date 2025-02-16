from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.api.dependencies.repository import get_repository
from src.app.common.api.dependencies.session_ext import get_async_session_ext
from src.app.chatbot import repository, schemas as sch, service

router = APIRouter(prefix="/chats", tags=["chat"])


@router.get(
    "",
    summary="get all chats",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.ChatSch],
)
async def get_chats(
    chat_repository: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
):
    stmt = await chat_repository.get_all_stmt()
    return await sqla_paginate(chat_repository.async_session, stmt)


@router.post(
    "",
    summary="create new chat",
    status_code=status.HTTP_200_OK,
    response_model=sch.ChatSch,
)
async def ask(
    session_ext: AsyncSession = Depends(get_async_session_ext),
    obj_in: sch.ChatCreateRequestSch = Body(...),
    chat_repository: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
    chat_message_repository: repository.ChatMessageRepository = Depends(
        get_repository(repo_type=repository.ChatMessageRepository)
    ),
):
    chat_service = service.ChatService(
        chat_repository=chat_repository,
        chat_message_repository=chat_message_repository,
        session_ext=session_ext,
    )
    return await chat_service.create_chat(obj_in=obj_in)
