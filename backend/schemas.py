# Pergaminos del escriba: validan a quien cruza las puertas del reino.
from pydantic import BaseModel, Field


# --- Estandartes de los clanes ---
class FaccionBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    recurso_especial: str | None = Field(default=None, max_length=100)


class FaccionCreate(FaccionBase):
    pass


class FaccionRead(FaccionBase):
    id: int

    class Config:
        from_attributes = True


# --- Campeones del Altar ---
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


# --- Crónicas con linaje: lecturas que traen a la familia entera ---
class HeroesInFaccion(BaseModel):
    id: int
    nombre: str
    clase_heroe: str
    atributo_principal: str

    class Config:
        from_attributes = True


class FaccionWithHeroes(FaccionRead):
    heroes: list[HeroesInFaccion] = []


class FaccionSimple(BaseModel):
    id: int
    nombre: str
    recurso_especial: str | None = None

    class Config:
        from_attributes = True


class HeroeWithFaccion(HeroeRead):
    faccion: FaccionSimple | None = None
