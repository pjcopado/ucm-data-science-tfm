from fastapi import APIRouter

from . import chat, chat_message, chat_stream

router = APIRouter()

router.include_router(router=chat.router)
router.include_router(router=chat_message.router)
router.include_router(router=chat_stream.router)
