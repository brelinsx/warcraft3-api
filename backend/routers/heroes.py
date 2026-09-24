from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.database import get_db
from backend import models, schemas

router = APIRouter(prefix="/heroes", tags=["Heroes"])

@router.get("/", response_model=list[schemas.HeroeWithFaccion])
def list_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Heroe).options(joinedload(models.Heroe.faccion)).offset(skip).limit(limit).all()

@router.get("/{heroe_id}", response_model=schemas.HeroeWithFaccion)
def get_heroe(heroe_id: int, db: Session = Depends(get_db)):
    h = db.query(models.Heroe).options(joinedload(models.Heroe.faccion)).filter(models.Heroe.id == heroe_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    return h