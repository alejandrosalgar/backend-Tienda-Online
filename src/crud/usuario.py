"""
CRUD para la entidad Usuario.
Incluye creación, login (verificación de contraseña) y operaciones básicas.
"""

import hashlib
from typing import List, Optional
from uuid import UUID


from sqlalchemy.orm import Session


from src.entities.usuario import Usuario


def _hash_contrasena(contrasena: str) -> str:
    """Hashea la contraseña con SHA-256 (para no guardar en claro)."""
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def crear(
    db: Session,
    nombre_usuario: str,
    email: str,
    contrasena: str,
    rol: str = "usuario",
    activo: bool = True,
) -> Usuario:
    """Crea un nuevo usuario."""

    usuario_existente = db.query(Usuario).filter(Usuario.email == email.strip()).first()

    if usuario_existente:
        raise ValueError("El email ya está registrado")

    usuario = Usuario(
        nombre_usuario=nombre_usuario.strip(),
        email=email.strip(),
        contrasena=_hash_contrasena(contrasena),
        rol=rol.strip(),
        activo=activo,
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login(db: Session, email: str, contrasena: str) -> Optional[Usuario]:
    """
    Verifica credenciales usando email + contraseña.
    """
    usuario = db.query(Usuario).filter(Usuario.email == email.strip()).first()

    if not usuario or not usuario.activo:
        return None

    if usuario.contrasena != _hash_contrasena(contrasena):
        return None

    return usuario


def obtener_por_id(db: Session, id_usuario: UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_nombre_usuario(db: Session, nombre_usuario: str) -> Optional[Usuario]:
    return (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )


def obtener_todos(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()


def hay_usuarios(db: Session) -> bool:
    """Indica si existe al menos un usuario."""
    return db.query(Usuario).first() is not None


def actualizar(
    db: Session,
    id_usuario: UUID,
    *,
    nombre_usuario: Optional[str] = None,
    email: Optional[str] = None,
    contrasena: Optional[str] = None,
    rol: Optional[str] = None,
    activo: Optional[bool] = None,
) -> Optional[Usuario]:

    usuario = obtener_por_id(db, id_usuario)

    if not usuario:
        return None

    if nombre_usuario is not None:
        usuario.nombre_usuario = nombre_usuario.strip()

    if email is not None:
        usuario.email = email.strip()

    if contrasena is not None:
        usuario.contrasena = _hash_contrasena(contrasena)

    if rol is not None:
        usuario.rol = rol.strip()

    if activo is not None:
        usuario.activo = activo

    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(db: Session, id_usuario: UUID) -> bool:
    usuario = obtener_por_id(db, id_usuario)

    if not usuario:
        return False

    db.delete(usuario)
    db.commit()
    return True
