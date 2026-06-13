from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from app.adapters.http.dependencies import get_current_user, require_admin, require_operador_o_admin
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.producto_repository_sql import ProductoRepositorySQL
from app.application.use_cases.producto_use_cases import (
    CrearProductos, ObtenerProducto, ListarProductos,
    ActualizarProducto, EliminarProducto,
    BuscarProductosPorNombre, FiltrarProductosPorPrecio
)

producto_router = APIRouter()

class ProductoRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    descripcion: str = Field(default="", max_length=1000)
    vendedor: str = Field(default="", max_length=255)
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    imagenes: List[str] = []

class ProductoUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=255)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    vendedor: Optional[str] = Field(default=None, max_length=255)
    precio: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    imagenes: Optional[List[str]] = None

@producto_router.post("/productos")
def crear_producto(request: ProductoRequest, db: Session = Depends(get_db), usuario = Depends(require_admin)):
    repositorio = ProductoRepositorySQL(db)
    return CrearProductos(repositorio).ejecutar(
        nombre=request.nombre,
        descripcion=request.descripcion,
        vendedor=request.vendedor,
        precio=request.precio if request.precio >= 0 else 0, 
        stock=request.stock if request.stock >= 0 else 0,
        imagenes=request.imagenes
    )

@producto_router.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return ListarProductos(ProductoRepositorySQL(db)).ejecutar()

@producto_router.get("/productos/buscar/{nombre}")
def buscar_producto(nombre: str, db: Session = Depends(get_db)):
    return BuscarProductosPorNombre(ProductoRepositorySQL(db)).ejecutar(nombre)

@producto_router.get("/productos/filtrar")
def filtrar_por_precio(precio_min: float, precio_max: float, db: Session = Depends(get_db)):
    return FiltrarProductosPorPrecio(ProductoRepositorySQL(db)).ejecutar(precio_min, precio_max)

@producto_router.get("/productos/{id}")
def obtener_producto(id: str, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    try:
        return ObtenerProducto(ProductoRepositorySQL(db)).ejecutar(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@producto_router.put("/productos/{id}")
def actualizar_producto(id: str, request: ProductoUpdateRequest, db: Session = Depends(get_db), usuario = Depends(require_operador_o_admin)):
    try:
        return ActualizarProducto(ProductoRepositorySQL(db)).ejecutar(
            id=id,
            nombre=request.nombre,
            descripcion=request.descripcion,
            vendedor=request.vendedor,
            precio=request.precio if request.precio >= 0 else 0,
            stock=request.stock if request.stock >= 0 else 0,
            imagenes=request.imagenes
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@producto_router.delete("/productos/{id}")
def eliminar_producto(id: str, db: Session = Depends(get_db), usuario = Depends(require_admin)):
    EliminarProducto(ProductoRepositorySQL(db)).ejecutar(id)
    return {"message": "Producto eliminado correctamente"}
