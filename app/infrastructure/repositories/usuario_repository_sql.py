from sqlalchemy.orm import Session
from app.domain.ports.usuario_repository import UsuarioRepository
from app.domain.entities.usuario import Usuario
from app.infrastructure.database.models import UsuarioModel
from typing import Optional

class UsuarioRepositorySQL(UsuarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            rol=model.rol,
            hashed_password=model.hashed_password,
            fecha_registro=model.fecha_registro
        )
        
    def guardar(self, usuario: Usuario):
        model = UsuarioModel(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            rol=usuario.rol,
            hashed_password=usuario.hashed_password,
            fecha_registro=usuario.fecha_registro
        )
        self.db.add(model)
        self.db.commit()

    def obtener_por_id(self, id: str) -> Optional[Usuario]:
        model = self.db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
        return self._to_entity(model) if model else None
        
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        model = self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
        return self._to_entity(model) if model else None
        
    def buscar_por_nombre(self, nombre: str) -> Optional[Usuario]:
        model = self.db.query(UsuarioModel).filter(UsuarioModel.nombre == nombre).first()
        return self._to_entity(model) if model else None
        