from dataclasses import dataclass, field
from typing import List
from datetime import datetime

@dataclass
class OrdenItem:
    producto_id: str
    nombre_producto: str
    precio_unitario: float
    cantidad: int

@dataclass
class OrdenCompra:
    id: str
    perfil_id: str
    total: float
    estado: str
    direccion_envio: str
    metodo_pago: str
    items: List[OrdenItem] = field(default_factory=list)
    fecha: datetime = field(default_factory=datetime.now)
