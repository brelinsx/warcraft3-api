# Pergaminos del escriba: validan a quien cruza las puertas del reino.
from backend.schemas.faccion import (
    FaccionBase,
    FaccionCreate,
    FaccionRead,
    FaccionSimple,
)
from backend.schemas.heroe import (
    HeroeBase,
    HeroeCreate,
    HeroeRead,
    HeroesInFaccion,
)
from backend.schemas.relaciones import FaccionWithHeroes, HeroeWithFaccion

__all__ = [
    "FaccionBase",
    "FaccionCreate",
    "FaccionRead",
    "FaccionSimple",
    "FaccionWithHeroes",
    "HeroeBase",
    "HeroeCreate",
    "HeroeRead",
    "HeroesInFaccion",
    "HeroeWithFaccion",
]
