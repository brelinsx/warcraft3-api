# Campeón del reino: héroe invocado en el Altar.
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Heroe(Base):
    """Héroe grabado en la tabla heroes, atado a un único clan."""

    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    clase_heroe = Column(String, nullable=False)
    atributo_principal = Column(String, nullable=False)
    faccion_id = Column(
        Integer, ForeignKey("facciones.id", ondelete="CASCADE"), nullable=False
    )

    # Juramento de lealtad: todo héroe sirve a un único clan.
    faccion = relationship("Faccion", back_populates="heroes")
