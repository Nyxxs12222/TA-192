from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelspydantic import Usuario
from DB.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter

routerUsuario = APIRouter()

@routerUsuario.post("/usuarios", response_model=Usuario, tags=["Operaciones CRUD"])
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

@routerUsuario.get("/todosUsuario", tags=["Operaciones CRUD"])
def leer_usuarios():
    db = Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error al consultar usuarios", "Exception": str(e)})
    finally:
        db.close()

@routerUsuario.get("/todosUsuario/{id}", tags=["Operaciones CRUD"])
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

@routerUsuario.delete("/deleteUsuario/{id}", tags=["Operaciones CRUD"])
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

@routerUsuario.put("/updateUsuario/{id}", response_model=Usuario, tags=["Operaciones CRUD"])
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