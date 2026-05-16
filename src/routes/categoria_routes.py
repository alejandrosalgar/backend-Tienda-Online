from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from src.database.config import get_db
from src.crud import categoria as categoria_crud

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
)


# =========================
# MODELOS PYDANTIC
# =========================


class CategoriaCreate(BaseModel):
    nombre_categoria: str
    id_usuario_creacion: UUID
    descripcion: Optional[str] = None


class CategoriaUpdate(BaseModel):
    id_usuario_edita: UUID
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None


# =========================
# SERIALIZADOR
# =========================


def categoria_response(categoria):
    return {
        "id_categoria": str(categoria.id_categoria),
        "nombre_categoria": categoria.nombre_categoria,
        "descripcion": categoria.descripcion,
        "estado": True,
        "fecha_creacion": categoria.fecha_creacion,
        "fecha_edicion": categoria.fecha_edicion,
        "id_usuario_creacion": str(categoria.id_usuario_creacion),
        "id_usuario_edita": (
            str(categoria.id_usuario_edita) if categoria.id_usuario_edita else None
        ),
    }


# =========================
# ENDPOINTS
# =========================


@router.post("/")
def crear_categoria(
    body: CategoriaCreate,
    db: Session = Depends(get_db),
):
    categoria = categoria_crud.crear(
        db,
        body.nombre_categoria,
        body.id_usuario_creacion,
        body.descripcion,
    )

    return categoria_response(categoria)


@router.get("/")
def listar_categorias(
    db: Session = Depends(get_db),
):
    categorias = categoria_crud.obtener_todos(db)

    return [categoria_response(c) for c in categorias]


@router.get("/{id_categoria}")
def obtener_categoria(
    id_categoria: UUID,
    db: Session = Depends(get_db),
):
    categoria = categoria_crud.obtener_por_id(
        db,
        id_categoria,
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada",
        )

    return categoria_response(categoria)


@router.delete("/{id_categoria}")
def eliminar_categoria(
    id_categoria: UUID,
    db: Session = Depends(get_db),
):
    eliminado = categoria_crud.eliminar(
        db,
        id_categoria,
    )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada",
        )

    return {"mensaje": "Categoria eliminada"}


@router.put("/{id_categoria}")
def actualizar_categoria(
    id_categoria: UUID,
    body: CategoriaUpdate,
    db: Session = Depends(get_db),
):
    categoria = categoria_crud.actualizar(
        db,
        id_categoria,
        body.id_usuario_edita,
        nombre_categoria=body.nombre_categoria,
        descripcion=body.descripcion,
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada",
        )

    return categoria_response(categoria)
