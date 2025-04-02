from fastapi import FastAPI
from DB.conexion import engine, Base
from routers.usuario import routerUsuario
from routers.auth import routerAuth

app = FastAPI(
    title="Mi primera API 192",
    description="Roberto Uriel Martínez Martínez",
    version="1.0.1"
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Inicio"])
def home():
    """Ruta de bienvenida a la API."""
    return {"mensaje": "Bienvenido a FastAPI"}

app.include_router(routerUsuario)
app.include_router(routerAuth)