from abc import ABC, abstractmethod

from shared_kernel.bus.domain_event import domain_event


class EventBus(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def publish(self, events: [domain_event]) -> None: # type: ignore
        raise NotImplementedError('Method publish must be implemented')
