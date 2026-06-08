from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.faq_repository_sql import FaqRepositorySQL
from app.infrastructure.motores.motor_faq_simple import MotorFaqSimple
from app.application.use_cases.chat_use_cases import ProcesarMensajeCliente
from app.realtime.connection_manager import manager

chat_router = APIRouter()


@chat_router.websocket("/ws/chat/{cliente_id}")
async def websocket_chat_cliente(
    websocket: WebSocket,
    cliente_id: str,
    db: Session = Depends(get_db),
):
    await manager.conectar_cliente(cliente_id, websocket)

    motor = MotorFaqSimple(FaqRepositorySQL(db))
    procesar = ProcesarMensajeCliente(motor)

    try:
        while True:
            data = await websocket.receive_json()
            contenido = data.get("contenido", "").strip()
            if not contenido:
                continue

            respuesta = procesar.ejecutar(contenido)

            if respuesta is not None:
                # Coincidió con una FAQ -> respuesta automática al cliente.
                await manager.enviar_a_cliente(cliente_id, {
                    "autor": respuesta.autor,
                    "contenido": respuesta.contenido,
                    "tipo": respuesta.tipo,
                    "fecha": respuesta.fecha.isoformat(),
                })
            else:
                # Nadie supo responder -> escalar a TODOS los admins (en vivo).
                await manager.broadcast_admins({
                    "tipo": "escalamiento",
                    "cliente_id": cliente_id,
                    "contenido": contenido,
                })
                await manager.enviar_a_cliente(cliente_id, {
                    "autor": "asistente",
                    "contenido": "Un momento, un agente te responderá en breve.",
                    "tipo": "info",
                })
    except WebSocketDisconnect:
        manager.desconectar_cliente(cliente_id)


@chat_router.websocket("/ws/admin")
async def websocket_admin(websocket: WebSocket):
    await manager.conectar_admin(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            cliente_id = data.get("cliente_id")
            contenido = data.get("contenido", "").strip()
            if not cliente_id or not contenido:
                continue
            await manager.enviar_a_cliente(cliente_id, {
                "autor": "asistente",
                "contenido": contenido,
                "tipo": "humano",
            })
    except WebSocketDisconnect:
        manager.desconectar_admin(websocket)