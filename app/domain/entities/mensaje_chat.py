from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MensajeChat:
    autor: str          
    contenido: str
    tipo: str = "texto" 
    fecha: datetime = field(default_factory=datetime.now)