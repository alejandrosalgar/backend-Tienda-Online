from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.crud import categoria as categoria_crud

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/")
def crear_categoria(
    nombre_categoria: str,
    id_usuario_creacion: UUID,
    descripcion: str = None,
    db: Session = Depends(get_db),
):
    return categoria_crud.crear(db, nombre_categoria, id_usuario_creacion, descripcion)


@router.get("/")
def listar_categorias(db: Session = Depends(get_db)):
    return categoria_crud.obtener_todos(db)


@router.get("/{id_categoria}")
def obtener_categoria(id_categoria: UUID, db: Session = Depends(get_db)):
    categoria = categoria_crud.obtener_por_id(db, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


@router.delete("/{id_categoria}")
def eliminar_categoria(id_categoria: UUID, db: Session = Depends(get_db)):
    eliminado = categoria_crud.eliminar(db, id_categoria)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return {"mensaje": "Categoria eliminada"}


@router.put("/{id_categoria}")
def actualizar_categoria(
    id_categoria: UUID,
    id_usuario_edita: UUID,
    nombre_categoria: str = None,
    descripcion: str = None,
    db: Session = Depends(get_db),
):
    categoria = categoria_crud.actualizar(
        db,
        id_categoria,
        id_usuario_edita,
        nombre_categoria=nombre_categoria,
        descripcion=descripcion,
    )

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria
