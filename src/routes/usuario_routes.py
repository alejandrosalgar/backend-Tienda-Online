from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.database.config import get_db
from src.crud import usuario as usuario_crud

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/")
def crear_usuario(
    nombre_usuario: str,
    email: str,
    contrasena: str,
    db: Session = Depends(get_db),
):
    try:
        return usuario_crud.crear(db, nombre_usuario, email, contrasena)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_crud.obtener_todos(db)


@router.get("/{id_usuario}")
def obtener_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    usuario = usuario_crud.obtener_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    eliminado = usuario_crud.eliminar(db, id_usuario)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}


@router.put("/{id_usuario}")
def actualizar_usuario(
    id_usuario: UUID,
    nombre_usuario: str = None,
    email: str = None,
    contrasena: str = None,
    rol: str = None,
    activo: bool = None,
    db: Session = Depends(get_db),
):
    usuario = usuario_crud.actualizar(
        db,
        id_usuario,
        nombre_usuario=nombre_usuario,
        email=email,
        contrasena=contrasena,
        rol=rol,
        activo=activo,
    )

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario
