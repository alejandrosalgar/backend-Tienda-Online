from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.categoria import Categoria


def crear(
    nombre_categoria: str, id_usuario_creacion: UUID, descripcion: Optional[str] = None
) -> Categoria:
    db = SessionLocal()
    try:
        categoria_existente = (
            db.query(Categoria)
            .filter(Categoria.nombre_categoria == nombre_categoria.strip())
            .first()
        )
        if categoria_existente:
            raise ValueError("La categoría ya existe")

        categoria = Categoria(
            nombre_categoria=nombre_categoria.strip(),
            descripcion=(descripcion.strip() if descripcion else None),
            id_usuario_creacion=id_usuario_creacion,
        )

        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria
    finally:
        db.close()


def obtener_por_id(id_categoria: UUID) -> Optional[Categoria]:
    db = SessionLocal()
    try:
        return (
            db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
        )
    finally:
        db.close()


def obtener_todos() -> List[Categoria]:
    db = SessionLocal()
    try:
        return db.query(Categoria).all()
    finally:
        db.close()


def actualizar(
    id_categoria: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Categoria]:
    db = SessionLocal()
    try:
        categoria = (
            db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
        )
        if not categoria:
            return None

        for key, value in kwargs.items():
            setattr(categoria, key, value)

        categoria.id_usuario_edita = id_usuario_edita
        db.commit()
        db.refresh(categoria)

        return categoria
    finally:
        db.close()


def eliminar(id_categoria: UUID) -> bool:
    db = SessionLocal()
    try:
        categoria = (
            db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
        )
        if not categoria:
            return False

        db.delete(categoria)
        db.commit()
        return True
    finally:
        db.close()
