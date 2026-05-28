from fastapi import FastAPI
from app.infrastructure.database.base import engine
from app.infrastructure.database import models
from app.adapters.http.producto_router import producto_router
from app.adapters.http.perfil_compra_router import perfil_compra_router
from app.adapters.http.orden_compra_router import orden_compra_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PuzzleStore API",
    description="E-commerce de cubos Rubik, rompecabezas y puzzles — Arquitectura Hexagonal",
    version="1.0.0"
)

app.include_router(producto_router, tags=["Productos"])
app.include_router(perfil_compra_router, tags=["Perfiles de Compra"])
app.include_router(orden_compra_router, tags=["Órdenes de Compra"])

@app.get("/")
def root():
    return {"message": "Bienvenido a PuzzleStore API"}
