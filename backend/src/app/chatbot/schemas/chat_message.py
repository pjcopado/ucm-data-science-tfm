__all__ = ["ChatMessageCreateSch", "ChatMessageCreateRequestSch", "ChatMessageUpdateSch", "ChatMessageSch"]

import uuid

from src.app.common.schemas import OrmBaseModel, TimestampModelMixin, UUIDModelMixin
from src.app.chatbot.enums import ChatMessageResponseStatusEnum


class ChatMessageBaseSch(OrmBaseModel):
    question: str


class ChatMessageCreateSch(ChatMessageBaseSch):
    llm_response_id: uuid.UUID | None
    query: str | None
    query_explanation: str | None
    query_response: str | None
    confidence_score: float | None
    response: str | None
    status: ChatMessageResponseStatusEnum


class ChatMessageCreateRequestSch(ChatMessageBaseSch):
    question: str


class ChatMessageUpdateSch(OrmBaseModel):
    is_valid: bool | None


class ChatMessageSch(ChatMessageBaseSch, TimestampModelMixin, UUIDModelMixin):
    llm_response_id: uuid.UUID | None
    query: str | None
    query_explanation: str | None
    query_response: str | None
    confidence_score: float | None
    response: str | None
    is_valid: bool | None
    status: ChatMessageResponseStatusEnum
