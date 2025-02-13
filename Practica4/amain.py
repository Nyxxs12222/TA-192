from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI(
    title='Administrador de Tareas',
    description='Roberto Uriel Martinez Martinez',
    version='1.0.1'
)

tareas = [
    {
        "id": 1, "Titulo": 
        "Mandado", "Descripcion": 
        "Comprar 20 Huveos, 10 manzanas", 
        "Vencimiento" : "None", 
        "Estado" : "Activo"
    }
]

@app.get('/Todas_las_tareas', tags=['CRUD'])
def showTasks():
    return {"Las tareas registradas son": tareas}

@app.post('/tareas/', tags=['CRUD'])
def makeTask(tarea: Dict):
    for t in tareas:
        if t["id"] == tarea.get("id"):
            raise HTTPException(status_code=400, detail="Este id ya existe")

    tareas.append(tarea)
    return tarea

@app.delete('/tareas/{id}', tags=['CRUD'])
def deleteTask(id: int):
    for index, t in enumerate(tareas):
        if t["id"] == id:
            tareas.pop(index)
            return {"Tarea Eiminada"}
    
    raise HTTPException(status_code=404, detail="No se encontro ninguna tarea")