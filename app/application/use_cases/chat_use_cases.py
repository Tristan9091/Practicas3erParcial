import uuid

from app.domain.entities.conversacion import Conversacion, EstadoConversacion
from app.domain.entities.mensaje_chat import MensajeChat, AutorMensaje
from app.domain.entities.respuesta_asistente import RespuestaAsistente
from app.domain.ports.conversacion_repository import ConversacionRepository
from app.domain.ports.motor_respuestas import MotorRespuestas

UMBRAL_ESCALAMIENTO = 0.35


class IniciarConversacion:
    def __init__(self, conversacion_repository: ConversacionRepository):
        self.conversacion_repository = conversacion_repository

    def ejecutar(self, cliente_id: str) -> Conversacion:
        conversacion = Conversacion(
            id=str(uuid.uuid4()),
            cliente_id=cliente_id,
            estado=EstadoConversacion.ABIERTA,
        )
        self.conversacion_repository.guardar(conversacion)
        return conversacion


class ProcesarMensajeCliente:
    def __init__(
        self,
        conversacion_repository: ConversacionRepository,
        motor_respuestas: MotorRespuestas,
    ):
        self.conversacion_repository = conversacion_repository
        self.motor_respuestas = motor_respuestas

    def ejecutar(self, conversacion_id: str, texto_cliente: str):
        conversacion = self.conversacion_repository.obtener_por_id(conversacion_id)
        if not conversacion:
            raise ValueError("Conversacion no encontrada")

        mensaje_cliente = MensajeChat(
            id=str(uuid.uuid4()),
            conversacion_id=conversacion_id,
            autor=AutorMensaje.CLIENTE,
            contenido=texto_cliente,
        )
        self.conversacion_repository.agregar_mensaje(mensaje_cliente)
        conversacion.agregar(mensaje_cliente)

        respuesta: RespuestaAsistente = self.motor_respuestas.responder(
            texto_cliente, conversacion
        )

        mensaje_asistente = MensajeChat(
            id=str(uuid.uuid4()),
            conversacion_id=conversacion_id,
            autor=AutorMensaje.ASISTENTE,
            contenido=respuesta.contenido,
        )
        self.conversacion_repository.agregar_mensaje(mensaje_asistente)
        conversacion.agregar(mensaje_asistente)

        if not respuesta.manejada or respuesta.confianza < UMBRAL_ESCALAMIENTO:
            conversacion.estado = EstadoConversacion.ESCALADA
            self.conversacion_repository.actualizar_estado(conversacion)

        return mensaje_cliente, mensaje_asistente, respuesta


class ObtenerHistorial:
    def __init__(self, conversacion_repository: ConversacionRepository):
        self.conversacion_repository = conversacion_repository

    def ejecutar(self, conversacion_id: str) -> Conversacion:
        conversacion = self.conversacion_repository.obtener_por_id(conversacion_id)
        if not conversacion:
            raise ValueError("Conversacion no encontrada")
        return conversacion
