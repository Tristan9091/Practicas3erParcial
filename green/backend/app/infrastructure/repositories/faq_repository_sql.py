from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.domain.entities.faq import FAQ
from app.domain.ports.faq_repository import FaqRepository
from app.infrastructure.database.models import FaqModel


class FaqRepositorySQL(FaqRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: FaqModel) -> FAQ:
        return FAQ(
            id=model.id,
            pregunta=model.pregunta,
            respuesta=model.respuesta,
            categoria=model.categoria,
            palabras_clave=model.palabras_clave or [],
        )

    def guardar(self, faq: FAQ) -> None:
        model = FaqModel(
            id=faq.id,
            pregunta=faq.pregunta,
            respuesta=faq.respuesta,
            categoria=faq.categoria,
            palabras_clave=faq.palabras_clave,
        )
        self.db.add(model)
        self.db.commit()

    def listar_todas(self) -> List[FAQ]:
        return [self._to_entity(m) for m in self.db.query(FaqModel).all()]

    def buscar_candidatas(self, texto: str) -> List[FAQ]:

        tokens = [t for t in texto.lower().split() if len(t) > 3]
        if not tokens:
            return self.listar_todas()

        condiciones = [FaqModel.pregunta.ilike(f"%{t}%") for t in tokens]
        modelos = self.db.query(FaqModel).filter(or_(*condiciones)).all()

        if not modelos:
            return self.listar_todas()
        return [self._to_entity(m) for m in modelos]
