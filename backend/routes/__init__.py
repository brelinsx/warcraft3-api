# Caminos del reino: reexporta las rutas para el trono (main).
from backend.routes.facciones import router as facciones_router
from backend.routes.heroes import router as heroes_router

__all__ = ["facciones_router", "heroes_router"]
