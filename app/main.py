from fastapi import FastAPI
from app.infrastructure.database.base import engine
from app.infrastructure.database import models
from app.adapters.http.producto_router import producto_router
from app.adapters.http.perfil_compra_router import perfil_compra_router
from app.adapters.http.orden_compra_router import orden_compra_router
from app.adapters.http.auth_router import router as auth_router
from app.realtime.chat_ws import chat_router
import uuid
from app.infrastructure.database.base import SessionLocal
from app.infrastructure.repositories.faq_repository_sql import FaqRepositorySQL
from app.domain.entities.pregunta_frecuente import PreguntaFrecuente

models.Base.metadata.create_all(bind=engine)

def sembrar_faqs():
    db = SessionLocal()
    try:
        repo = FaqRepositorySQL(db)
        if repo.listar_todas():          
            return
        faqs = [
            PreguntaFrecuente(
                id=str(uuid.uuid4()),
                pregunta="¿Cómo consulto el estado de mi orden?",
                respuesta="Puedes ver el estado de tu orden en 'Mis pedidos'. "
                          "Si pagaste hace menos de 24h, aún puede aparecer como pendiente.",
                palabras_clave=["estado", "orden", "pedido", "rastrear", "seguimiento"],
            ),
            PreguntaFrecuente(
                id=str(uuid.uuid4()),
                pregunta="¿Qué métodos de pago aceptan?",
                respuesta="Aceptamos tarjeta de crédito/débito, PayPal y transferencia.",
                palabras_clave=["pago", "pagar", "tarjeta", "paypal", "transferencia", "metodos"],
            ),
            PreguntaFrecuente(
                id=str(uuid.uuid4()),
                pregunta="¿Cuánto tarda el envío?",
                respuesta="Los envíos tardan de 3 a 5 días hábiles según tu ubicación.",
                palabras_clave=["envio", "enviar", "tarda", "llega", "demora", "dias", "tiempo"],
            ),
            PreguntaFrecuente(
                id=str(uuid.uuid4()),
                pregunta="¿Cuál es el horario de atención?",
                respuesta="Atendemos de lunes a viernes de 9:00 a 18:00.",
                palabras_clave=["horario", "atencion", "abren", "cierran", "horas"],
            ),
        ]
        for faq in faqs:
            repo.guardar(faq)
    finally:
        db.close()


sembrar_faqs()

app = FastAPI(
    title="PuzzleStore API",
    description="E-commerce de cubos Rubik, rompecabezas y puzzles",
    version="1.0.0"
)

app.include_router(producto_router, tags=["Productos"])
app.include_router(perfil_compra_router, tags=["Perfiles de Compra"])
app.include_router(orden_compra_router, tags=["Órdenes de Compra"])
app.include_router(auth_router)
app.include_router(chat_router, tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Bienvenido a PuzzleStore API"}
