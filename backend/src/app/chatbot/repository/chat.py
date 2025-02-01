from src.app.common.repository import BaseRepository
from src.app.chatbot import models, schemas as sch


class ChatRepository(BaseRepository[models.ChatModel, sch.ChatCreateSch, sch.ChatUpdateSch]):
    model = models.ChatModel

    async def create(self, *, obj_in, **kwargs):
        messages = [models.ChatMessageModel(**message) for message in obj_in.pop("messages")]
        return await super().create(obj_in=obj_in, messages=messages, **kwargs)
