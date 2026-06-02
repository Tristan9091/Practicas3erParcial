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

---

## Práctica 3 — Chat Cliente-Asistente en tiempo real (WebSockets)

Sistema de chat en tiempo real entre cliente y un asistente automático que
responde preguntas frecuentes (FAQ), diseñado con Arquitectura Hexagonal y
**desacoplado para poder reemplazar el motor de respuestas por IA** en el
futuro sin tocar el resto del sistema.

### Cómo probarlo

1. Levantar el servidor: `python3 -m uvicorn app.main:app --reload`
2. Abrir en el navegador: `http://127.0.0.1:8000/chat-demo`
3. Escribir preguntas como: *"¿cuánto tarda el envío?"*, *"¿qué métodos de
   pago aceptan?"*, *"¿cuál es el horario?"*, *"¿estado de mi pedido?"*.

Las FAQs iniciales se siembran automáticamente al arrancar (si la tabla está
vacía).

### Flujo del WebSocket

1. El cliente crea una conversación: `POST /chat/conversaciones {cliente_id}`
   y recibe un `conversacion_id`.
2. Abre el socket en `ws://HOST/ws/chat/{conversacion_id}`.
3. Envía texto plano por el socket.
4. El servidor difunde en JSON el mensaje del cliente y la respuesta del
   asistente a todos los participantes de la conversación.

### Endpoints añadidos

- `POST /chat/conversaciones` — Inicia una conversación.
- `GET  /chat/conversaciones/{id}` — Historial de mensajes.
- `GET  /chat/faqs` — Lista las FAQs.
- `POST /chat/faqs` — Alta de FAQ (requiere admin).
- `WS   /ws/chat/{conversacion_id}` — Canal de chat en tiempo real.
- `GET  /chat-demo` — Cliente HTML de prueba.

### Arquitectura del chat (hexagonal)

```
app/
├── domain/
│   ├── entities/        FAQ, MensajeChat, Conversacion, RespuestaAsistente
│   └── ports/           MotorRespuestas (★), FaqRepository,
│                        ConversacionRepository, NotificadorTiempoReal
├── application/
│   └── use_cases/       chat_use_cases.py (IniciarConversacion,
│                        ProcesarMensajeCliente, ObtenerHistorial)
├── infrastructure/
│   ├── motor/           motor_faq_simple.py (★ implementación actual),
│   │                    motor_ia_stub.py (cómo se integraría IA), texto.py
│   ├── repositories/    faq_repository_sql.py, conversacion_repository_sql.py
│   └── database/        models.py (+tablas chat), seed_faqs.py
├── adapters/
│   └── http/            chat_router.py (REST de apoyo)
└── realtime/            ★ todo lo de tiempo real
    ├── connection_manager.py    registro de conexiones WebSocket
    ├── websocket_notificador.py implementa el puerto de salida
    ├── chat_socket.py           endpoint WebSocket (driving adapter)
    ├── dependencias_chat.py     composición / inyección de dependencias
    └── static/chat.html         cliente de prueba
```

### Sistema de respuestas automáticas (decisiones de diseño)

- **Detección de coincidencias:** el `FaqRepositorySQL` recupera candidatas
  con `LIKE` (recuperación simple, como pide la práctica). El
  `MotorFaqSimple` puntúa cada candidata combinando el solapamiento de
  palabras (sin acentos ni *stopwords*) con las `palabras_clave` de la FAQ
  (que pesan más). El mejor puntaje se normaliza a una **confianza** [0,1].
- **Estructura de respuestas:** todo motor devuelve un `RespuestaAsistente`
  (contenido, confianza, manejada, faq_id, fuente).
- **Almacenamiento de FAQs:** tabla `faqs` con pregunta, respuesta, categoría
  y palabras clave.
- **Manejo de conversaciones:** entidad `Conversacion` con estados
  `abierta`, `escalada`, `cerrada`. Si la confianza no supera el umbral, la
  conversación se marca como **escalada** (preparado para atención humana).

### Por qué es escalable a IA (★ clave de la evaluación)

El caso de uso `ProcesarMensajeCliente` depende del **puerto**
`MotorRespuestas`, nunca de una implementación concreta. Para migrar a un
asistente de IA / embeddings / RAG / LLM, solo se cambia la función
`construir_motor()` en `app/realtime/dependencias_chat.py` para que devuelva
otra implementación del mismo puerto (ver `motor_ia_stub.py`). Ni el caso de
uso, ni el adaptador WebSocket, ni los repositorios cambian.
