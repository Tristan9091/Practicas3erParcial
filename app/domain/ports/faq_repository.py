from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.pregunta_frecuente import PreguntaFrecuente

class FaqRepository(ABC):
    @abstractmethod
    def listar_todas(self) -> List[PreguntaFrecuente]:
        pass

    @abstractmethod
    def buscar(self, texto: str) -> List[PreguntaFrecuente]:
        pass

    @abstractmethod
    def guardar(self, faq: PreguntaFrecuente):
        pass