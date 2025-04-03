from fastapi import FastAPI
from DB.conexion import engine, Base
from routers.usuario import routerUsuario

app = FastAPI(
    title="API Usuarios"
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Inicio"])
def home():
    return {"mensaje": "Bienvenido"}

app.include_router(routerUsuario)