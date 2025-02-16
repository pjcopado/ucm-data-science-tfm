import uuid

import sqlalchemy as sa

from src.app.common.repository import BaseRepository
from src.app.chatbot import models, schemas as sch


class ChatMessageRepository(BaseRepository[models.ChatMessageModel, sch.ChatMessageCreateSch, sch.ChatMessageUpdateSch]):
    model = models.ChatMessageModel

    async def get_all_stmt(self, *, chat_id: uuid.UUID):
        stmt = sa.select(self.model).where(self.model.chat_id == chat_id)
        return stmt.order_by(self.model.created_at.desc())
