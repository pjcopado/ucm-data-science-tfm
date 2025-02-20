import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.app.common.database import Base, UUIDMixIn
from src.app.chatbot.enums import ChatMessageResponseStatusEnum


class ChatMessageModel(Base, UUIDMixIn):
    __tablename__ = "chat_message"
    __mapper_args__ = {"eager_defaults": True}

    chat_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("chat.id"), index=True, nullable=False)
    llm_response_id: Mapped[uuid.UUID] = mapped_column(sa.UUID(as_uuid=True), index=True, nullable=True)
    question: Mapped[str] = mapped_column(sa.Text, nullable=False)
    query: Mapped[str] = mapped_column(sa.Text, nullable=True)
    query_explanation: Mapped[str] = mapped_column(sa.Text, nullable=True)
    query_response: Mapped[str] = mapped_column(sa.Text, nullable=True)
    confidence_score: Mapped[float] = mapped_column(sa.Float, nullable=True)
    response: Mapped[str] = mapped_column(sa.Text, nullable=True)
    is_valid: Mapped[bool] = mapped_column(sa.Boolean, index=True, nullable=True)
    status: Mapped[str] = mapped_column(
        sa.String,
        index=True,
        nullable=False,
        default=ChatMessageResponseStatusEnum.PENDING.value,
    )

    chat = relationship("ChatModel", back_populates="messages")

    def __repr__(self) -> str:
        response = f"{self.response[:10]}..." if self.response else None
        return f"{self.__class__.__name__}(question={self.question}, response={response})"
