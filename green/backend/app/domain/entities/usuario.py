from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Usuario:
    id: str
    nombre: str
    email: str
    rol: str
    hashed_password: str
    fecha_registro: datetime = field(default_factory=datetime.now)    