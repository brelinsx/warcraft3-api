# Pergaminos del escriba para los estandartes de los clanes.
from pydantic import BaseModel, Field


class FaccionBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    recurso_especial: str | None = Field(default=None, max_length=100)


class FaccionCreate(FaccionBase):
    pass


class FaccionRead(FaccionBase):
    id: int

    class Config:
        from_attributes = True


class FaccionSimple(BaseModel):
    id: int
    nombre: str
    recurso_especial: str | None = None

    class Config:
        from_attributes = True
