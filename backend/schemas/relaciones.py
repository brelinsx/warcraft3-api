# Crónicas con linaje: lecturas que traen a la familia entera.
from backend.schemas.faccion import FaccionRead, FaccionSimple
from backend.schemas.heroe import HeroeRead, HeroesInFaccion


class FaccionWithHeroes(FaccionRead):
    heroes: list[HeroesInFaccion] = []


class HeroeWithFaccion(HeroeRead):
    faccion: FaccionSimple | None = None
