from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from src.database.config import get_db
from src.crud import producto as producto_crud

router = APIRouter(tags=["Productos"])


# =========================
# MODELOS PYDANTIC
# =========================


class ProductoCreate(BaseModel):
    nombre_producto: str
    id_categoria: UUID
    id_usuario_creacion: UUID
    precio: float
    stock: int
    descripcion_producto: Optional[str] = None


class ProductoUpdate(BaseModel):
    id_usuario_edita: UUID
    nombre_producto: Optional[str] = None
    descripcion_producto: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None


# =========================
# ENDPOINTS
# =========================


@router.post("/")
def crear_producto(
    body: ProductoCreate,
    db: Session = Depends(get_db),
):
    return producto_crud.crear(
        db,
        body.nombre_producto,
        body.id_categoria,
        body.id_usuario_creacion,
        body.precio,
        body.stock,
        body.descripcion_producto,
    )


@router.get("/")
def listar_productos(db: Session = Depends(get_db)):
    return producto_crud.obtener_todos(db)


@router.get("/{id_producto}")
def obtener_producto(id_producto: UUID, db: Session = Depends(get_db)):
    producto = producto_crud.obtener_por_id(db, id_producto)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto


@router.put("/{id_producto}")
def actualizar_producto(
    id_producto: UUID,
    body: ProductoUpdate,
    db: Session = Depends(get_db),
):
    producto = producto_crud.actualizar(
        db,
        id_producto,
        body.id_usuario_edita,
        nombre_producto=body.nombre_producto,
        descripcion_producto=body.descripcion_producto,
        precio=body.precio,
        stock=body.stock,
    )

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto


@router.delete("/{id_producto}")
def eliminar_producto(id_producto: UUID, db: Session = Depends(get_db)):
    eliminado = producto_crud.eliminar(db, id_producto)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"mensaje": "Producto eliminado"}
