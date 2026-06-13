from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database.base import engine, SessionLocal
from app.infrastructure.database import models
from app.infrastructure.database.seed_faqs import sembrar_faqs
from app.adapters.http.producto_router import producto_router
from app.adapters.http.perfil_compra_router import perfil_compra_router
from app.adapters.http.orden_compra_router import orden_compra_router
from app.adapters.http.auth_router import router as auth_router
from app.adapters.http.chat_router import chat_router
from app.realtime.chat_socket import chat_socket_router
from app.adapters.http.imagen_router import imagen_router


UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

_db = SessionLocal()
try:
    sembrar_faqs(_db)
finally:
    _db.close()

app = FastAPI(
    title="PuzzleStore API",
    description="E-commerce de cubos Rubik, rompecabezas y puzzles",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.include_router(producto_router, tags=["Productos"])
app.include_router(perfil_compra_router, tags=["Perfiles de Compra"])
app.include_router(orden_compra_router, tags=["Órdenes de Compra"])
app.include_router(auth_router)
app.include_router(chat_router, tags=["Chat"])
app.include_router(chat_socket_router, tags=["Chat WebSocket"])
app.include_router(imagen_router, tags=["Imágenes"])

_static_dir = os.path.join(os.path.dirname(__file__), "realtime", "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/")
def root():
    return {"message": "Bienvenido a PuzzleStore API"}


@app.get("/chat-demo")
def chat_demo():
    """Pagina de prueba del chat en tiempo real."""
    return FileResponse(os.path.join(_static_dir, "chat.html"))
