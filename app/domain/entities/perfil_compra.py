from dataclasses import dataclass, field
from typing import List

@dataclass
class PerfilCompra:
    id: str
    nombre: str
    email: str
    direccion: str
    metodo_pago: str
    preferencias: List[str] = field(default_factory=list)
