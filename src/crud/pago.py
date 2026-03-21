from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.pago import Pago


db = SessionLocal()


def crear(
    id_pedido: UUID,
    metodo_pago: str,
    monto_pagado: str,
    estado_pago: str,
    id_usuario_creacion: UUID,
) -> Pago:
    pago = Pago(
        id_pedido=id_pedido,
        metodo_pago=metodo_pago,
        monto_pagado=monto_pagado,
        estado_pago=estado_pago,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return pago


def obtener_por_id(id_pago: UUID) -> Optional[Pago]:
    return db.query(Pago).filter(Pago.id_pago == id_pago).first()


def obtener_todos() -> List[Pago]:
    return db.query(Pago).all()


def actualizar(
    id_pago: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Pago]:
    pago = obtener_por_id(id_pago)
    if not pago:
        return None
    for key, value in kwargs.items():
        if hasattr(pago, key):
            setattr(pago, key, value)
    pago.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(pago)
    return pago


def eliminar(id_pago: UUID) -> bool:
    pago = obtener_por_id(id_pago)
    if not pago:
        return False
    db.delete(pago)
    db.commit()
    return True
