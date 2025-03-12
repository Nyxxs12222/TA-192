# Importa las librerías necesarias para FastAPI y otras funcionalidades.
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelspydantic import Usuario, modeloAuth  # Se importa la definición de modelos de Pydantic
from genToken import createToken  # Importa la función para crear tokens JWT
from middlewares import BearerJWT  # Importa middleware para autenticar con JWT

# Inicializa la aplicación FastAPI con configuración básica (título, descripción y versión).
app = FastAPI(
    title='Mi primera API 192',
    description='Maria Monserrat Campuzano Leon',
    version='1.0.1'
)

# Lista de usuarios simulando una base de datos.
lista_usuarios = [
    {"id": 1, "nombre": "monchis", "edad": 22, "correo": "example@example.com"},
    {"id": 2, "nombre": "alejandro", "edad": 24, "correo": "example2@example.com"},
    {"id": 3, "nombre": "maria", "edad": 20, "correo": "example3@example.com"},
    {"id": 4, "nombre": "felix", "edad": 23, "correo": "example4@example.com"}
]

# Endpoint home: Ruta principal para verificar que la API esté funcionando.
@app.get('/', tags=['Hola mundo'])
def home():
    return {'mensaje': 'Bienvenido a FastAPI'}

# Endpoint de autenticación: Recibe las credenciales de usuario y genera un token si son válidas.
@app.post('/auth', tags=['Autentificacion'])
def login(autorizacion: modeloAuth):
    # Valida las credenciales (ejemplo estático para 'uriel@example.com' y '123456789').
    if autorizacion.email == 'uriel@example.com' and autorizacion.passw == '123456789':
        # Si las credenciales son correctas, genera el token con la función createToken.
        token: str = createToken(autorizacion.model_dump())
        print(token)  # Imprime el token para referencia (debe quitarse en producción).
        # Devuelve el token como una respuesta JSON.
        return JSONResponse(content=token)
    else:
        # Si las credenciales no coinciden, retorna un mensaje de error.
        return {"Aviso": "Usuario sin autorizacion"}

# Obtener todos los usuarios: Solo accesible si el usuario está autenticado con JWT.
@app.get('/usuarios', dependencies=[Depends(BearerJWT())], response_model=List[Usuario], tags=['Operaciones CRUD'])
def obtener_usuarios():
    # Retorna la lista de usuarios en formato JSON.
    return lista_usuarios

# Agregar un nuevo usuario: Recibe un nuevo usuario y lo agrega a la lista.
@app.post('/usuarios', response_model=Usuario, tags=['Operaciones CRUD'])
def agregar_usuario(usuario: Usuario):
    # Verifica si el ID del usuario ya existe en la lista.
    for usr in lista_usuarios:
        if usr["id"] == usuario.id:
            # Si el ID ya existe, lanza un error 400 con el mensaje 'El ID ya existe'.
            raise HTTPException(status_code=400, detail="El ID ya existe")
    # Si el ID no existe, agrega el nuevo usuario a la lista.
    lista_usuarios.append(usuario.model_dump())
    return usuario

# Actualizar usuario: Recibe un ID de usuario y los nuevos datos para actualizarlo.
@app.put('/usuarios/{id_usuario}', response_model=Usuario, tags=['Operaciones CRUD'])
def actualizar_usuario(id_usuario: int, usuarioActualizar: Usuario):
    # Busca el usuario por su ID en la lista.
    for i, usr in enumerate(lista_usuarios):
        if usr["id"] == id_usuario:
            # Si encuentra el usuario, lo actualiza con los nuevos datos.
            lista_usuarios[i] = usuarioActualizar.model_dump()
            return lista_usuarios[i]
    # Si no encuentra el usuario, lanza un error 404.
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Endpoint eliminar usuario: Elimina un usuario de la lista por su ID.
@app.delete('/usuario/{id_usuario}', tags=['Operaciones CRUD'])
def deleteUsuario(id_usuario: int):
    # Busca el usuario por su ID en la lista.
    for index, usr in enumerate(lista_usuarios):
        if usr["id"] == id_usuario:
            # Si lo encuentra, lo elimina de la lista.
            lista_usuarios.pop(index)
            return {"mensaje": "Usuario eliminado correctamente"}
    # Si no encuentra el usuario, lanza un error 404.
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
