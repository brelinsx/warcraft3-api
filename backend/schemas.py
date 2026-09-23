from pydantic import BaseModel, Field

# --- Facciones ---
class FaccionBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    recurso_especial: str | None = Field(default=None, max_length=100)

class FaccionCreate(FaccionBase):
    pass

class FaccionRead(FaccionBase):
    id: int
    class Config:
        from_attributes = True

# --- Heroes ---
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