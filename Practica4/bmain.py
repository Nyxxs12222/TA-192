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

@app.put('/tareas/{id}', tags=['Opciones Tareas'])
def editarTarea(id: int, TaskUpd: Tarea):
    for index, t in enumerate(tareas):
        if t.id == id:
            tareas[index] = TaskUpd
            return {"mensaje": "Se actualizó la tarea correctamente", "tarea": tareas[index]}
    
    raise HTTPException(status_code=404, detail="No se encontró ninguna tarea")

@app.delete('/tareas/{id}', tags=['Opciones Tareas'])
def eliminarTarea(id: int):
    for index, t in enumerate(tareas):
        if t.id == id:
            tareas.pop(index)
            return {"mensaje": "Tarea Eliminada"}
    
    raise HTTPException(status_code=404, detail="No se encontró ninguna tarea")