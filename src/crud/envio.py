from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.envio import Envio


db = SessionLocal()


def crear(
    id_pedido: UUID,
    direccion_envio: str,
    estado_envio: str,
    id_usuario_creacion: UUID,
    transportista: Optional[str] = None,
) -> Envio:
    envio = Envio(
        id_pedido=id_pedido,
        direccion_envio=direccion_envio,
        estado_envio=estado_envio,
        transportista=transportista,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(envio)
    db.commit()
    db.refresh(envio)
    return envio


def obtener_por_id(id_envio: UUID) -> Optional[Envio]:
    return db.query(Envio).filter(Envio.id_envio == id_envio).first()


def obtener_todos() -> List[Envio]:
    return db.query(Envio).all()


def actualizar(
    id_envio: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Envio]:
    envio = obtener_por_id(id_envio)
    if not envio:
        return None
    for key, value in kwargs.items():
        if hasattr(envio, key):
            setattr(envio, key, value)
    envio.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(envio)
    return envio


def eliminar(id_envio: UUID) -> bool:
    envio = obtener_por_id(id_envio)
    if not envio:
        return False
    db.delete(envio)
    db.commit()
    return True
