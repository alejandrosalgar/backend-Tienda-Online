from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from src.database.config import get_db
from src.crud import pedido as pedido_crud

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


# =========================
# MODELOS PYDANTIC
# =========================


class PedidoCreate(BaseModel):
    id_usuario: UUID
    total_pagado: float
    id_usuario_creacion: UUID


class PedidoUpdate(BaseModel):
    id_usuario_edita: UUID
    id_usuario: Optional[UUID] = None
    total_pagado: Optional[float] = None


# =========================
# SERIALIZADOR
# =========================


def pedido_response(pedido):
    return {
        "id_pedido": str(pedido.id_pedido),
        "id_usuario": str(pedido.id_usuario),
        "total_pagado": pedido.total_pagado,
        "fecha_creacion": pedido.fecha_creacion,
        "fecha_edicion": pedido.fecha_edicion,
        "id_usuario_creacion": str(pedido.id_usuario_creacion),
        "id_usuario_edita": (
            str(pedido.id_usuario_edita) if pedido.id_usuario_edita else None
        ),
    }


# =========================
# ENDPOINTS
# =========================


@router.post("/")
def crear_pedido(
    body: PedidoCreate,
    db: Session = Depends(get_db),
):

    pedido = pedido_crud.crear(
        db,
        body.total_pagado,
        body.id_usuario,
        body.id_usuario_creacion,
    )

    return pedido_response(pedido)


@router.get("/")
def listar_pedidos(
    db: Session = Depends(get_db),
):

    pedidos = pedido_crud.obtener_todos(db)

    return [pedido_response(p) for p in pedidos]


@router.get("/{id_pedido}")
def obtener_pedido(
    id_pedido: UUID,
    db: Session = Depends(get_db),
):

    pedido = pedido_crud.obtener_por_id(
        db,
        id_pedido,
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado",
        )

    return pedido_response(pedido)


@router.put("/{id_pedido}")
def actualizar_pedido(
    id_pedido: UUID,
    body: PedidoUpdate,
    db: Session = Depends(get_db),
):

    pedido = pedido_crud.actualizar(
        db,
        id_pedido,
        body.id_usuario_edita,
        id_usuario=body.id_usuario,
        total_pagado=body.total_pagado,
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado",
        )

    return pedido_response(pedido)


@router.delete("/{id_pedido}")
def eliminar_pedido(
    id_pedido: UUID,
    db: Session = Depends(get_db),
):

    eliminado = pedido_crud.eliminar(
        db,
        id_pedido,
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado",
        )

    return {"mensaje": "Pedido eliminado"}
