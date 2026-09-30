# Altar de los Héroes: el ritual de los campeones (lógica de negocio).
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from backend import models, schemas


def listar_heroes(db: Session, skip: int = 0, limit: int = 100):
    """Pasa revista a los campeones, cada uno junto a su clan."""
    return (
        db.query(models.Heroe)
        .options(joinedload(models.Heroe.faccion))
        .order_by(models.Heroe.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def obtener_heroe(db: Session, heroe_id: int):
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


def crear_heroe(db: Session, data: schemas.HeroeCreate):
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


def actualizar_heroe(db: Session, heroe_id: int, data: schemas.HeroeCreate):
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


def eliminar_heroe(db: Session, heroe_id: int):
    """Destierra a un héroe en silencio; 404 si su nombre es leyenda vacía."""
    h = db.query(models.Heroe).filter(models.Heroe.id == heroe_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Heroe no encontrado")
    db.delete(h)
    db.commit()
    return {"detail": f"Heroe {heroe_id} eliminado"}
