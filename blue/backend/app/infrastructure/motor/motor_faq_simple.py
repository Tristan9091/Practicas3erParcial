from app.domain.entities.conversacion import Conversacion
from app.domain.entities.faq import FAQ
from app.domain.entities.respuesta_asistente import RespuestaAsistente
from app.domain.ports.faq_repository import FaqRepository
from app.domain.ports.motor_respuestas import MotorRespuestas
from app.infrastructure.motor.texto import normalizar, tokenizar


class MotorFaqSimple(MotorRespuestas):
    UMBRAL_COINCIDENCIA = 0.35
    PESO_PALABRA_CLAVE = 2.0

    def __init__(self, faq_repository: FaqRepository):
        self.faq_repository = faq_repository

    def _puntaje(self, tokens_mensaje: set, faq: FAQ) -> float:
        if not tokens_mensaje:
            return 0.0

        tokens_pregunta = set(tokenizar(faq.pregunta))
        solapamiento = len(tokens_mensaje & tokens_pregunta)

        claves_norm = {normalizar(k) for k in faq.palabras_clave}
        coincidencias_clave = sum(
            1 for clave in claves_norm if clave and clave in tokens_mensaje
        )

        bruto = solapamiento + self.PESO_PALABRA_CLAVE * coincidencias_clave
        maximo = len(tokens_mensaje) + self.PESO_PALABRA_CLAVE
        return min(bruto / maximo, 1.0) if maximo else 0.0

    def responder(self, pregunta: str, conversacion: Conversacion) -> RespuestaAsistente:
        tokens_mensaje = set(tokenizar(pregunta))
        candidatas = self.faq_repository.buscar_candidatas(pregunta)

        mejor_faq: FAQ | None = None
        mejor_puntaje = 0.0
        for faq in candidatas:
            puntaje = self._puntaje(tokens_mensaje, faq)
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_faq = faq

        if mejor_faq and mejor_puntaje >= self.UMBRAL_COINCIDENCIA:
            return RespuestaAsistente(
                contenido=mejor_faq.respuesta,
                confianza=round(mejor_puntaje, 3),
                manejada=True,
                faq_id=mejor_faq.id,
                fuente="faq_simple",
            )

        return RespuestaAsistente(
            contenido=(
                "Por ahora no encontre una respuesta automatica para tu "
                "consulta. La pase a un asistente del equipo, que te "
                "contactara en breve. Tambien puedes reformular tu pregunta."
            ),
            confianza=round(mejor_puntaje, 3),
            manejada=False,
            fuente="faq_simple",
        )
