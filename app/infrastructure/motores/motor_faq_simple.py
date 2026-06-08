import unicodedata
from typing import Optional
from app.domain.ports.motor_respuestas import MotorRespuestas
from app.domain.ports.faq_repository import FaqRepository
from app.domain.entities.mensaje_chat import MensajeChat


def _normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


class MotorFaqSimple(MotorRespuestas):
    def __init__(self, faq_repository: FaqRepository):
        self.faq_repository = faq_repository

    def responder(self, mensaje_cliente: str) -> Optional[MensajeChat]:
        texto = _normalizar(mensaje_cliente)
        faqs = self.faq_repository.listar_todas()

        mejor_faq = None
        mejor_puntaje = 0
        for faq in faqs:
            puntaje = sum(
                1 for palabra in faq.palabras_clave
                if _normalizar(palabra) in texto
            )
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_faq = faq

        if mejor_faq is None:
            return None

        return MensajeChat(
            autor="asistente",
            contenido=mejor_faq.respuesta,
            tipo="auto",
        )