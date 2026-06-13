import uuid
from app.domain.entities.usuario import Usuario
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_EMAIL = "admin@gmail.com"
ROLES_VALIDOS = ["cliente", "operador", "admin"]


class RegistrarUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, nombre, email, password):
        if self.usuario_repository.buscar_por_email(email):
            raise ValueError("El email ya está registrado")
        rol = "admin" if email == ADMIN_EMAIL else "cliente"
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


class ListarUsuarios:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self):
        return self.usuario_repository.listar_todos()


class CambiarRolUsuario:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def ejecutar(self, email, nuevo_rol):
        if nuevo_rol not in ROLES_VALIDOS:
            raise ValueError("Rol no válido")
        if email == ADMIN_EMAIL:
            raise ValueError("No se puede cambiar el rol del administrador principal")
        usuario = self.usuario_repository.buscar_por_email(email)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        usuario.rol = nuevo_rol
        self.usuario_repository.actualizar(usuario)
        return usuario