import uuid

from sqlalchemy.orm import Session

from app.domain.entities.faq import FAQ
from app.infrastructure.repositories.faq_repository_sql import FaqRepositorySQL

FAQS_INICIALES = [
    FAQ(
        id=str(uuid.uuid4()),
        pregunta="Como consulto el estado de mi orden",
        respuesta=(
            "Puedes ver el estado de tu orden en 'Mis pedidos' dentro de tu "
            "cuenta, o consultando el endpoint /ordenes/{id} con tu numero de "
            "orden. Los estados posibles son: pendiente, enviado y entregado."
        ),
        categoria="ordenes",
        palabras_clave=["orden", "pedido", "estado", "rastreo", "seguimiento"],
    ),
    FAQ(
        id=str(uuid.uuid4()),
        pregunta="Cuales son los metodos de pago disponibles",
        respuesta=(
            "Aceptamos tarjetas de credito y debito, transferencia bancaria y "
            "pago contra entrega en zonas seleccionadas."
        ),
        categoria="pagos",
        palabras_clave=["pago", "pagar", "tarjeta", "transferencia", "metodos"],
    ),
    FAQ(
        id=str(uuid.uuid4()),
        pregunta="Cuanto tardan los tiempos de envio",
        respuesta=(
            "Los envios nacionales tardan de 3 a 5 dias habiles. Los envios "
            "express llegan en 24 a 48 horas en ciudades principales."
        ),
        categoria="envios",
        palabras_clave=["envio", "enviar", "entrega", "tiempo", "tardan", "dias"],
    ),
    FAQ(
        id=str(uuid.uuid4()),
        pregunta="Cuales son los horarios de atencion",
        respuesta=(
            "Nuestro horario de atencion es de lunes a viernes de 9:00 a 18:00 "
            "y sabados de 10:00 a 14:00."
        ),
        categoria="horarios",
        palabras_clave=["horario", "atencion", "abierto", "atienden", "hora"],
    ),
    FAQ(
        id=str(uuid.uuid4()),
        pregunta="Como puedo devolver un producto",
        respuesta=(
            "Tienes 30 dias para devolver un producto en su empaque original. "
            "Inicia la devolucion desde 'Mis pedidos' y te enviaremos la guia."
        ),
        categoria="devoluciones",
        palabras_clave=["devolver", "devolucion", "cambio", "reembolso"],
    ),
    FAQ(
        id=str(uuid.uuid4()),
        pregunta="Ex de verdad",
        respuesta=(
            "Eres el peor amor que eh conocido tan perfecto que no te olvido piensa en mi ayudame "
            "a odiarte has las cosas que hacen los cobardes no me trates bien ni sonrias mas pues "
            "mi alma sigue sufriendo se un ex de verdad y tratame mal, ayudame con eso"
        ),
        categoria="devoluciones",
        palabras_clave=["Ex", "verdad", "Ex de verdad", "ex", "Verdad"],
    )
]


def sembrar_faqs(db: Session) -> int:
    """Inserta las FAQs iniciales solo si la tabla esta vacia.

    Devuelve cuantas FAQs se insertaron (0 si ya existian).
    """
    repo = FaqRepositorySQL(db)
    if repo.listar_todas():
        return 0
    for faq in FAQS_INICIALES:
        repo.guardar(faq)
    return len(FAQS_INICIALES)
