from sqlalchemy.orm import Session
from app.domain.ports.perfil_compra_repository import PerfilCompraRepository
from app.domain.entities.perfil_compra import PerfilCompra
from app.infrastructure.database.models import PerfilCompraModel
from typing import Optional

class PerfilCompraRepositorySQL(PerfilCompraRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: PerfilCompraModel) -> PerfilCompra:
        return PerfilCompra(
            id=model.id,
            nombre=model.nombre,
            email=model.email,
            direccion=model.direccion,
            metodo_pago=model.metodo_pago,
            preferencias=model.preferencias or []
        )

    def guardar(self, perfil: PerfilCompra):
        model = PerfilCompraModel(
            id=perfil.id,
            nombre=perfil.nombre,
            email=perfil.email,
            direccion=perfil.direccion,
            metodo_pago=perfil.metodo_pago,
            preferencias=perfil.preferencias
        )
        self.db.add(model)
        self.db.commit()

    def obtener_por_nombre(self, nombre: str) -> Optional[PerfilCompra]:
        model = self.db.query(PerfilCompraModel).filter(PerfilCompraModel.nombre == nombre).first()
        return self._to_entity(model) if model else None

    def actualizar(self, perfil: PerfilCompra):
        model = self.db.query(PerfilCompraModel).filter(PerfilCompraModel.id == perfil.id).first()
        if not model:
            raise ValueError("Perfil no encontrado")
        model.nombre = perfil.nombre
        model.email = perfil.email
        model.direccion = perfil.direccion
        model.metodo_pago = perfil.metodo_pago
        model.preferencias = perfil.preferencias
        self.db.commit()
