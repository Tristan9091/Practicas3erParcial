"""Prueba de humo del chat SIN necesidad de MySQL.

Levanta la app con una base SQLite en memoria y hace un round-trip completo
por WebSocket. Sirve para verificar que toda la logica del chat funciona
antes de la demo, sin depender de XAMPP.

Uso:
    pip install -r requirements.txt
    pip install httpx          # solo para esta prueba (TestClient)
    python3 probar_chat.py
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Forzamos SQLite en memoria ANTES de importar la app.
import app.infrastructure.database.base as base
_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
base.engine = _engine
base.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

from fastapi.testclient import TestClient
import app.main as main_module

client = TestClient(main_module.app)


def check(condicion, ok, error):
    if condicion:
        print(f"  OK  {ok}")
    else:
        print(f"  XX  {error}")
        sys.exit(1)


print("\n== Prueba de humo del chat ==\n")

faqs = client.get("/chat/faqs").json()
check(len(faqs) == 5, f"FAQs sembradas: {len(faqs)}", "No se sembraron las 5 FAQs")

r = client.post("/chat/conversaciones", json={"cliente_id": "demo"})
check(r.status_code == 200, "Conversacion creada", f"Fallo al crear conversacion: {r.text}")
conv_id = r.json()["conversacion_id"]

preguntas = [
    "Cuanto tardan en llegar los envios?",
    "Que metodos de pago aceptan?",
    "Cual es el horario de atencion?",
    "Como veo el estado de mi pedido?",
    "Tienen descuento en cubos de neon morados?",  # sin match -> escala
]

print("\n  Conversacion:")
with client.websocket_connect(f"/ws/chat/{conv_id}") as ws:
    ws.receive_json()  # bienvenida
    for pregunta in preguntas:
        ws.send_text(pregunta)
        eco = ws.receive_json()
        resp = ws.receive_json()
        check(eco["autor"] == "cliente" and resp["autor"] == "asistente",
              "", "Los autores de los mensajes no son los esperados")
        print(f"    Cliente : {pregunta}")
        print(f"    Asistente: {resp['contenido'][:65]}...")
        print()

hist = client.get(f"/chat/conversaciones/{conv_id}").json()
check(len(hist["mensajes"]) == len(preguntas) * 2,
      f"Mensajes persistidos: {len(hist['mensajes'])}", "No se guardaron todos los mensajes")
check(hist["estado"] == "escalada",
      "Conversacion escalada tras pregunta sin match", f"Estado inesperado: {hist['estado']}")

print("\n== TODO EN ORDEN ==\n")