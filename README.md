# Warcraft 3 API — API REST + Cliente Web

API REST completa en **FastAPI** con modelo relacional 1:N y portal web en **HTML + CSS + JavaScript + Axios** para documentar y probar la API.
Temática: universo Warcraft 3 — **facciones** y **héroes**.

Relación: una facción tiene muchos héroes. Un héroe pertenece a una sola facción.

## 1. Descripción

**Backend (70% del proyecto):**
- CRUD relacional completo sobre 2 tablas con PK/FK.
- Lectura con datos relacionados (`facción con sus héroes`, `héroe con su facción`).
- Validación con Pydantic y códigos HTTP semánticos.
- Integridad referencial: sin `faccion_id` huérfanos, sin nombres de facción duplicados, borrado en cascada.

**Frontend (cliente de soporte):**
- Portal de documentación + demo viva.
- Listado, creación, edición y borrado desde la web con Axios.
- Búsqueda por nombre, filtrado por facción, mensajes de éxito/error y estados de carga.
- Responsive Mobile First con identidad Warcraft (oscuro + dorado).

## 2. Tecnologías

- Python 3.14 + venv
- FastAPI 0.141.1
- Uvicorn 0.53.0
- SQLAlchemy 2.0.54 + SQLite (`warcraft3.db`, no se sube a Git)
- Pydantic 2.13.5 / pydantic-core 2.46.5
- Starlette 1.6.0, AnyIO 4.15.1, httpx 0.28.1 (tests)
- Frontend: HTML5 semántico, CSS3, JavaScript Vanilla, Axios vía CDN
- Git + Gitflow (`main` / `develop` / `feature/*`), GitHub

## 3. Instalación local paso a paso (Windows PowerShell)

```powershell
# 1. Clonar e ir a la raíz
git clone https://github.com/brelinsx/warcraft3-api.git
cd "API REST"

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar (PowerShell)
.\venv\Scripts\Activate.ps1
# Si da error de ejecución: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 4. Instalar dependencias
python -m pip install -r backend/requirements.txt

# 5. Arrancar backend
uvicorn backend.main:app --reload
# API: http://127.0.0.1:8000
# Swagger: http://127.0.0.1:8000/docs

# 6. Abrir frontend (nueva terminal, backend corriendo)
cd frontend
python -m http.server 5500
# Abrir http://localhost:5500/
# Alternativa: doble clic en frontend/index.html
```

Estructura:
```
API REST/
  backend/
    main.py          # app + CORS + include routers
    database.py      # engine SQLite, SessionLocal, Base, get_db
    models.py        # Faccion, Heroe
    schemas.py       # Pydantic Create/Read + WithHeroes/WithFaccion
    routers/
      facciones.py
      heroes.py
    requirements.txt
  frontend/
    index.html
    styles.css
    app.js
  warcraft3.db       # generado solo, ignorado por Git
```

## 4. Diagrama Entidad-Relación (DER)

```
facciones 1 --- N heroes

facciones(
  id INT PK AUTOINCREMENT,
  nombre TEXT UNIQUE NOT NULL,
  recurso_especial TEXT NULL
)

heroes(
  id INT PK AUTOINCREMENT,
  nombre TEXT NOT NULL,
  clase_heroe TEXT NOT NULL,
  atributo_principal TEXT NOT NULL CHECK(Fuerza|Agilidad|Inteligencia),
  faccion_id INT NOT NULL FK -> facciones.id ON DELETE CASCADE
)
```

- `Faccion.heroes = relationship("Heroe", back_populates="faccion", cascade="all, delete-orphan")`
- Borrar una facción borra sus héroes. No se puede crear héroe con `faccion_id` inexistente.

Datos semilla actuales (limpios):
- Horda (1) / Alianza (2) / No-muertos (3) / Elfos Nocturnos (4)
- Thrall-Horda, Jaina-Alianza, Arthas-No-muertos, Tyrande-Elfos Nocturnos

## 5. Documentación de endpoints

Base: `http://127.0.0.1:8000`

