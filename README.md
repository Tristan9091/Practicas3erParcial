# PuzzleStore — E-commerce

**Programación Web 1 · Prof. Kegovc**

Tienda en línea de cubos, rompecabezas y puzzles. El proyecto integra las cuatro prácticas del curso en un solo sistema fullstack: un backend en FastAPI con Arquitectura Hexagonal (P1), autenticación y autorización con JWT (P2), un chat cliente–asistente en tiempo real con WebSockets y atención humana en viv(P3) y el frontend completo del e-commerce con su panel administrativo (P4).

---

## Estructura del proyecto

```
project/
├── backend/                    # API en FastAPI (Arquitectura Hexagonal)
│   ├── app/
│   │   ├── domain/             # Entidades y puertos (contratos)
│   │   ├── application/        # Casos de uso (lógica de negocio)
│   │   ├── infrastructure/     # Repositorios SQLAlchemy, BD y motor de FAQ
│   │   ├── adapters/http/      # Routers (productos, auth, órdenes, perfiles, imágenes, chat)
│   │   ├── realtime/           # WebSockets del chat y gestor de conexiones
│   │   ├── security/           # Generación y validación de JWT
│   │   └── main.py             # Punto de entrada (CORS, estáticos, routers)
│   └── uploads/                # Imágenes de productos (se llena al subir)
├── frontend/                   # Cliente en HTML + CSS + JS (Bootstrap por CDN)
│   ├── login.html              # Login / registro
│   ├── index.html              # Catálogo + carrito + chat
│   ├── checkout.html           # Resumen, compra, historial + chat
│   ├── admin.html              # Backoffice (productos, órdenes, usuarios, chat de agente)
│   ├── css/styles.css
│   └── js/
│       ├── auth.js             # Sesión y token JWT
│       ├── api.js              # Llamadas al backend
│       ├── login.js            # Login / registro
│       ├── index.js            # Catálogo y carrito
│       ├── checkout.js         # Checkout e historial
│       ├── chat.js             # WebSocket del chat (compartido)
│       └── admin.js            # Backoffice
├── requirements.txt
└── README.md
```

---

## Requisitos y ejecución

**Requisitos:** Python 3.10+, MySQL en ejecución y conexión a internet (Bootstrap
se carga por CDN).

**1. Base de datos.** Crear la base en MySQL:

```sql
CREATE DATABASE puzzlestore;
```

La cadena de conexión está en `backend/app/infrastructure/database/base.py`. Ajustarla
si el usuario/contraseña de MySQL son distintos:

```
mysql+pymysql://root:root1234@127.0.0.1:3306/puzzlestore
```

**2. Backend.** Instalar dependencias y levantar el servidor desde la carpeta `backend/`:

```bash
pip install -r ../requirements.txt
cd backend
python3 -m uvicorn app.main:app --reload
```

Queda en `http://127.0.0.1:8000`. Las tablas se crean solas al arrancar y, si la tabla
de FAQs está vacía, se cargan unas preguntas frecuentes de ejemplo. La documentación
interactiva está en `http://127.0.0.1:8000/docs`.

**3. Frontend.** Servirlo con un servidor estático desde la carpeta `frontend/`:

```bash
cd frontend
python3 -m http.server 5500
```

Abrir `http://127.0.0.1:5500/login.html`. Importante: el frontend debe abrirse a través
del servidor (no con doble clic en el archivo), o el navegador bloquea las peticiones y
los WebSockets.

---

## Roles y primer acceso

El sistema maneja tres roles: **cliente**, **operador** y **admin**.

- Al registrarse, el usuario **no elige rol**: nace siempre como `cliente`. La única excepción es el correo `admin@gmail.com`, que nace como `admin`. Esto evita que cualquiera se registre con permisos de administrador.
- El administrador, desde la pestaña **Usuarios** del backoffice, puede promover a otras cuentas a `operador` o `admin`.
- Como el rol viaja dentro del token JWT, los cambios de rol aplican la **próxima vez que el usuario inicia sesión**.

Permisos por rol:

- **cliente:** catálogo, carrito, compra, historial y chat.
- **operador:** entra al backoffice; puede editar productos, gestionar órdenes y atenderel chat escalado. No puede crear/eliminar productos ni gestionar usuarios.
- **admin:** acceso total al backoffice, incluida la gestión de usuarios.

---

## Práctica 1 — E-commerce Hexagonal

**Objetivo:** un backend de e-commerce desacoplado y organizado siguiendo Arquitectura
Hexagonal.

El backend separa responsabilidades en capas: **dominio** (entidades como `Producto`,`PerfilCompra`, `OrdenCompra`, y los puertos/interfaces)**aplicación** (casos de uso con la lógica de negocio), **infraestructura** (repositorios SQLAlchemy/MySQL que cumplen los puertos) y **adaptadores** (routers de FastAPI). Las tres entidades mínimas están presentes y el flujo de una orden es: producto en catálogo → perfil de compra → orden que referencia el perfil, lista sus items y calcula el total → estado que evoluciona
(`pendiente`, `pagada`, `enviada`, `entregada`, `cancelada`).

