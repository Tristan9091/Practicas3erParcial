import re
import unicodedata
from typing import List

STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del",
    "a", "al", "y", "o", "que", "en", "es", "mi", "me", "se", "su", "por",
    "para", "con", "como", "cual", "cuales", "cuanto", "donde", "cuando",
    "hay", "tengo", "tiene", "esta", "estan", "puedo", "quiero", "necesito",
}


def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^\w\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def tokenizar(texto: str) -> List[str]:
    return [
        palabra
        for palabra in normalizar(texto).split()
        if palabra and palabra not in STOPWORDS
    ]
