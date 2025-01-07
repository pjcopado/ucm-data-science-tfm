from abc import ABC, abstractmethod
from typing import Optional
from entity.query import query_executor
from uuid import UUID


class query_repository(ABC):
    @abstractmethod
    def return_query(self) -> query_executor:
        pass