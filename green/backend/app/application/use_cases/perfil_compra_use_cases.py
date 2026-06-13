import uuid
from app.domain.entities.perfil_compra import PerfilCompra

class CrearPerfilCompra:
    def __init__(self, perfil_compra_repository):
        self.perfil_compra_repository = perfil_compra_repository

    def ejecutar(self, nombre, email, direccion="", metodo_pago="", preferencias=None):
        nuevo_perfil = PerfilCompra(
            id=str(uuid.uuid4()),
            nombre=nombre,
            email=email,
            direccion=direccion,
            metodo_pago=metodo_pago,
            preferencias=preferencias or []
        )
        self.perfil_compra_repository.guardar(nuevo_perfil)
        return nuevo_perfil

class ObtenerPerfilCompra:
    def __init__(self, perfil_compra_repository):
        self.perfil_compra_repository = perfil_compra_repository

    def ejecutar(self, nombre):
        perfil = self.perfil_compra_repository.obtener_por_nombre(nombre)
        if not perfil:
            raise ValueError("Perfil no encontrado")
        return perfil

class ActualizarPerfilCompra:
    def __init__(self, perfil_compra_repository):
        self.perfil_compra_repository = perfil_compra_repository

    def ejecutar(self, nombre, email=None, direccion=None, metodo_pago=None, preferencias=None):
        perfil = self.perfil_compra_repository.obtener_por_nombre(nombre)
        if not perfil:
            raise ValueError("Perfil de compra no encontrado")
        if nombre:
            perfil.nombre = nombre
        if email:
            perfil.email = email
        if direccion:
            perfil.direccion = direccion
        if metodo_pago:
            perfil.metodo_pago = metodo_pago
        if preferencias is not None:
            perfil.preferencias = preferencias
        self.perfil_compra_repository.actualizar(perfil)
        return perfil
