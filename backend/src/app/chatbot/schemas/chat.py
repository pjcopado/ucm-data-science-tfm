__all__ = ["ChatCreateSch", "ChatCreateRequestSch", "ChatUpdateSch", "ChatSch"]

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin
from .chat_message import ChatMessageSch


class ChatBaseSch(OrmBaseModel):
    pass


class ChatCreateRequestSch(OrmBaseModel):
    question: str


class ChatCreateSch(ChatBaseSch):
    question: str
    query: str | None = None
    query_explanation: str | None = None
    query_response: str | None = None
    response: str | None = None


class ChatUpdateSch(OrmBaseModel):
    pass


class ChatSch(ChatBaseSch, TimestampModelMixin, UUIDModelMixin):
    first_message: ChatMessageSch | None
