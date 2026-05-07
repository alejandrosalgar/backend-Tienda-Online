from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from src.database.config import get_db
from src.crud import usuario as crud_usuario

router = APIRouter(tags=["Usuarios"])


# =========================
# MODELOS PYDANTIC
# =========================


class UsuarioCreate(BaseModel):
    nombre_usuario: str
    email: str
    contrasena: str
    rol: Optional[str] = "usuario"
    activo: Optional[bool] = True


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    email: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class LoginRequest(BaseModel):
    email: str
    contrasena: str


# =========================
# SERIALIZADOR
# =========================


def usuario_response(usuario):
    return {
        "id_usuario": str(usuario.id_usuario),
        "nombre_completo": usuario.nombre_usuario,
        "nombre_usuario": usuario.nombre_usuario,
        "email": usuario.email,
        "rol": usuario.rol,
        "activo": usuario.activo,
    }


# =========================
# ENDPOINTS
# =========================


@router.post("/")
def crear_usuario(
    body: UsuarioCreate,
    db: Session = Depends(get_db),
):
    usuario = crud_usuario.crear(
        db,
        body.nombre_usuario,
        body.email,
        body.contrasena,
        body.rol,
        body.activo,
    )

    return usuario_response(usuario)


@router.get("/")
def obtener_usuarios(
    db: Session = Depends(get_db),
):
    usuarios = crud_usuario.obtener_todos(db)

    return [usuario_response(u) for u in usuarios]


@router.get("/{id_usuario}")
def obtener_usuario(
    id_usuario: UUID,
    db: Session = Depends(get_db),
):
    usuario = crud_usuario.obtener_por_id(db, id_usuario)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario_response(usuario)


@router.put("/{id_usuario}")
def actualizar_usuario(
    id_usuario: UUID,
    body: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    usuario = crud_usuario.actualizar(
        db,
        id_usuario,
        nombre_usuario=body.nombre_usuario,
        email=body.email,
        contrasena=body.contrasena,
        rol=body.rol,
        activo=body.activo,
    )

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario_response(usuario)


@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: UUID,
    db: Session = Depends(get_db),
):
    eliminado = crud_usuario.eliminar(db, id_usuario)

    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"mensaje": "Usuario eliminado"}


@router.post("/login")
def login(
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    usuario = crud_usuario.login(
        db,
        body.email,
        body.contrasena,
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
        )

    return {
        "ok": True,
        "usuario": usuario_response(usuario),
    }
