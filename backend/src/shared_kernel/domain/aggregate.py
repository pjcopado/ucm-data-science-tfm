from abc import abstractmethod
from datetime import datetime
from uuid import UUID
from .entity import domain_entity
from shared_kernel.bus.domain_event import domain_event

class AggregateRoot(domain_entity):
    @abstractmethod
    def __init__(self, id: UUID, created_at: datetime):
        super().__init__(id, created_at)
        self.__events = []

    def pull_events(self) -> [domain_event]: # type: ignore
        events = self.__events
        self.__events = []
        return events

    def add_event(self, event: domain_event) -> None:
        if isinstance(event, domain_event):
            self.__events.append(event)