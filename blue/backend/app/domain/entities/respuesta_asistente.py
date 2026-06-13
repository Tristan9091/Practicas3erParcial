from dataclasses import dataclass
from typing import Optional


@dataclass
class RespuestaAsistente:
    contenido: str
    confianza: float = 0.0
    manejada: bool = True
    faq_id: Optional[str] = None
    fuente: str = "desconocida"
