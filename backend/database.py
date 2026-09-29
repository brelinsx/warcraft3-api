# Altar de los Héroes: forja la conexión con la piedra rúnica (SQLite).
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Manantial de maná: archivo donde duerme la base de datos del reino.
DATABASE_URL = "sqlite:///./warcraft3.db"

# Portal Oscuro: motor que abre el paso hacia las tierras de los datos.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cuartel: forja una sesión de batalla por cada petición que llega.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pergamino ancestral: linaje del que descienden todos los clanes (modelos).
Base = declarative_base()


def get_db():
    """Invoca una sesión y la destierra cuando el hechizo termina."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
