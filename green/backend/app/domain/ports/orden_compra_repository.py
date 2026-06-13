from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.orden_compra import OrdenCompra

class OrdenCompraRepository(ABC):
    @abstractmethod
    def guardar(self, orden: OrdenCompra):
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[OrdenCompra]:
        pass

    @abstractmethod
    def actualizar(self, orden: OrdenCompra):
        pass

    @abstractmethod
    def listar_por_perfil_id(self, perfil_id: str) -> List[OrdenCompra]:
        pass

    @abstractmethod
    def listar_todas(self) -> List[OrdenCompra]:
        pass