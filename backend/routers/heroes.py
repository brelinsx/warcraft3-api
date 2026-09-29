# Altar de los Héroes: rutas de los campeones del reino.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.get("/", response_model=list[schemas.HeroeWithFaccion])
def list_heroes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Pasa revista a los campeones, cada uno junto a su clan."""
    return (
        db.query(models.Heroe)
        .options(joinedload(models.Heroe.faccion))
        .order_by(models.Heroe.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{heroe_id}", response_model=schemas.HeroeWithFaccion)
def get_heroe(heroe_id: int, db: Session = Depends(get_db)):
    """Llama a un campeón por su nombre de guerra; 404 si nunca existió."""
    h = (
        db.query(models.Heroe)
        .options(joinedload(models.Heroe.faccion))
        .filter(models.Heroe.id == heroe_id)
        .first()
    )
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    return h


@router.post("/", response_model=schemas.HeroeRead, status_code=201)
def create_heroe(data: schemas.HeroeCreate, db: Session = Depends(get_db)):
    """Invoca un héroe en el Altar; 400 si el clan no existe o el
    nombre ya está grabado en la piedra."""
    if not db.query(models.Faccion).filter(models.Faccion.id == data.faccion_id).first():
        raise HTTPException(status_code=400, detail="faccion_id no existe")
    if db.query(models.Heroe).filter(models.Heroe.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="El héroe ya está registrado en el Altar")
    h = models.Heroe(**data.model_dump())
    db.add(h)
    db.commit()
    db.refresh(h)
    return h


@router.put("/{heroe_id}", response_model=schemas.HeroeRead)
def update_heroe(heroe_id: int, data: schemas.HeroeCreate, db: Session = Depends(get_db)):
    """Reforja a un campeón; 404 si cayó en batalla, 400 si jura por un clan falso."""
    h = db.query(models.Heroe).filter(models.Heroe.id == heroe_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    if data.faccion_id != h.faccion_id:
        if not db.query(models.Faccion).filter(models.Faccion.id == data.faccion_id).first():
            raise HTTPException(status_code=400, detail="faccion_id no existe")
    for field, value in data.model_dump().items():
        setattr(h, field, value)
    db.commit()
    db.refresh(h)
    return h


@router.delete("/{heroe_id}")
def delete_heroe(heroe_id: int, db: Session = Depends(get_db)):
    """Destierra a un héroe en silencio; 404 si su nombre es leyenda vacía."""
    h = db.query(models.Heroe).filter(models.Heroe.id == heroe_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    db.delete(h)
    db.commit()
    return {"detail": f"Heroe {heroe_id} eliminado"}
