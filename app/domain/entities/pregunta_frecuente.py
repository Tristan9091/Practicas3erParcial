from dataclasses import dataclass, field
from typing import List

@dataclass
class PreguntaFrecuente:
    id: str
    pregunta: str
    respuesta: str
    palabras_clave: List[str] = field(default_factory=list)