from app.domain.entities.mensaje_chat import MensajeChat
from app.domain.ports.notificador_tiempo_real import NotificadorTiempoReal
from app.realtime.connection_manager import ConnectionManager


class WebSocketNotificador(NotificadorTiempoReal):
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def notificar(self, conversacion_id: str, mensaje: MensajeChat) -> None:
        await self.manager.difundir(
            conversacion_id,
            {
                "id": mensaje.id,
                "conversacion_id": mensaje.conversacion_id,
                "autor": mensaje.autor.value,
                "contenido": mensaje.contenido,
                "timestamp": mensaje.timestamp.isoformat(),
            },
        )
