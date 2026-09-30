# Puerta de Orgrimmar: caminos del clan (solo HTTP, la táctica vive en controllers).
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import schemas
from backend.controllers import facciones as consejo
from backend.database import get_db

router = APIRouter(prefix="/facciones", tags=["Facciones"])


@router.get("/", response_model=list[schemas.FaccionWithHeroes])
def list_facciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return consejo.listar_facciones(db, skip, limit)


@router.get("/{faccion_id}", response_model=schemas.FaccionWithHeroes)
def get_faccion(faccion_id: int, db: Session = Depends(get_db)):
    return consejo.obtener_faccion(db, faccion_id)


@router.post("/", response_model=schemas.FaccionRead, status_code=201)
def create_faccion(data: schemas.FaccionCreate, db: Session = Depends(get_db)):
    return consejo.crear_faccion(db, data)


@router.put("/{faccion_id}", response_model=schemas.FaccionRead)
def update_faccion(faccion_id: int, data: schemas.FaccionCreate, db: Session = Depends(get_db)):
    return consejo.actualizar_faccion(db, faccion_id, data)


@router.delete("/{faccion_id}")
def delete_faccion(faccion_id: int, db: Session = Depends(get_db)):
    return consejo.eliminar_faccion(db, faccion_id)
