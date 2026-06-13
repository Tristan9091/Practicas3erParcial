from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.usuario import Usuario

class UsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario):
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        pass

    @abstractmethod
    def actualizar(self, usuario: Usuario):
        pass