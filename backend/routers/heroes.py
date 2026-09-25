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

@router.post("/", response_model=schemas.HeroeRead, status_code=201)
def create_heroe(data: schemas.HeroeCreate, db: Session = Depends(get_db)):
    if not db.query(models.Faccion).filter(models.Faccion.id == data.faccion_id).first():
        raise HTTPException(status_code=400, detail="faccion_id no existe")
    h = models.Heroe(**data.model_dump())
    db.add(h); db.commit(); db.refresh(h)
    return h

@router.put("/{heroe_id}", response_model=schemas.HeroeRead)
def update_heroe(heroe_id: int, data: schemas.HeroeCreate, db: Session = Depends(get_db)):
    h = db.query(models.Heroe).filter(models.Heroe.id == heroe_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    if data.faccion_id != h.faccion_id and not db.query(models.Faccion).filter(models.Faccion.id == data.faccion_id).first():
        raise HTTPException(status_code=400, detail="faccion_id no existe")
    for k, v in data.model_dump().items():
        setattr(h, k, v)
    db.commit(); db.refresh(h)
    return h

@router.delete("/{heroe_id}")
def delete_heroe(heroe_id: int, db: Session = Depends(get_db)):
    h = db.query(models.Heroe).filter(models.Heroe.id == heroe_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    db.delete(h); db.commit()
    return {"detail": f"Heroe {heroe_id} eliminado"}