from abc import ABC, abstractmethod
from shared_kernel.domain.entity import domain_entity
from datetime import datetime


class query_executor(ABC):
    @abstractmethod
    def fetch_results(self, query: str) -> list:
        """
        Ejecuta una consulta SQL y recupera los resultados.
        """
        pass
