from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.crud import producto as producto_crud

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/")
def crear_producto(
    nombre_producto: str,
    id_categoria: UUID,
    id_usuario_creacion: UUID,
    precio: float,
    stock: int,
    db: Session = Depends(get_db),
):
    return producto_crud.crear(
        db, nombre_producto, id_categoria, id_usuario_creacion, precio, stock
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


@router.delete("/{id_producto}")
def eliminar_producto(id_producto: UUID, db: Session = Depends(get_db)):
    eliminado = producto_crud.eliminar(db, id_producto)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}


@router.put("/{id_producto}")
def actualizar_producto(
    id_producto: UUID,
    id_usuario_edita: UUID,
    nombre_producto: str = None,
    descripcion_producto: str = None,
    precio: float = None,
    stock: int = None,
    db: Session = Depends(get_db),
):
    producto = producto_crud.actualizar(
        db,
        id_producto,
        id_usuario_edita,
        nombre_producto=nombre_producto,
        descripcion_producto=descripcion_producto,
        precio=precio,
        stock=stock,
    )

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto
