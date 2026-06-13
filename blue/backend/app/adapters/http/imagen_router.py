import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.adapters.http.dependencies import require_admin

imagen_router = APIRouter()

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "uploads")
EXTENSIONES_PERMITIDAS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
TIPOS_PERMITIDOS = {"image/jpeg", "image/png", "image/webp", "image/gif"}
TAMANO_MAXIMO = 5 * 1024 * 1024  # 5 MB

@imagen_router.post("/productos/upload-imagen")
async def subir_imagen(archivo: UploadFile = File(...), usuario=Depends(require_admin)):
    # Validar extensión del archivo
    extension = os.path.splitext(archivo.filename)[1].lower()
    if extension not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(status_code=400, detail="Extensión de archivo no permitida")

    # Validar tipo MIME
    if archivo.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")

    # Validar tamaño del archivo
    if archivo.size > TAMANO_MAXIMO:
        raise HTTPException(status_code=400, detail="El archivo es demasiado grande")

    # Generar un nombre de archivo único
    nombre_archivo = f"{uuid.uuid4()}{extension}"
    ruta_guardado = os.path.join(UPLOADS_DIR, nombre_archivo)

    # Guardar el archivo en el sistema de archivos
    with open(ruta_guardado, "wb") as buffer:
        buffer.write(await archivo.read())

    # Retornar la URL de la imagen subida
    url_imagen = f"/uploads/{nombre_archivo}"
    return {"url": url_imagen}
