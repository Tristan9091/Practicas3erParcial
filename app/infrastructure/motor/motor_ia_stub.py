from app.domain.entities.conversacion import Conversacion
from app.domain.entities.respuesta_asistente import RespuestaAsistente
from app.domain.ports.motor_respuestas import MotorRespuestas


class MotorIAStub(MotorRespuestas):
    def responder(self, pregunta: str, conversacion: Conversacion) -> RespuestaAsistente:
        raise NotImplementedError(
            "MotorIAStub es solo demostrativo. Implementar recuperacion "
            "(RAG) + llamada al LLM aqui y devolver un RespuestaAsistente."
        )
