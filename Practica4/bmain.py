from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title='Administrador de Tareas',
    description='Hecho por Roberto Martinez',
)

class Tarea(BaseModel):
    id: int
    Titulo: str
    Descripcion: str
    Vencimiento: str
    Estado: str

tareas = []

@app.get('/Todas_las_tareas', tags=['Opciones Tareas'])
def mostrarTareas():
    return {"Las tareas registradas son": tareas}

@app.post('/tareas/', tags=['Opciones Tareas'])
def crearTarea(tarea: Tarea):
    for t in tareas:
        if t.id == tarea.id:
            raise HTTPException(status_code=400, detail="Este id ya existe")
    tareas.append(tarea)
    return tarea
