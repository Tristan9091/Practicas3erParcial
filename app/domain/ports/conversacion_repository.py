from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.conversacion import Conversacion
from app.domain.entities.mensaje_chat import MensajeChat


class ConversacionRepository(ABC):
    @abstractmethod
    def guardar(self, conversacion: Conversacion) -> None:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Conversacion]:
        pass

    @abstractmethod
    def agregar_mensaje(self, mensaje: MensajeChat) -> None:
        pass

    @abstractmethod
    def actualizar_estado(self, conversacion: Conversacion) -> None:
        pass

    @abstractmethod
    def listar_por_cliente(self, cliente_id: str) -> List[Conversacion]:
        pass
