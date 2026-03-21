import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Pago(Base):
    """Modelo de pago"""

    __tablename__ = "pago"

    id_pago = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_pedido = Column(
        UUID(as_uuid=True), ForeignKey("pedido.id_pedido"), nullable=False
    )
    metodo_pago = Column(String(50), nullable=False)
    monto_pagado = Column(String(50), nullable=False)
    estado_pago = Column(String(50), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    pedido = relationship("Pedido", foreign_keys=[id_pedido])
