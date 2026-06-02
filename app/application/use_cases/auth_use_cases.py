import uuid
from app.domain.entities.usuario import Usuario
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegistrarUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, nombre, email, password, rol="cliente"):
        if self.usuario_repository.buscar_por_email(email):
            raise ValueError("El email ya está registrado")
        nuevo_usuario = Usuario(
            id=str(uuid.uuid4()),
            nombre=nombre,
            email=email,
            rol=rol,
            hashed_password=pwd_context.hash(password),
        )
        self.usuario_repository.guardar(nuevo_usuario)
        return nuevo_usuario
    
class LoginUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, email, password):
        usuario = self.usuario_repository.buscar_por_email(email)
        if not usuario or not pwd_context.verify(password, usuario.hashed_password):
            raise ValueError("Credenciales inválidas")
        return usuario

