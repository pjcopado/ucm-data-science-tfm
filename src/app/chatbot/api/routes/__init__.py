from fastapi import APIRouter

from . import chat

router = APIRouter()

router.include_router(router=chat.router)
