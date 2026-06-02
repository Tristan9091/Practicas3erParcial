from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.conversacion import Conversacion, EstadoConversacion
from app.domain.entities.mensaje_chat import MensajeChat, AutorMensaje
from app.domain.ports.conversacion_repository import ConversacionRepository
from app.infrastructure.database.models import ConversacionModel, MensajeChatModel


class ConversacionRepositorySQL(ConversacionRepository):
    def __init__(self, db: Session):
        self.db = db

    def _mensaje_to_entity(self, model: MensajeChatModel) -> MensajeChat:
        return MensajeChat(
            id=model.id,
            conversacion_id=model.conversacion_id,
            autor=AutorMensaje(model.autor),
            contenido=model.contenido,
            timestamp=model.timestamp,
        )

    def _to_entity(self, model: ConversacionModel) -> Conversacion:
        return Conversacion(
            id=model.id,
            cliente_id=model.cliente_id,
            estado=EstadoConversacion(model.estado),
            creada_en=model.creada_en,
            mensajes=[self._mensaje_to_entity(m) for m in model.mensajes],
        )

    def guardar(self, conversacion: Conversacion) -> None:
        model = ConversacionModel(
            id=conversacion.id,
            cliente_id=conversacion.cliente_id,
            estado=conversacion.estado.value,
            creada_en=conversacion.creada_en,
        )
        self.db.add(model)
        self.db.commit()

    def obtener_por_id(self, id: str) -> Optional[Conversacion]:
        model = (
            self.db.query(ConversacionModel)
            .filter(ConversacionModel.id == id)
            .first()
        )
        return self._to_entity(model) if model else None

    def agregar_mensaje(self, mensaje: MensajeChat) -> None:
        model = MensajeChatModel(
            id=mensaje.id,
            conversacion_id=mensaje.conversacion_id,
            autor=mensaje.autor.value,
            contenido=mensaje.contenido,
            timestamp=mensaje.timestamp,
        )
        self.db.add(model)
        self.db.commit()

    def actualizar_estado(self, conversacion: Conversacion) -> None:
        model = (
            self.db.query(ConversacionModel)
            .filter(ConversacionModel.id == conversacion.id)
            .first()
        )
        if not model:
            raise ValueError("Conversacion no encontrada")
        model.estado = conversacion.estado.value
        self.db.commit()

    def listar_por_cliente(self, cliente_id: str) -> List[Conversacion]:
        modelos = (
            self.db.query(ConversacionModel)
            .filter(ConversacionModel.cliente_id == cliente_id)
            .all()
        )
        return [self._to_entity(m) for m in modelos]
