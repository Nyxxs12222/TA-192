from fastapi import FastAPI, HTTPException
from typing import List, Dict

app = FastAPI(
    title='Administrador de Tareas',
    description='Roberto Uriel Martinez Martinez',
)

tareas = [
    {
        "id": 1, 
        "Titulo": "Mandado", 
        "Descripcion": "Repasar los apuntes de TAI ",
        "Vencimiento" : "“14-02-24”", 
        "Estado" : "Completada"
    }
]

@app.get('/Todas_las_tareas', tags=['Opciones Tareas'])
def mostrarTareas():
    return {"Las tareas registradas son": tareas}

@app.post('/tareas/', tags=['Opciones Tareas'])
def crearTarea(tarea: Dict):
    for t in tareas:
        if t["id"] == tarea.get("id"):
            raise HTTPException(status_code=400, detail="Este id ya existe")

    tareas.append(tarea)
    return tarea

@app.put('/tareas/{id}', tags=['Opciones Tareas'])
def editarTarea(id: int, TaskUpd: dict):
    for index, t in enumerate(tareas):
        if t["id"] == id:
            tareas[index].update(TaskUpd) 
            return {"mensaje": "Se actualizo la tarea correctamente", "tarea": tareas[index]}
    
    raise HTTPException(status_code=404, detail="No se encontro ninguna tarea")

@app.delete('/tareas/{id}', tags=['Opciones Tareas'])
def eliminarTarea(id: int):
    for index, t in enumerate(tareas):
        if t["id"] == id:
            tareas.pop(index)
            return {"Tarea Eiminada"}
    
    raise HTTPException(status_code=404, detail="No se encontro ninguna tarea")