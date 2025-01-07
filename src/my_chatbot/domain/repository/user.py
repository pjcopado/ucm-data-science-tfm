from abc import ABC, abstractmethod
from typing import Optional
from entity.user import User
from uuid import UUID


class user_repository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        pass