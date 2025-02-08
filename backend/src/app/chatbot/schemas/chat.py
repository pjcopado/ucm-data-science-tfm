__all__ = ["ChatCreateSch", "ChatUpdateSch", "ChatSch"]

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin
from .chat_message import ChatMessageSch


class ChatBaseSch(OrmBaseModel):
    pass


class ChatCreateRequestSch(OrmBaseModel):
    question: str


class ChatCreateSch(ChatBaseSch):
    question: str


class ChatUpdateSch(OrmBaseModel):
    pass


class ChatSch(ChatBaseSch, TimestampModelMixin, UUIDModelMixin):
    first_message: ChatMessageSch
