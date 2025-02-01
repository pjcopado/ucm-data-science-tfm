__all__ = ["ChatCreateSch", "ChatUpdateSch", "ChatSch"]

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin
from src.app.chatbot.enums import ChatResponseStatusEnum


class ChatBaseSch(OrmBaseModel):
    question: str


class ChatCreateSch(ChatBaseSch):
    pass


class ChatUpdateSch(OrmBaseModel):
    answer: str = None
    status: ChatResponseStatusEnum = None


class ChatSch(ChatBaseSch, TimestampModelMixin, UUIDModelMixin):
    answer: str | None
    status: ChatResponseStatusEnum
