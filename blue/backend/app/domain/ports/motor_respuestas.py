from abc import ABC, abstractmethod

from app.domain.entities.conversacion import Conversacion
from app.domain.entities.respuesta_asistente import RespuestaAsistente


class MotorRespuestas(ABC):
    @abstractmethod
    def responder(self, pregunta: str, conversacion: Conversacion) -> RespuestaAsistente:
        pass
