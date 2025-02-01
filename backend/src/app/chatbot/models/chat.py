import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.common.database import Base, UUIDMixIn
from .chat_message import ChatMessageModel


class ChatModel(Base, UUIDMixIn):
    __tablename__ = "chat"
    __mapper_args__ = {"eager_defaults": True}

    owner_id: Mapped[uuid.UUID] = mapped_column(nullable=False)

    messages = relationship("ChatMessageModel", back_populates="chat")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
