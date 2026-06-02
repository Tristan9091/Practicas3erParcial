from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infrastructure.database.base import Base

class ProductoModel(Base):
    __tablename__ = "productos"

    id = Column(String(36), primary_key=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, default="")
    vendedor = Column(String(255), default="")
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    imagenes = Column(JSON, default=list)

class PerfilCompraModel(Base):
    __tablename__ = "perfiles_compra"

    id = Column(String(36), primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    direccion = Column(String(500), default="")
    metodo_pago = Column(String(100), default="")
    preferencias = Column(JSON, default=list)
    ordenes = relationship("OrdenCompraModel", back_populates="perfil")

class OrdenCompraModel(Base):
    __tablename__ = "ordenes_compra"

    id = Column(String(36), primary_key=True)
    perfil_id = Column(String(36), ForeignKey("perfiles_compra.id"), nullable=False)
    total = Column(Float, nullable=False)
    estado = Column(String(50), default="pendiente")
    direccion_envio = Column(String(500), default="")
    metodo_pago = Column(String(100), default="")
    fecha = Column(DateTime, default=datetime.now)
    perfil = relationship("PerfilCompraModel", back_populates="ordenes")
    items = relationship("OrdenItemModel", back_populates="orden")

class OrdenItemModel(Base):
    __tablename__ = "orden_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    orden_id = Column(String(36), ForeignKey("ordenes_compra.id"), nullable=False)
    producto_id = Column(String(36), nullable=False)
    nombre_producto = Column(String(255), nullable=False)
    precio_unitario = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    orden = relationship("OrdenCompraModel", back_populates="items")

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id= Column(String(36), primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    rol = Column(String(50), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)


class FaqModel(Base):
    __tablename__ = "faqs"

    id = Column(String(36), primary_key=True)
    pregunta = Column(String(500), nullable=False)
    respuesta = Column(Text, nullable=False)
    categoria = Column(String(100), default="general")
    palabras_clave = Column(JSON, default=list)


class ConversacionModel(Base):
    __tablename__ = "conversaciones"

    id = Column(String(36), primary_key=True)
    cliente_id = Column(String(36), nullable=False)
    estado = Column(String(50), default="abierta")
    creada_en = Column(DateTime, default=datetime.now)
    mensajes = relationship(
        "MensajeChatModel",
        back_populates="conversacion",
        order_by="MensajeChatModel.timestamp",
    )


class MensajeChatModel(Base):
    __tablename__ = "mensajes_chat"

    id = Column(String(36), primary_key=True)
    conversacion_id = Column(String(36), ForeignKey("conversaciones.id"), nullable=False)
    autor = Column(String(20), nullable=False)
    contenido = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    conversacion = relationship("ConversacionModel", back_populates="mensajes")
