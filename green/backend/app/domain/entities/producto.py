from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Producto:
    id: str
    nombre: str
    descripcion: str
    vendedor: str
    precio: float
    stock: int = 0
    imagenes: List[str] = field(default_factory=list)
