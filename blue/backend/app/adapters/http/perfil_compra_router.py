from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.database.base import get_db
from app.adapters.http.dependencies import get_current_user
from app.infrastructure.repositories.perfil_compra_repository_sql import PerfilCompraRepositorySQL
from app.application.use_cases.perfil_compra_use_cases import (
    CrearPerfilCompra, ObtenerPerfilCompra, ActualizarPerfilCompra
)

perfil_compra_router = APIRouter()

class PerfilCompraRequest(BaseModel):
    nombre: str
    email: EmailStr  
    direccion: str = ""
    metodo_pago: str = ""
    preferencias: List[str] = []

class PerfilCompraUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None 
    direccion: Optional[str] = None
    metodo_pago: Optional[str] = None
    preferencias: Optional[List[str]] = None

@perfil_compra_router.post("/perfiles", status_code=status.HTTP_201_CREATED)
def crear_perfil(request: PerfilCompraRequest, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    return CrearPerfilCompra(PerfilCompraRepositorySQL(db)).ejecutar(
        nombre=request.nombre,
        email=request.email,
        direccion=request.direccion,
        metodo_pago=request.metodo_pago,
        preferencias=request.preferencias
    )

@perfil_compra_router.get("/perfiles/{id}")
def obtener_perfil(id: str, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    try:
        return ObtenerPerfilCompra(PerfilCompraRepositorySQL(db)).ejecutar(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@perfil_compra_router.put("/perfiles/{id}")
def actualizar_perfil(id: str, request: PerfilCompraUpdateRequest, db: Session = Depends(get_db), usuario = Depends(get_current_user)):
    try:
        return ActualizarPerfilCompra(PerfilCompraRepositorySQL(db)).ejecutar(
            id=id,
            nombre=request.nombre,
            email=request.email,
            direccion=request.direccion,
            metodo_pago=request.metodo_pago,
            preferencias=request.preferencias
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
