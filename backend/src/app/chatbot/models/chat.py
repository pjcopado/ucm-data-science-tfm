from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.app.common.database import Base, UUIDMixIn


class ChatModel(Base, UUIDMixIn):
    __tablename__ = "chat"
    __mapper_args__ = {"eager_defaults": True}

    messages = relationship("ChatMessageModel", back_populates="chat", lazy="joined", order_by="ChatMessageModel.created_at")

    @hybrid_property
    def first_message(self):
        if self.messages:
            return self.messages[0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(messages count = {len(self.messages)})"
