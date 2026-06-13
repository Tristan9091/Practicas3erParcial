from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List

from app.domain.entities.mensaje_chat import MensajeChat


class EstadoConversacion(str, Enum):
    ABIERTA = "abierta"
    ESCALADA = "escalada"
    CERRADA = "cerrada"


@dataclass
class Conversacion:
    id: str
    cliente_id: str
    estado: EstadoConversacion = EstadoConversacion.ABIERTA
    mensajes: List[MensajeChat] = field(default_factory=list)
    creada_en: datetime = field(default_factory=datetime.now)

    def agregar(self, mensaje: MensajeChat) -> None:
        self.mensajes.append(mensaje)
