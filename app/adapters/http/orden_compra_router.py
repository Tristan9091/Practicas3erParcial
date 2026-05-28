from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.orden_compra_repository_sql import OrdenCompraRepositorySQL
from app.application.use_cases.orden_compra_use_cases import (
    CrearOrdenCompra, ObtenerOrdenCompra, ListarOrdenesPorPerfil, CancelarOrden
)

orden_compra_router = APIRouter()

class OrdenItemRequest(BaseModel):
    producto_id: str
    nombre_producto: str
    precio_unitario: float
    cantidad: int

class OrdenCompraRequest(BaseModel):
    perfil_id: str
    items: List[OrdenItemRequest]
    direccion_envio: str = ""
    metodo_pago: str = ""

@orden_compra_router.post("/ordenes")
def crear_orden(request: OrdenCompraRequest, db: Session = Depends(get_db)):
    return CrearOrdenCompra(OrdenCompraRepositorySQL(db)).ejecutar(
        perfil_id=request.perfil_id,
        items=[{
            'producto_id': item.producto_id,
            'nombre_producto': item.nombre_producto,
            'precio_unitario': item.precio_unitario,
            'cantidad': item.cantidad
        } for item in request.items],
        direccion_envio=request.direccion_envio,
        metodo_pago=request.metodo_pago
    )

@orden_compra_router.get("/ordenes/{id}")
def obtener_orden(id: str, db: Session = Depends(get_db)):
    try:
        return ObtenerOrdenCompra(OrdenCompraRepositorySQL(db)).ejecutar(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@orden_compra_router.get("/ordenes/perfil/{perfil_id}")
def listar_ordenes_por_perfil(perfil_id: str, db: Session = Depends(get_db)):
    return ListarOrdenesPorPerfil(OrdenCompraRepositorySQL(db)).ejecutar(perfil_id)

@orden_compra_router.patch("/ordenes/{id}/cancelar")
def cancelar_orden(id: str, db: Session = Depends(get_db)):
    try:
        return CancelarOrden(OrdenCompraRepositorySQL(db)).ejecutar(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
