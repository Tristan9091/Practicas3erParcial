from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.faq import FAQ


class FaqRepository(ABC):
    @abstractmethod
    def guardar(self, faq: FAQ) -> None:
        pass

    @abstractmethod
    def listar_todas(self) -> List[FAQ]:
        pass

    @abstractmethod
    def buscar_candidatas(self, texto: str) -> List[FAQ]:
        pass
