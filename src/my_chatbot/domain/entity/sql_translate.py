from abc import ABC, abstractmethod

class SqlTranslator(ABC):   
    @abstractmethod
    def translate(self, text: str) -> str:
        pass

