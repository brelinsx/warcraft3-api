# Trono del reino: la aplicación FastAPI y sus portales (routes).
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import models
from backend.database import Base, engine
from backend.routes import facciones_router, heroes_router


# Despertar de los Antiguos: levanta las tierras (tablas) si aún no existen.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warcraft 3 API", version="0.1.0")

# Pacto de no agresión: el portal web puede invocar a la API sin bloqueo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(facciones_router)
app.include_router(heroes_router)


@app.get("/", tags=["Root"])
def root():
    """Centinela del reino: confirma que la API sigue en pie."""
    return {"msg": "Warcraft 3 API OK, ve a /docs"}
