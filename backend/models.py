# Tablillas del destino: los dos clanes del reino y su pacto de sangre (1:N).
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Faccion(Base):
    """Clan del reino: Horda, Alianza, No-muertos o Elfos Nocturnos."""

    __tablename__ = "facciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False, index=True)
    recurso_especial = Column(String, nullable=True)

    # Cada estandarte cobija a sus héroes; si el clan cae, caen con él.
    heroes = relationship(
        "Heroe", back_populates="faccion", cascade="all, delete-orphan"
    )


class Heroe(Base):
    """Campeón invocado en el Altar de los Héroes."""

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
