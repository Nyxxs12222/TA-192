from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(
    title='Mi primer API 192',
    description='Roberto Uriel Martinez Martinez',
    version='1.0.1'
)

usuarios = [
    {"id": 1, "nombre": "Uriel", "edad": 20},
    {"id": 2, "nombre": "Isay", "edad": 37},
    {"id": 3, "nombre": "Evelyn", "edad": 20},
    {"id": 4, "nombre": "Ana", "edad": 15}
]

# Endpoint home
@app.get('/', tags=['Hola Mundo'])
def home():
    return {'hello': 'world FastAPI'}

#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios', tags=['Operaciones CRUD'])
def leerUsuarios():
    return {"Los usuarios registrados son ": usuarios}

#Endpoint Agregar Nuevos 
@app.post('/usuario/', tags=['Operaciones CRUD'])
def agregarUsuario(usuario:dict):
    for usr in usuarios: 
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code = 400, detail="El id ya existe")

    usuarios.append(usuario)
    return usuario

# Endpoint Actualizar 
@app.put('/usuario/{id}', tags=['Operaciones CRUD'])
def actualizarUsuario(id: int, usuarioAct: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuarioAct) 
            return {"mensaje": "Usuario actualizado correctamente", "usuario": usuarios[index]}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Endpoint Eliminar 
@app.delete('/usuario/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {"Usuario Eliminado"}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

""" 
# Endpoint promedio
@app.get('/promedio', tags=['Promedios'])
def promedio():
    return 5.5

# Endpoint parámetro obligatorio
@app.get('/usuario/{id}', tags=['Parámetro obligatorio'])
def consultaUsuario(id: int):
    # conectamos a la BD
    # consultamos
    return {'Se encontró el usuario': id}

# Endpoint parámetro opcional
@app.get('/usuario/', tags=['Parámetro Opcional'])
def consultaUsuario2(id: Optional[int] = None):
    if id is not None:
        for usu in usuarios:
            if usu["id"] == id:
                return {"mensaje": "Usuario encontrado", "usuario": usu}
        return {"mensaje": f"No se encontró el usuario con id: {id}"}
    else:
        return {"mensaje": "No se proporcionó un id"}
    
#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."} """