__all__ = ["ChatMessageCreateSch", "ChatMessageUpdateSch", "ChatMessageSch"]

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin
from src.app.chatbot.enums import ChatMessageResponseStatusEnum


class ChatMessageBaseSch(OrmBaseModel):
    question: str


class ChatMessageCreateSch(ChatMessageBaseSch):
    pass


class ChatMessageUpdateSch(OrmBaseModel):
    is_valid: bool | None


class ChatMessageSch(ChatMessageBaseSch, TimestampModelMixin, UUIDModelMixin):
    response: str | None
    is_valid: bool | None
    query_explanation: str | None
    status: ChatMessageResponseStatusEnum
