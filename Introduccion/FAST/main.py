from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from modelspydantic import Usuario, modeloAuth  
from genToken import createToken  
from middleware import BearerJWT  
from DB.conexion import Session, engine, Base
from models.modelsDB import User

# Inicialización de la aplicación
app = FastAPI(
    title="Mi primera API 192",
    description="Roberto Uriel Martínez Martínez",
    version="1.0.1"
)

# Creación de las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Datos de prueba
lista_usuarios = [
    {"id": 1, "nombre": "monchis", "edad": 22, "correo": "example@example.com"},
    {"id": 2, "nombre": "alejandro", "edad": 24, "correo": "example2@example.com"},
    {"id": 3, "nombre": "maria", "edad": 20, "correo": "example3@example.com"},
    {"id": 4, "nombre": "felix", "edad": 23, "correo": "example4@example.com"}
]

@app.get("/", tags=["Inicio"])
def home():
    """Ruta de bienvenida a la API."""
    return {"mensaje": "Bienvenido a FastAPI"}

@app.post("/auth", tags=["Autenticación"])
def login(autorizacion: modeloAuth):
    """Autenticación de usuario y generación de token."""
    if autorizacion.email == "uriel@example.com" and autorizacion.passw == "123456789":
        token: str = createToken(autorizacion.model_dump())
        return JSONResponse(content=token)
    return JSONResponse(status_code=401, content={"Aviso": "Usuario sin autorización"})


@app.get("/usuarios", dependencies=[Depends(BearerJWT())], response_model=List[Usuario], tags=["Operaciones CRUD"])
def obtener_usuarios():
    return lista_usuarios

@app.post("/usuarios", response_model=Usuario, tags=["Operaciones CRUD"])
def agregar_usuario(usuario: Usuario):
    db = Session()
    try:
        nuevo_usuario = User(**usuario.model_dump())
        db.add(nuevo_usuario)
        db.commit()
        return JSONResponse(status_code=201, content={"message": "Usuario Guardado", "usuario": usuario.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al guardar usuario", "Exception": str(e)})
    finally:
        db.close()

@app.get("/todosUsuario", tags=["Operaciones CRUD"])
def leer_usuarios():
    db = Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar usuarios", "Exception": str(e)})
    finally:
        db.close()

@app.get("/todosUsuario/{id}", tags=["Operaciones CRUD"])
def leer_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})
        return JSONResponse(content=jsonable_encoder(usuario))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar usuario", "Exception": str(e)})
    finally:
        db.close()

@app.delete("/deleteUsuario/{id}", tags=["Operaciones CRUD"])
def eliminar_usuario(id: int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        db.delete(usuario)
        db.commit()
        return JSONResponse(content={"message": "Usuario eliminado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al eliminar usuario", "Exception": str(e)})

@app.put("/updateUsuario/{id}", response_model=Usuario, tags=["Operaciones CRUD"])
def actualizar_usuario(id: int, usuario: Usuario):
    db = Session()
    try:
        usuario_existente = db.query(User).filter(User.id == id).first()
        if not usuario_existente:
            return JSONResponse(status_code=404, content={"message": "Usuario no encontrado"})

        for key, value in usuario.model_dump().items():
            setattr(usuario_existente, key, value)

        db.commit()
        return JSONResponse(content={"message": "Usuario actualizado correctamente", "usuario": jsonable_encoder(usuario_existente)})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar usuario", "Exception": str(e)})
    finally:
        db.close()


"""
@app.put("/usuarios/{id_usuario}", response_model=Usuario, tags=["Operaciones CRUD"])
def actualizar_usuario(id_usuario: int, usuarioActualizar: Usuario):
    Actualiza un usuario en la lista de prueba.
    for i, usr in enumerate(lista_usuarios):
        if usr["id"] == id_usuario:
            lista_usuarios[i] = usuarioActualizar.model_dump()
            return lista_usuarios[i]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuario/{id_usuario}", tags=["Operaciones CRUD"])
def delete_usuario(id_usuario: int):
    Elimina un usuario de la lista de prueba.
    for index, usr in enumerate(lista_usuarios):
        if usr["id"] == id_usuario:
            lista_usuarios.pop(index)
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
"""
