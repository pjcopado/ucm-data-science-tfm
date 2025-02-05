from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository

from src.app.chatbot import repository, schemas as sch, service

router = APIRouter(prefix="/chats", tags=["chat"])


@router.get(
    "",
    summary="get all chats",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.ChatSch],
)
async def get_chats(
    repository: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
):
    stmt = await repository.get_all_stmt()
    return await sqla_paginate(repository.async_session, stmt)


@router.post(
    "",
    summary="create new chat",
    status_code=status.HTTP_200_OK,
    # response_model=sch.ChatSch,
)
async def ask(
    obj_in: sch.ChatCreateSch = Body(...),
    repository: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
):
    chat_service = service.ChatService(repository=repository)
    prompt = obj_in.question
    result = await chat_service.ask(prompt=prompt)
    return {"response": result}
    # return await repository.create(obj_in=obj_in)
