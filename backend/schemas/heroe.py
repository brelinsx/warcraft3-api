# Pergaminos del escriba para los campeones del Altar.
from pydantic import BaseModel, Field


class HeroeBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    clase_heroe: str = Field(min_length=2, max_length=50)
    atributo_principal: str = Field(pattern="^(Fuerza|Agilidad|Inteligencia)$")
    faccion_id: int


class HeroeCreate(HeroeBase):
    pass


class HeroeRead(HeroeBase):
    id: int

    class Config:
        from_attributes = True


class HeroesInFaccion(BaseModel):
    id: int
    nombre: str
    clase_heroe: str
    atributo_principal: str

    class Config:
        from_attributes = True
