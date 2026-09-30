# Consejo de guerra: la táctica de los clanes (lógica de negocio).
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from backend import models, schemas


def listar_facciones(db: Session, skip: int = 0, limit: int = 100):
    """Recorre el reino página a página, cada clan con su hueste."""
    return (
        db.query(models.Faccion)
        .options(joinedload(models.Faccion.heroes))
        .order_by(models.Faccion.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def obtener_faccion(db: Session, faccion_id: int):
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


def crear_faccion(db: Session, data: schemas.FaccionCreate):
    """Funda un clan nuevo; 400 si su nombre ya ondea en otra torre."""
    if db.query(models.Faccion).filter(models.Faccion.nombre == data.nombre).first():
        raise HTTPException(status_code=400, detail="Nombre de faccion ya existe")
    f = models.Faccion(**data.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


def actualizar_faccion(db: Session, faccion_id: int, data: schemas.FaccionCreate):
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


def eliminar_faccion(db: Session, faccion_id: int):
    """Arrasa el clan y su hueste con él (cascada)."""
    f = db.query(models.Faccion).filter(models.Faccion.id == faccion_id).first()
    if not f:
        raise HTTPException(status_code=404, detail="Faccion no encontrada")
    db.delete(f)
    db.commit()
    return {"detail": f"Faccion {faccion_id} eliminada con sus heroes"}
