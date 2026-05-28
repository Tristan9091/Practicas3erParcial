# PuzzleStore API

E-commerce de cubos Rubik, rompecabezas y puzzles, desarrollado con FastAPI siguiendo Arquitectura Hexagonal.

## Requisitos

- Python 3.11+
- XAMPP con MySQL corriendo
- Base de datos `puzzlestore` creada en phpMyAdmin

## Instalación

```bash
pip3 install -r requirements.txt
```

## Ejecutar el servidor

```bash
python3 -m uvicorn app.main:app --reload
```

## Documentación interactiva

Una vez corriendo, visita: http://127.0.0.1:8000/docs

## Base de datos

Las tablas se crean automáticamente al iniciar el servidor:

- `productos`
- `perfiles_compra`
- `ordenes_compra`
- `orden_items`

## Endpoints principales

### Productos

- `POST /productos` — Crear producto
- `GET /productos` — Listar todos
- `GET /productos/{id}` — Obtener por ID
- `PUT /productos/{id}` — Actualizar
- `DELETE /productos/{id}` — Eliminar
- `GET /productos/buscar/{nombre}` — Buscar por nombre
- `GET /productos/filtrar?precio_min=X&precio_max=Y` — Filtrar por precio

### Perfiles de Compra

- `POST /perfiles` — Crear perfil
- `GET /perfiles/{id}` — Obtener por ID
- `PUT /perfiles/{id}` — Actualizar

### Órdenes de Compra

- `POST /ordenes` — Crear orden
- `GET /ordenes/{id}` — Obtener por ID
- `GET /ordenes/perfil/{perfil_id}` — Listar órdenes de un perfil
- `PATCH /ordenes/{id}/cancelar` — Cancelar orden

## Arquitectura Hexagonal

El sistema separa:

- **Dominio**: lógica y entidades puras, sin dependencias externas
- **Aplicación**: casos de uso que orquestan la lógica
- **Infraestructura**: implementación concreta con MySQL via SQLAlchemy
- **Adaptadores**: capa HTTP que conecta el mundo exterior con los casos de uso
