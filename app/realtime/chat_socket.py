from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.domain.entities.mensaje_chat import MensajeChat, AutorMensaje
from app.infrastructure.database.base import SessionLocal
from app.realtime.connection_manager import manager
from app.realtime.dependencias_chat import (
    construir_obtener_historial,
    construir_procesar_mensaje,
)
from app.realtime.websocket_notificador import WebSocketNotificador

chat_socket_router = APIRouter()


@chat_socket_router.websocket("/ws/chat/{conversacion_id}")
async def chat_websocket(websocket: WebSocket, conversacion_id: str):
    notificador = WebSocketNotificador(manager)

    db = SessionLocal()
    try:
        conversacion = construir_obtener_historial(db).ejecutar(conversacion_id)
    except ValueError:
        await websocket.close(code=4404)
        return
    finally:
        db.close()

    await manager.conectar(conversacion_id, websocket)

    await websocket.send_json(
        {
            "autor": AutorMensaje.SISTEMA.value,
            "contenido": "Conectado al chat de soporte de PuzzleStore.",
            "conversacion_id": conversacion_id,
        }
    )

    try:
        while True:
            texto = await websocket.receive_text()
            texto = texto.strip()
            if not texto:
                continue

            # Una sesion de BD por mensaje para reflejar siempre el estado
            # mas reciente y evitar sesiones colgadas en conexiones largas.
            db = SessionLocal()
            try:
                caso_uso = construir_procesar_mensaje(db)
                mensaje_cliente, mensaje_asistente, _ = caso_uso.ejecutar(
                    conversacion_id, texto
                )
            finally:
                db.close()

            # Difundimos ambos mensajes a todos los participantes.
            await notificador.notificar(conversacion_id, mensaje_cliente)
            await notificador.notificar(conversacion_id, mensaje_asistente)

    except WebSocketDisconnect:
        manager.desconectar(conversacion_id, websocket)
    except Exception:
        manager.desconectar(conversacion_id, websocket)
        await websocket.close(code=1011)
