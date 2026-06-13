import uuid
from app.domain.entities.producto import Producto

class CrearProductos:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self, nombre, precio, descripcion="", vendedor="", stock=0, imagenes=None):
        nuevo_producto = Producto(
            id=str(uuid.uuid4()),
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            imagenes=imagenes or [],
            vendedor=vendedor,
            stock=stock
        )
        self.producto_repository.guardar(nuevo_producto)
        return nuevo_producto

class ObtenerProducto:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self, id):
        producto = self.producto_repository.obtener_por_id(id)
        if not producto:
            raise ValueError("Producto no encontrado")
        return producto

class ListarProductos:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self):
        return self.producto_repository.listar_todos()

class ActualizarProducto:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self, id, nombre=None, precio=None, descripcion=None, vendedor=None, stock=None, imagenes=None):
        producto = self.producto_repository.obtener_por_id(id)
        if not producto:
            raise ValueError("Producto no encontrado")
        if nombre:
            producto.nombre = nombre
        if precio:
            producto.precio = precio
        if descripcion:
            producto.descripcion = descripcion
        if vendedor:
            producto.vendedor = vendedor
        if stock is not None:
            producto.stock = stock
        if imagenes is not None:
            producto.imagenes = imagenes
        self.producto_repository.actualizar(producto)
        return producto

class EliminarProducto:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self, id):
        self.producto_repository.eliminar(id)

class BuscarProductosPorNombre:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self, nombre):
        return self.producto_repository.buscar_por_nombre(nombre)

class FiltrarProductosPorPrecio:
    def __init__(self, producto_repository):
        self.producto_repository = producto_repository

    def ejecutar(self, precio_min, precio_max):
        return self.producto_repository.filtrar_por_precio(precio_min, precio_max)
