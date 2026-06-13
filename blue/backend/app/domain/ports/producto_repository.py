from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.producto import Producto

class ProductoRepository(ABC):
    @abstractmethod
    def guardar(self, producto: Producto):
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def actualizar(self, producto: Producto):
        pass

    @abstractmethod
    def eliminar(self, id: str):
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        pass

    @abstractmethod
    def filtrar_por_precio(self, precio_min: float, precio_max: float) -> List[Producto]:
        pass