| Método | Ruta | Descripción | Params | Éxito | Errores |
|---|---|---|---|---|---|
| GET | `/` | Healthcheck | — | 200 `{msg}` | 500 |
| GET | `/facciones/` | Listar con héroes + paginación | `skip=0`, `limit=100` query | 200 `[FaccionWithHeroes]` | 422, 500 |
| GET | `/facciones/{id}` | Una facción con héroes | `id` path int | 200 | 404, 422, 500 |
| POST | `/facciones/` | Crear | body `FaccionCreate` | 201 | 400 duplicado, 422 validación, 500 |
| PUT | `/facciones/{id}` | Actualizar total | `id` + body `FaccionCreate` | 200 | 404, 400 duplicado, 422, 500 |
| DELETE | `/facciones/{id}` | Borrar + cascade | `id` | 200 `{detail}` | 404, 500 |
| GET | `/heroes/` | Listar con facción + paginación | `skip`, `limit` | 200 `[HeroeWithFaccion]` | 422, 500 |
| GET | `/heroes/{id}` | Un héroe con facción | `id` | 200 | 404, 422, 500 |
| POST | `/heroes/` | Crear | body `HeroeCreate` | 201 | 400 `faccion_id no existe`, 422, 500 |
| PUT | `/heroes/{id}` | Actualizar total | `id` + body | 200 | 404, 400 FK, 422, 500 |
| DELETE | `/heroes/{id}` | Borrar | `id` | 200 | 404, 500 |

Validaciones Pydantic (422 automático):
- `nombre`, `clase_heroe`: 2-50 chars.
- `atributo_principal`: `^(Fuerza|Agilidad|Inteligencia)$`.
- `faccion_id`: int requerido.
- `recurso_especial`: opcional, max 100.

### Ejemplos

```bash
# Crear facción -> 201
curl -X POST http://127.0.0.1:8000/facciones/ -H "Content-Type: application/json" -d "{\"nombre\":\"Horda\",\"recurso_especial\":\"Madera\"}"
# {"nombre":"Horda","recurso_especial":"Madera","id":1}

# Duplicada -> 400
# {"detail":"Nombre de faccion ya existe"}

# Crear héroe -> 201
curl -X POST http://127.0.0.1:8000/heroes/ -H "Content-Type: application/json" -d "{\"nombre\":\"Thrall\",\"clase_heroe\":\"Chaman\",\"atributo_principal\":\"Inteligencia\",\"faccion_id\":1}"

# FK falsa -> 400
# {"detail":"faccion_id no existe"}

# Atributo malo -> 422
# {"detail":[{...,"loc":["body","atributo_principal"]...}]}

# Leer con relación -> 200
curl http://127.0.0.1:8000/facciones/1
# {"nombre":"Horda",...,"heroes":[{"id":1,"nombre":"Thrall",...}]}

curl http://127.0.0.1:8000/heroes/1
# {"nombre":"Thrall",...,"faccion":{"id":1,"nombre":"Horda",...}}

# Inexistente -> 404
curl http://127.0.0.1:8000/facciones/999
# {"detail":"Faccion no encontrada"}
```

Frontend usa los mismos códigos: verde OK, rojo `detail` del backend, `OK - N facciones` o `ERROR: arranca backend`.

## 6. Revisión de código y DB (Día 8)

- Backend: `snake_case` en archivos/columnas, `PascalCase` en `Faccion/Heroe`, `joinedload` en READ, `model_dump()` + `setattr` en PUT, `HTTPException` 400/404 explícitos.
- Frontend `app.js`: `"use strict"`, `state` único (sin `ALL_*` sueltas), `escapeHtml` anti-XSS, `trim()` + `parseInt(v,10)`, `addEventListener` + delegación `data-action` (sin `onclick` inline), helper `getErrorDetail`.
- DB limpiada el Día 8: borrado total + reseed 4+4 vía API (IDs 1-4, sin `string-string`, Arthas en No-muertos). `warcraft3.db` ignorado en `.gitignore` (`venv/`, `__pycache__/`, `*.db`, `*.sqlite`, `.env`).
- Verificado con TestClient: 201/200/400/404/422, paginación `skip/limit`, cascade facción->héroes, Swagger `/docs` y web `localhost:5500` en `OK`.
