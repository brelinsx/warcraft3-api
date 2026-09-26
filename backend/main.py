from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.database import Base, engine
from backend import models
from backend.routers import facciones, heroes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Warcraft 3 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(facciones.router)
app.include_router(heroes.router)

@app.get("/", tags=["Root"])
def root():
    return {"msg": "Warcraft 3 API OK, ve a /docs"}