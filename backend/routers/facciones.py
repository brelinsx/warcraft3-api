# Puerta de Orgrimmar: rutas del clan de las facciones.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/facciones", tags=["Facciones"])


@router.get("/", response_model=list[schemas.FaccionWithHeroes])
def list_facciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Recorre el reino página a página, cada clan con su hueste."""
    return (
        db.query(models.Faccion)
        .options(joinedload(models.Faccion.heroes))
        .order_by(models.Faccion.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{faccion_id}", response_model=schemas.FaccionWithHeroes)
def get_faccion(faccion_id: int, db: Session = Depends(get_db)):
    """Busca un estandarte por su sello; 404 si yace en el olvido."""
    f = (
        db.query(models.Faccion)
        .options(joinedload(models.Faccion.heroes))
        .filter(models.Faccion.id == faccion_id)
        .first()
    )
    if not f:
        raise HTTPException(status_code=404, detail="Faccion no encontrada")
    return f


@router.post("/", response_model=schemas.FaccionRead, status_code=201)
def create_faccion(data: schemas.FaccionCreate, db: Session = Depends(get_db)):
    """Funda un clan nuevo; 400 si su nombre ya ondea en otra torre."""
    if db.query(models.Faccion).filter(models.Faccion.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Nombre de faccion ya existe")
    f = models.Faccion(**data.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


@router.put("/{faccion_id}", response_model=schemas.FaccionRead)
def update_faccion(faccion_id: int, data: schemas.FaccionCreate, db: Session = Depends(get_db)):
    """Reescribe el estandarte; 404 si el clan no existe."""
    f = db.query(models.Faccion).filter(models.Faccion.id == faccion_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faccion no encontrada")
    if data.nombre != f.nombre:
        if db.query(models.Faccion).filter(models.Faccion.nombre == data.nombre).first():
            raise HTTPException(status_code=400, detail="Nombre de faccion ya existe")
    for field, value in data.model_dump().items():
        setattr(f, field, value)
    db.commit()
    db.refresh(f)
    return f


@router.delete("/{faccion_id}")
def delete_faccion(faccion_id: int, db: Session = Depends(get_db)):
    """Arrase total: cae el clan y su hueste con él (cascada)."""
    f = db.query(models.Faccion).filter(models.Faccion.id == faccion_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faccion no encontrada")
    db.delete(f)
    db.commit()
    return {"detail": f"Faccion {faccion_id} eliminada con sus heroes"}
