from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Faccion(Base):
    __tablename__ = "facciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False, index=True)
    recurso_especial = Column(String, nullable=True)

    heroes = relationship("Heroe", back_populates="faccion", cascade="all, delete-orphan")

class Heroe(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    clase_heroe = Column(String, nullable=False)
    atributo_principal = Column(String, nullable=False)
    faccion_id = Column(Integer, ForeignKey("facciones.id", ondelete="CASCADE"), nullable=False)

    faccion = relationship("Faccion", back_populates="heroes")