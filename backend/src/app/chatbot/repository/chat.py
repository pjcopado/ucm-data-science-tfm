from src.app.common.repository import BaseRepository
from src.app.chatbot import models, schemas as sch


class ChatRepository(BaseRepository[models.ChatModel, sch.ChatCreateSch, sch.ChatUpdateSch]):
    model = models.ChatModel

    async def create(self, *, obj_in: sch.ChatCreateSch, **kwargs):
        messages = [models.ChatMessageModel(question=obj_in.question)]
        return await super().create(obj_in={}, messages=messages, **kwargs)
