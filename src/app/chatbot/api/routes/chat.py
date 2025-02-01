import datetime as dt
import uuid

from fastapi import APIRouter, Body, status, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate as sqla_paginate

from src.app.common.api.dependencies.repository import get_repository

# from src.app.chatbot.api import dependencies as deps
from src.app.chatbot import repository, schemas as sch

router = APIRouter(prefix="/chat", tags=["chatbot"])


@router.get(
    "",
    summary="get all questions",
    status_code=status.HTTP_200_OK,
    response_model=Page[sch.ChatSch],
)
async def get_questions(
    repository: repository.ChatRepository = Depends(get_repository(repo_type=repository.ChatRepository)),
):
    stmt = await repository.get_all_stmt()
    return await sqla_paginate(repository.async_session, stmt)


@router.post(
    "",
    summary="ask question",
    status_code=status.HTTP_200_OK,
    response_model=sch.ChatSch,
)
async def ask(
    obj_in: sch.ChatCreateSch = Body(...),
    # impact_repo: repository.ImpactRepository = Depends(get_repository(repo_type=repository.ImpactRepository)),
):
    answer = "Generating response..."

    response = {
        "id": uuid.uuid4(),
        "question": obj_in.question,
        "answer": answer,
        "status": "pending",
        "created_at": dt.datetime.now(),
        "updated_at": None,
    }
    return response
