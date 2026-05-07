from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.pedido import Pedido


def crear(
    db: Session,
    total_pagado: float,
    id_usuario: UUID,
    id_usuario_creacion: UUID,
) -> Pedido:

    pedido = Pedido(
        id_usuario=id_usuario,
        id_usuario_creacion=id_usuario_creacion,
        total_pagado=total_pagado,
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido


def obtener_por_id(
    db: Session,
    id_pedido: UUID,
) -> Optional[Pedido]:

    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()


def obtener_todos(
    db: Session,
) -> List[Pedido]:

    return db.query(Pedido).all()


def obtener_por_usuario(
    db: Session,
    id_usuario: UUID,
) -> List[Pedido]:

    return db.query(Pedido).filter(Pedido.id_usuario == id_usuario).all()


def actualizar(
    db: Session,
    id_pedido: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Pedido]:

    pedido = obtener_por_id(
        db,
        id_pedido,
    )

    if not pedido:
        return None

    for key, value in kwargs.items():
        if hasattr(pedido, key):
            setattr(pedido, key, value)

    pedido.id_usuario_edita = id_usuario_edita

    db.commit()
    db.refresh(pedido)

    return pedido


def eliminar(
    db: Session,
    id_pedido: UUID,
) -> bool:

    pedido = obtener_por_id(
        db,
        id_pedido,
    )

    if not pedido:
        return False

    db.delete(pedido)
    db.commit()

    return True
