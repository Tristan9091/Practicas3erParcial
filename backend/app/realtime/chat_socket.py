from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.domain.entities.mensaje_chat import MensajeChat, AutorMensaje
from app.infrastructure.database.base import SessionLocal
from app.realtime.connection_manager import manager
from app.realtime.dependencias_chat import (
    construir_obtener_historial,
    construir_procesar_mensaje,
    construir_responder_como_agente,
)
from app.realtime.websocket_notificador import WebSocketNotificador

chat_socket_router = APIRouter()


@chat_socket_router.websocket("/ws/chat/{conversacion_id}")
async def chat_websocket(websocket: WebSocket, conversacion_id: str):
    notificador = WebSocketNotificador(manager)

    db = SessionLocal()
    try:
        conversacion = construir_obtener_historial(db).ejecutar(conversacion_id)
        cliente_id = conversacion.cliente_id
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

            db = SessionLocal()
            try:
                caso_uso = construir_procesar_mensaje(db)
                mensaje_cliente, mensaje_asistente, respuesta = caso_uso.ejecutar(
                    conversacion_id, texto
                )
            finally:
                db.close()

            await notificador.notificar(conversacion_id, mensaje_cliente)
            await notificador.notificar(conversacion_id, mensaje_asistente)

            # Si el bot no supo responder, avisamos a los agentes (admin/operador)
            # conectados al canal de staff para que respondan en vivo.
            if not respuesta.manejada:
                await manager.difundir_staff(
                    {
                        "tipo": "escalamiento",
                        "conversacion_id": conversacion_id,
                        "cliente_id": cliente_id,
                        "contenido": texto,
                    }
                )

    except WebSocketDisconnect:
        manager.desconectar(conversacion_id, websocket)
    except Exception:
        manager.desconectar(conversacion_id, websocket)
        await websocket.close(code=1011)


# Canal para agentes (admin/operador): reciben escalamientos y responden en vivo.
@chat_socket_router.websocket("/ws/staff")
async def staff_websocket(websocket: WebSocket):
    notificador = WebSocketNotificador(manager)
    await manager.conectar_staff(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            conversacion_id = data.get("conversacion_id")
            contenido = (data.get("contenido") or "").strip()
            if not conversacion_id or not contenido:
                continue

            db = SessionLocal()
            try:
                mensaje = construir_responder_como_agente(db).ejecutar(
                    conversacion_id, contenido
                )
            finally:
                db.close()

            await notificador.notificar(conversacion_id, mensaje)

    except WebSocketDisconnect:
        manager.desconectar_staff(websocket)
    except Exception:
        manager.desconectar_staff(websocket)