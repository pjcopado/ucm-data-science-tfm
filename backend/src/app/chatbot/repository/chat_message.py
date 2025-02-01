from src.app.common.repository import BaseRepository
from src.app.chatbot import models, schemas as sch


class ChatMessageRepository(BaseRepository[models.ChatMessageModel, sch.ChatMessageCreateSch, sch.ChatMessageUpdateSch]):
    model = models.ChatMessageModel
