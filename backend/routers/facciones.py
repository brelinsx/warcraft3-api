from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.database import get_db
from backend import models, schemas

router = APIRouter(prefix="/facciones", tags=["Facciones"])

@router.get("/", response_model=list[schemas.FaccionWithHeroes])
def list_facciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Faccion).options(joinedload(models.Faccion.heroes)).offset(skip).limit(limit).all()

@router.get("/{faccion_id}", response_model=schemas.FaccionWithHeroes)
def get_faccion(faccion_id: int, db: Session = Depends(get_db)):
    f = db.query(models.Faccion).options(joinedload(models.Faccion.heroes)).filter(models.Faccion.id == faccion_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faccion no encontrada")
    return f