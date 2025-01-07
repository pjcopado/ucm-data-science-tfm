from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar
from uuid import UUID
import uuid

EntityType = TypeVar("EntityType", bound="domain_entity")


class domain_entity(ABC):
    @abstractmethod
    def __init__(self, id: UUID = None, created_at: datetime = None):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()

    @property
    def id(self) -> UUID:
        return self.__id

    @id.setter
    def id(self, id: UUID) -> None:
        if not isinstance(id, UUID):
            raise InvalidDomainEntityError('Field id must be a valid UUID type')
        self.__id = id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at: datetime) -> None:
        if not isinstance(created_at, datetime):
            raise InvalidDomainEntityError('Field created_at must be a valid datetime type')
        

        self.__created_at = created_at

