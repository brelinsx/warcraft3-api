# Estandarte de los clanes: Horda, Alianza, No-muertos o Elfos Nocturnos.
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Faccion(Base):
    """Clan del reino grabado en la tabla facciones."""

    __tablename__ = "facciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False, index=True)
    recurso_especial = Column(String, nullable=True)

    # Cada estandarte cobija a sus héroes; si el clan cae, caen con él.
    heroes = relationship(
        "Heroe", back_populates="faccion", cascade="all, delete-orphan"
    )
