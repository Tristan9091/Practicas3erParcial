import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.adapters.http.dependencies import require_admin
from app.domain.entities.faq import FAQ
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.faq_repository_sql import FaqRepositorySQL
from app.realtime.dependencias_chat import (
    construir_iniciar_conversacion,
    construir_obtener_historial,
)

chat_router = APIRouter(prefix="/chat")


class IniciarConversacionRequest(BaseModel):
    cliente_id: str = Field(min_length=1, max_length=64)


class FaqRequest(BaseModel):
    pregunta: str = Field(min_length=1, max_length=500)
    respuesta: str = Field(min_length=1, max_length=2000)
    categoria: str = Field(default="general", max_length=100)
    palabras_clave: list[str] = []


@chat_router.post("/conversaciones")
def iniciar_conversacion(request: IniciarConversacionRequest, db: Session = Depends(get_db)):
    conversacion = construir_iniciar_conversacion(db).ejecutar(request.cliente_id)
    return {
        "conversacion_id": conversacion.id,
        "estado": conversacion.estado.value,
        "ws_url": f"/ws/chat/{conversacion.id}",
    }


@chat_router.get("/conversaciones/{conversacion_id}")
def historial(conversacion_id: str, db: Session = Depends(get_db)):
    try:
        conversacion = construir_obtener_historial(db).ejecutar(conversacion_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {
        "id": conversacion.id,
        "cliente_id": conversacion.cliente_id,
        "estado": conversacion.estado.value,
        "mensajes": [
            {
                "autor": m.autor.value,
                "contenido": m.contenido,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in conversacion.mensajes
        ],
    }


@chat_router.get("/faqs")
def listar_faqs(db: Session = Depends(get_db)):
    return FaqRepositorySQL(db).listar_todas()


@chat_router.post("/faqs")
def crear_faq(request: FaqRequest, db: Session = Depends(get_db), usuario=Depends(require_admin)):
    faq = FAQ(
        id=str(uuid.uuid4()),
        pregunta=request.pregunta,
        respuesta=request.respuesta,
        categoria=request.categoria,
        palabras_clave=request.palabras_clave,
    )
    FaqRepositorySQL(db).guardar(faq)
    return faq
