from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from app.infrastructure.database.base import get_db
from app.infrastructure.repositories.usuario_repository_sql import UsuarioRepositorySQL
from app.application.use_cases.auth_use_cases import (
    RegistrarUsuario, LoginUsuario, ListarUsuarios, CambiarRolUsuario
)
from app.security.jwt_handler import crear_access_token, crear_refresh_token, verificar_token
from app.adapters.http.dependencies import require_admin

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)

class RefreshRequest(BaseModel):
    refresh_token: str

class CambiarRolRequest(BaseModel):
    rol: str = Field(pattern="^(admin|operador|cliente)$")

@router.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    try:
        registrar_usuario = RegistrarUsuario(UsuarioRepositorySQL(db))
        nuevo_usuario = registrar_usuario.ejecutar(
            nombre=user.nombre,
            email=user.email,
            password=user.password
        )
        return {"message": "Usuario registrado exitosamente", "usuario_id": nuevo_usuario.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        login_usuario = LoginUsuario(UsuarioRepositorySQL(db))
        usuario = login_usuario.ejecutar(email=form_data.username, password=form_data.password)
        access_token = crear_access_token(data={"sub": usuario.email, "rol": usuario.rol})
        refresh_token = crear_refresh_token(data={"sub": usuario.email, "rol": usuario.rol})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh")
def refresh_token(request: RefreshRequest):
    payload = verificar_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token de refresco inválido o expirado")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Token de refresco inválido")
    new_access_token = crear_access_token(data={"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db), usuario = Depends(require_admin)):
    usuarios = ListarUsuarios(UsuarioRepositorySQL(db)).ejecutar()
    return [
        {"id": u.id, "nombre": u.nombre, "email": u.email, "rol": u.rol,
         "fecha_registro": u.fecha_registro.isoformat() if u.fecha_registro else None}
        for u in usuarios
    ]

@router.patch("/usuarios/{email}/rol")
def cambiar_rol(email: str, request: CambiarRolRequest, db: Session = Depends(get_db), usuario = Depends(require_admin)):
    try:
        u = CambiarRolUsuario(UsuarioRepositorySQL(db)).ejecutar(email, request.rol)
        return {"email": u.email, "rol": u.rol}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))