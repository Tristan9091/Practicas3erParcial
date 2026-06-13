from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AutorMensaje(str, Enum):
    CLIENTE = "cliente"
    ASISTENTE = "asistente"
    SISTEMA = "sistema"
    AGENTE = "agente"


@dataclass
class MensajeChat:
    id: str
    conversacion_id: str
    autor: AutorMensaje
    contenido: str
    timestamp: datetime = field(default_factory=datetime.now)
