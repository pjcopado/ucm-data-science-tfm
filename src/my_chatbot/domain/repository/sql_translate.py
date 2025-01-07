from abc import ABC, abstractmethod
from typing import Optional
from entity.sql_translate import SqlTranslator
from uuid import UUID


class translate_repository(ABC):
    @abstractmethod
    def translate(self) -> SqlTranslator:
        pass