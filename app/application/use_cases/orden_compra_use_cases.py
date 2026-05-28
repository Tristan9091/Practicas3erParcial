import uuid
from app.domain.entities.orden_compra import OrdenCompra, OrdenItem

class CrearOrdenCompra:
    def __init__(self, orden_compra_repository):
        self.orden_compra_repository = orden_compra_repository

    def ejecutar(self, perfil_id, items, direccion_envio="", metodo_pago=""):
        nueva_orden = OrdenCompra(
            id=str(uuid.uuid4()),
            perfil_id=perfil_id,
            items=[OrdenItem(
                producto_id=item['producto_id'],
                nombre_producto=item['nombre_producto'],
                precio_unitario=item['precio_unitario'],
                cantidad=item['cantidad']
            ) for item in items],
            total=sum(item['precio_unitario'] * item['cantidad'] for item in items),
            estado="pendiente",
            direccion_envio=direccion_envio,
            metodo_pago=metodo_pago
        )
        self.orden_compra_repository.guardar(nueva_orden)
        return nueva_orden

class ObtenerOrdenCompra:
    def __init__(self, orden_compra_repository):
        self.orden_compra_repository = orden_compra_repository

    def ejecutar(self, id):
        orden = self.orden_compra_repository.obtener_por_id(id)
        if not orden:
            raise ValueError("Orden no encontrada")
        return orden

class ListarOrdenesPorPerfil:
    def __init__(self, orden_compra_repository):
        self.orden_compra_repository = orden_compra_repository

    def ejecutar(self, perfil_id):
        return self.orden_compra_repository.listar_por_perfil_id(perfil_id)

class CancelarOrden:
    def __init__(self, orden_compra_repository):
        self.orden_compra_repository = orden_compra_repository

    def ejecutar(self, id):
        orden = self.orden_compra_repository.obtener_por_id(id)
        if not orden:
            raise ValueError("Orden de compra no encontrada")
        if orden.estado != "pendiente":
            raise ValueError("Solo se pueden cancelar órdenes pendientes")
        orden.estado = "cancelada"
        self.orden_compra_repository.actualizar(orden)
        return orden
