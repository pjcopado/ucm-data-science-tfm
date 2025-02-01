__all__ = ["ChatCreateSch", "ChatUpdateSch", "ChatSch"]

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin


class ChatBaseSch(OrmBaseModel):
    pass


class ChatCreateSch(ChatBaseSch):
    question: str


class ChatUpdateSch(OrmBaseModel):
    pass


class ChatSch(ChatBaseSch, TimestampModelMixin, UUIDModelMixin):
    title: str
    pass
