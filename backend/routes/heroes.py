# Portal del Altar: caminos de los héroes (solo HTTP, el ritual vive en controllers).
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import schemas
from backend.controllers import heroes as altar
from backend.database import get_db

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.get("/", response_model=list[schemas.HeroeWithFaccion])
def list_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return altar.listar_heroes(db, skip, limit)


@router.get("/{heroe_id}", response_model=schemas.HeroeWithFaccion)
def get_heroe(heroe_id: int, db: Session = Depends(get_db)):
    return altar.obtener_heroe(db, heroe_id)


@router.post("/", response_model=schemas.HeroeRead, status_code=201)
def create_heroe(data: schemas.HeroeCreate, db: Session = Depends(get_db)):
    return altar.crear_heroe(db, data)


@router.put("/{heroe_id}", response_model=schemas.HeroeRead)
def update_heroe(heroe_id: int, data: schemas.HeroeCreate, db: Session = Depends(get_db)):
    return altar.actualizar_heroe(db, heroe_id, data)


@router.delete("/{heroe_id}")
def delete_heroe(heroe_id: int, db: Session = Depends(get_db)):
    return altar.eliminar_heroe(db, heroe_id)
