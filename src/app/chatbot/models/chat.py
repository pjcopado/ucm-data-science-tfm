import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.app.common.database import Base, UUIDMixIn
from src.app.chatbot.enums import ChatResponseStatusEnum


class ChatModel(Base, UUIDMixIn):
    __tablename__ = "chat"
    __mapper_args__ = {"eager_defaults": True}

    question: Mapped[str] = mapped_column(sa.Text, nullable=False)
    answer: Mapped[str] = mapped_column(sa.Text, nullable=True)
    status: Mapped[str] = mapped_column(sa.String, nullable=False, server_default=ChatResponseStatusEnum.PENDING.value)

    def __repr__(self) -> str:
        answer = f"{self.answer[:10]}..." if self.answer else None
        return f"{self.__class__.__name__}(question={self.question}, answer={answer})"
