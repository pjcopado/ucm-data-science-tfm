from src.app.common.repository import BaseRepository
from src.app.chatbot import models, schemas as sch


class ChatRepository(BaseRepository[models.ChatModel, sch.ChatCreateSch, sch.ChatUpdateSch]):
    model = models.ChatModel
