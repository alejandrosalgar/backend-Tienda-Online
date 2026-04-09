from typing import List, Optional
from uuid import UUID


from sqlalchemy.orm import Session


from src.entities.producto import Producto


def crear(
    db: Session,
    nombre_producto: str,
    id_categoria: UUID,
    id_usuario_creacion: UUID,
    precio: float,
    stock: int,
    descripcion_producto: Optional[str] = None,
) -> Producto:
    producto = Producto(
        nombre_producto=nombre_producto.strip(),
        id_categoria=id_categoria,
        id_usuario_creacion=id_usuario_creacion,
        precio=precio,
        stock=stock,
        descripcion_producto=(
            descripcion_producto.strip() if descripcion_producto else None
        ),
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def obtener_por_id(db: Session, id_producto: UUID) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id_producto == id_producto).first()


def obtener_todos(db: Session) -> List[Producto]:
    return db.query(Producto).all()


def obtener_por_categoria(db: Session, id_categoria: UUID) -> List[Producto]:
    return db.query(Producto).filter(Producto.id_categoria == id_categoria).all()


def actualizar(
    db: Session,
    id_producto: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Producto]:
    producto = obtener_por_id(db, id_producto)
    if not producto:
        return None

    for key, value in kwargs.items():
        if hasattr(producto, key):
            setattr(producto, key, value)

    producto.id_usuario_edita = id_usuario_edita

    db.commit()
    db.refresh(producto)
    return producto


def eliminar(db: Session, id_producto: UUID) -> bool:
    producto = obtener_por_id(db, id_producto)
    if not producto:
        return False

    db.delete(producto)
    db.commit()
    return True
