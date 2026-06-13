from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from app.adapters.http.dependencies import get_current_user, require_operador_o_admin
from sqlalchemy.orm import Session
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.producto_repository_sql import ProductoRepositorySQL
from app.infrastructure.repositories.orden_compra_repository_sql import OrdenCompraRepositorySQL
from app.application.use_cases.orden_compra_use_cases import (
    CrearOrdenCompra, ObtenerOrdenCompra, ListarOrdenesPorPerfil, CancelarOrden,
    ListarTodasLasOrdenes, ActualizarEstadoOrden
)

orden_compra_router = APIRouter()

class OrdenItemRequest(BaseModel):
    producto_id: str = Field(min_length=1)
    nombre_producto: str = Field(min_length=1, max_length=255)
    precio_unitario: float = Field(gt=0)
    cantidad: int = Field(ge=1)

class OrdenCompraRequest(BaseModel):
    perfil_id: str
    items: List[OrdenItemRequest]
    direccion_envio: str = ""
    metodo_pago: str = ""

class EstadoUpdateRequest(BaseModel):
    estado: str = Field(min_length=1)

@orden_compra_router.post("/ordenes")
def crear_orden(request: OrdenCompraRequest, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    try:
        return CrearOrdenCompra(
            OrdenCompraRepositorySQL(db),
            ProductoRepositorySQL(db)
        ).ejecutar(
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Listado de TODAS las ordenes: solo operador/admin (gestion de ordenes del backoffice)
@orden_compra_router.get("/ordenes")
def listar_todas_las_ordenes(db: Session = Depends(get_db), usuario = Depends(require_operador_o_admin)):
    return ListarTodasLasOrdenes(OrdenCompraRepositorySQL(db)).ejecutar()

@orden_compra_router.get("/ordenes/{id}")
def obtener_orden(id: str, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    try:
        return ObtenerOrdenCompra(OrdenCompraRepositorySQL(db)).ejecutar(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@orden_compra_router.get("/ordenes/perfil/{perfil_id}")
def listar_ordenes_por_perfil(perfil_id: str, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    return ListarOrdenesPorPerfil(OrdenCompraRepositorySQL(db)).ejecutar(perfil_id)

@orden_compra_router.patch("/ordenes/{id}/cancelar")
def cancelar_orden(id: str, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    try:
        return CancelarOrden(OrdenCompraRepositorySQL(db)).ejecutar(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@orden_compra_router.patch("/ordenes/{id}/estado")
def actualizar_estado_orden(id: str, request: EstadoUpdateRequest, db: Session = Depends(get_db), usuario = Depends(require_operador_o_admin)):
    try:
        return ActualizarEstadoOrden(OrdenCompraRepositorySQL(db)).ejecutar(id, request.estado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))