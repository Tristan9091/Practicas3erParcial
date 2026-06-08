from typing import Optional
from app.domain.entities.mensaje_chat import MensajeChat
from app.domain.ports.motor_respuestas import MotorRespuestas

class ProcesarMensajeCliente:
    def __init__(self, motor: MotorRespuestas):
        self.motor = motor

    def ejecutar(self, contenido: str) -> Optional[MensajeChat]:
        return self.motor.responder(contenido)