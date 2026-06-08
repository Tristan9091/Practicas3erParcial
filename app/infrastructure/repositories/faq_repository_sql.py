from sqlalchemy.orm import Session
from typing import List
from app.domain.ports.faq_repository import FaqRepository
from app.domain.entities.pregunta_frecuente import PreguntaFrecuente
from app.infrastructure.database.models import FaqModel


class FaqRepositorySQL(FaqRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_entity(self, model: FaqModel) -> PreguntaFrecuente:
        return PreguntaFrecuente(
            id=model.id,
            pregunta=model.pregunta,
            respuesta=model.respuesta,
            palabras_clave=model.palabras_clave or [],
        )

    def listar_todas(self) -> List[PreguntaFrecuente]:
        return [self._to_entity(m) for m in self.db.query(FaqModel).all()]

    def buscar(self, texto: str) -> List[PreguntaFrecuente]:
        return [
            self._to_entity(m)
            for m in self.db.query(FaqModel).filter(
                FaqModel.pregunta.ilike(f"%{texto}%")
            ).all()
        ]

    def guardar(self, faq: PreguntaFrecuente):
        model = FaqModel(
            id=faq.id,
            pregunta=faq.pregunta,
            respuesta=faq.respuesta,
            palabras_clave=faq.palabras_clave,
        )
        self.db.add(model)
        self.db.commit()