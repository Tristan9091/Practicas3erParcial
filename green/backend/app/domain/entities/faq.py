from dataclasses import dataclass, field
from typing import List


@dataclass
class FAQ:
    id: str
    pregunta: str
    respuesta: str
    categoria: str = "general"
    palabras_clave: List[str] = field(default_factory=list)