---

## Práctica 2 — Autenticación y Autorización (JWT)

**Objetivo:** proteger el backend con login, validación y control de acceso por roles.
Se eligió la **Opción 2 (OAuth 2 / JWT, hasta 100%)**.

- **Registro** (`POST /auth/register`): crea el usuario con la contraseña cifrada con
  bcrypt. El rol lo decide el backend (no el usuario).
- **Login** (`POST /auth/login`): usa `OAuth2PasswordRequestForm`; devuelve un **access
  token** y un **refresh token** (JWT con python-jose) que llevan el correo y el rol.
- **Refresh** (`POST /auth/refresh`): renueva el access token sin pedir credenciales.
- **Protección de rutas** (`dependencies.py`): dependencias reutilizables que FastAPI
  inyecta: `get_current_user`, `require_admin` y `require_operador_o_admin`.
- **Gestión de usuarios** (solo admin): `GET /auth/usuarios` y
  `PATCH /auth/usuarios/{email}/rol` para listar y cambiar roles.

El catálogo es público, pero crear/editar/eliminar productos, gestionar órdenes, subir
imágenes y administrar usuarios exigen el rol adecuado. El frontend manda el token en el
header `Authorization: Bearer ...` y redirige según el rol.

---

## Práctica 3 — Chat en tiempo real con WebSockets y atención humana

**Objetivo:** comunicación en tiempo real con respuestas automáticas a preguntas
frecuentes, escalable a IA, con la posibilidad de que un humano intervenga.

**Flujo completo:**

1. El cliente abre el chat: se crea una conversación (`POST /chat/conversaciones`) y se
   conecta por WebSocket a `/ws/chat/{conversacion_id}`.
2. Cada mensaje pasa por el **motor de respuestas** (`MotorFaqSimple`), que normaliza el
   texto y puntúa las FAQs por coincidencia de palabras clave.
3. Si encuentra una FAQ con confianza suficiente, el **bot responde automáticamente**.
4. Si no, el bot avisa al cliente que lo contactará un agente y la conversación se marca
   como **escalada**; ese aviso se difunde a los agentes conectados al canal `/ws/staff`.
5. Un **admin u operador** ve el mensaje en el panel y responde en vivo; su respuesta
   llega al cliente etiquetada como **agente**.

**Diseño desacoplado y escalable.** El motor se usa a través del puerto
`MotorRespuestas`. La implementación actual es por palabras clave, pero podría
reemplazarse por **embeddings, RAG o un LLM** sin tocar el WebSocket ni los casos de uso,
porque todos dependen del puerto y no de la implementación concreta.

---

## Práctica 4 — Frontend E-commerce y Backoffice Administrativo

**Objetivo:** el frontend completo integrando las tres prácticas anteriores.

Hecho en HTML, CSS y JavaScript con Bootstrap por CDN, con la lógica separada por
responsabilidades: `auth.js` (sesión/token), `api.js` (consumo de la API) y un archivo por
página. El carrito se mantiene en `localStorage` para sobrevivir el cambio entre el
catálogo y el checkout.

- **Cliente:** catálogo con búsqueda, carrito con control de stock, checkout con flujo
  completo de compra, historial de órdenes (con cancelación) y la sección de chat.
- **Administrador / operador (Backoffice):** gestión de productos, gestión de órdenes con
  cambio de estado, gestión de usuarios (solo admin) y panel de chat para atender las
  conversaciones escaladas.

**Manejo de imágenes (`multipart/form-data`).** El endpoint `POST /productos/upload-imagen`
recibe el archivo como `multipart/form-data`, lo valida (extensión, tipo MIME y tamaño
máximo de 5 MB), lo guarda físicamente en `backend/uploads/` con un nombre único y devuelve
su URL. Esa URL se persiste en el producto y se sirve como archivo estático en `/uploads`.
En el formulario del admin, la imagen se sube primero y luego se guarda el producto con la
URL resultante.

**Ajustes al backend para esta práctica:** se habilitó **CORS**, se montó la carpeta de
imágenes estáticas, se agregó la subida de imágenes, los endpoints de backoffice para
órdenes (`GET /ordenes` y `PATCH /ordenes/{id}/estado`), la gestión de usuarios por rol y
el canal de chat para agentes (`/ws/staff`), todo respetando la Arquitectura Hexagonal
(puerto → repositorio → caso de uso → router).

---

## Notas finales

- Los WebSockets del chat no van autenticados (consistente con el diseño de la P3); es una mejora futura posible.
- Bootstrap se carga por CDN, por lo que se requiere internet al ejecutar el frontend.
- La relación entre el usuario autenticado y su perfil de compra se mantiene desde el frontend (se crea el perfil en la primera compra y se reutiliza su id), ya que el backend las maneja como entidades independientes.
- Las FAQs de fábrica solo se siembran cuando la tabla está vacía; para cambiarlas hay que vaciar la tabla `faqs` y reiniciar el backend.
