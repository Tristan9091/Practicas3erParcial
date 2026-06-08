from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.clientes: Dict[str, WebSocket] = {}
        self.admins: List[WebSocket] = []

    async def conectar_cliente(self, cliente_id: str, websocket: WebSocket):
        await websocket.accept()
        self.clientes[cliente_id] = websocket

    async def conectar_admin(self, websocket: WebSocket):
        await websocket.accept()
        self.admins.append(websocket)

    def desconectar_cliente(self, cliente_id: str):
        self.clientes.pop(cliente_id, None)

    def desconectar_admin(self, websocket: WebSocket):
        if websocket in self.admins:
            self.admins.remove(websocket)

    async def enviar_a_cliente(self, cliente_id: str, mensaje: dict):
        websocket = self.clientes.get(cliente_id)
        if websocket is not None:
            await websocket.send_json(mensaje)

    async def broadcast_admins(self, mensaje: dict):
        desconectados = []
        for ws in self.admins:
            try:
                await ws.send_json(mensaje)
            except Exception:
                desconectados.append(ws)
        for ws in desconectados:
            self.desconectar_admin(ws)

manager = ConnectionManager()