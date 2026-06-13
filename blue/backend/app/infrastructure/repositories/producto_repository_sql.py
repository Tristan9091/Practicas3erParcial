from sqlalchemy.orm import Session
from app.domain.ports.producto_repository import ProductoRepository
from app.domain.entities.producto import Producto
from app.infrastructure.database.models import ProductoModel
from typing import List, Optional

class ProductoRepositorySQL(ProductoRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: ProductoModel) -> Producto:
        return Producto(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            vendedor=model.vendedor,
            precio=model.precio,
            stock=model.stock,
            imagenes=model.imagenes or []
        )

    def guardar(self, producto: Producto):
        model = ProductoModel(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            vendedor=producto.vendedor,
            precio=producto.precio,
            stock=producto.stock,
            imagenes=producto.imagenes
        )
        self.db.add(model)
        self.db.commit()

    def obtener_por_id(self, id: str) -> Optional[Producto]:
        model = self.db.query(ProductoModel).filter(ProductoModel.id == id).first()
        return self._to_entity(model) if model else None

    def listar_todos(self) -> List[Producto]:
        return [self._to_entity(m) for m in self.db.query(ProductoModel).all()]

    def actualizar(self, producto: Producto):
        model = self.db.query(ProductoModel).filter(ProductoModel.id == producto.id).first()
        if not model:
            raise ValueError("Producto no encontrado")
        model.nombre = producto.nombre
        model.descripcion = producto.descripcion
        model.vendedor = producto.vendedor
        model.precio = producto.precio
        model.stock = producto.stock
        model.imagenes = producto.imagenes
        self.db.commit()

    def eliminar(self, id: str):
        model = self.db.query(ProductoModel).filter(ProductoModel.id == id).first()
        if model:
            self.db.delete(model)
            self.db.commit()

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        return [self._to_entity(m) for m in
                self.db.query(ProductoModel).filter(ProductoModel.nombre.ilike(f"%{nombre}%")).all()]

    def filtrar_por_precio(self, precio_min: float, precio_max: float) -> List[Producto]:
        return [self._to_entity(m) for m in
                self.db.query(ProductoModel).filter(
                    ProductoModel.precio >= precio_min,
                    ProductoModel.precio <= precio_max
                ).all()]
