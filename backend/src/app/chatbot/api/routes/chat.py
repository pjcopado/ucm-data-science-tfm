from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository

from src.app.chatbot import repository, schemas as sch, service, enums

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
    obj_in: sch.ChatCreateSch = Body(...),
    chat_repository: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
    chat_message_repository: repository.ChatMessageRepository = Depends(
        get_repository(repo_type=repository.ChatMessageRepository)
    ),
):
    chat_service = service.ChatService(chat_repository=chat_repository, chat_message_repository=chat_message_repository)
    prompt = obj_in.question
    # TODO
    # response = await chat_service.ask(prompt=prompt)
    query_explanation = None
    response = None
    obj_in = {
        "question": prompt,
        "response": response,
        "is_valid": None,
        "query_explanation": query_explanation,
        "status": enums.ChatMessageResponseStatusEnum.COMPLETED.value,
    }
    return await chat_repository.create(obj_in=obj_in)
