__all__ = ["ChatCreateSch", "ChatUpdateSch", "ChatSch"]

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin
from src.app.chatbot.enums import ChatMessageResponseStatusEnum


class ChatBaseSch(OrmBaseModel):
    pass


class ChatCreateSch(ChatBaseSch):
    question: str


class ChatUpdateSch(OrmBaseModel):
    pass


class ChatSch(ChatBaseSch, TimestampModelMixin, UUIDModelMixin):
    pass
