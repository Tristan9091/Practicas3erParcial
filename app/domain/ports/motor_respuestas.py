from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.mensaje_chat import MensajeChat

class MotorRespuestas(ABC):
    @abstractmethod
    def responder(self, mensaje_cliente: str) -> Optional[MensajeChat]:
        """
        Recibe el texto del cliente y devuelve un MensajeChat del asistente,
        o None si el motor no sabe responder.
        """
        pass