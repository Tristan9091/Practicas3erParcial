from sqlalchemy.orm import Session
from app.domain.ports.orden_compra_repository import OrdenCompraRepository
from app.domain.entities.orden_compra import OrdenCompra, OrdenItem
from app.infrastructure.database.models import OrdenCompraModel, OrdenItemModel
from typing import List, Optional

class OrdenCompraRepositorySQL(OrdenCompraRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: OrdenCompraModel) -> OrdenCompra:
        return OrdenCompra(
            id=model.id,
            perfil_id=model.perfil_id,
            total=model.total,
            estado=model.estado,
            direccion_envio=model.direccion_envio,
            metodo_pago=model.metodo_pago,
            fecha=model.fecha,
            items=[OrdenItem(
                producto_id=item.producto_id,
                nombre_producto=item.nombre_producto,
                precio_unitario=item.precio_unitario,
                cantidad=item.cantidad
            ) for item in model.items]
        )

    def guardar(self, orden: OrdenCompra):
        model = OrdenCompraModel(
            id=orden.id,
            perfil_id=orden.perfil_id,
            total=orden.total,
            estado=orden.estado,
            direccion_envio=orden.direccion_envio,
            metodo_pago=orden.metodo_pago,
            fecha=orden.fecha
        )
        self.db.add(model)
        self.db.flush()
        for item in orden.items:
            item_model = OrdenItemModel(
                orden_id=orden.id,
                producto_id=item.producto_id,
                nombre_producto=item.nombre_producto,
                precio_unitario=item.precio_unitario,
                cantidad=item.cantidad
            )
            self.db.add(item_model)
        self.db.commit()

    def obtener_por_id(self, id: str) -> Optional[OrdenCompra]:
        model = self.db.query(OrdenCompraModel).filter(OrdenCompraModel.id == id).first()
        return self._to_entity(model) if model else None

    def actualizar(self, orden: OrdenCompra):
        model = self.db.query(OrdenCompraModel).filter(OrdenCompraModel.id == orden.id).first()
        if not model:
            raise ValueError("Orden no encontrada")
        model.estado = orden.estado
        self.db.commit()

    def listar_todas(self) -> List[OrdenCompra]:
        return [self._to_entity(m) for m in
                self.db.query(OrdenCompraModel).order_by(OrdenCompraModel.fecha.desc()).all()]

    def listar_por_perfil_id(self, perfil_id: str) -> List[OrdenCompra]:
        return [self._to_entity(m) for m in
                self.db.query(OrdenCompraModel).filter(OrdenCompraModel.perfil_id == perfil_id).all()]