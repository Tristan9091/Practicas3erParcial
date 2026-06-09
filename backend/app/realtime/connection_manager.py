from typing import Dict, Set

from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self._conexiones: Dict[str, Set[WebSocket]] = {}
        self._staff: Set[WebSocket] = set()

    async def conectar(self, conversacion_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._conexiones.setdefault(conversacion_id, set()).add(websocket)

    def desconectar(self, conversacion_id: str, websocket: WebSocket) -> None:
        sockets = self._conexiones.get(conversacion_id)
        if not sockets:
            return
        sockets.discard(websocket)
        if not sockets:
            self._conexiones.pop(conversacion_id, None)

    async def difundir(self, conversacion_id: str, payload: dict) -> None:
        for websocket in list(self._conexiones.get(conversacion_id, set())):
            try:
                await websocket.send_json(payload)
            except Exception:
                self.desconectar(conversacion_id, websocket)

    async def conectar_staff(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._staff.add(websocket)

    def desconectar_staff(self, websocket: WebSocket) -> None:
        self._staff.discard(websocket)

    async def difundir_staff(self, payload: dict) -> None:
        for websocket in list(self._staff):
            try:
                await websocket.send_json(payload)
            except Exception:
                self.desconectar_staff(websocket)

manager = ConnectionManager()
