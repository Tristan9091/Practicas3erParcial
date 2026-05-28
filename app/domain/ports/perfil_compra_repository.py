from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.perfil_compra import PerfilCompra

class PerfilCompraRepository(ABC):
    @abstractmethod
    def guardar(self, perfil: PerfilCompra):
        pass

    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[PerfilCompra]:
        pass

    @abstractmethod
    def actualizar(self, perfil: PerfilCompra):
        pass
