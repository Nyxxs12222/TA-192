from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI(
    title='Examen2doP',
    description='Roberto Uriel Martinez Martinez'
)

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=3, description="Mínimo 3 letras")
    tipo_licencia: str = Field(..., min_length=1, max_length=1, description="Solo pueden ser los caracteres A, B, C, D")
    no_licencia: str = Field(..., min_length=12, max_length=12, description="Debe tener 12 dígitos numéricos")

lista_usuarios = [
    Usuario(nombre="Uriel", tipo_licencia="A", no_licencia="123456789012"),
    Usuario(nombre="Jaime", tipo_licencia="A", no_licencia="123456789013")
]

@app.get('/usuarios/{no_licencia}', response_model=Usuario, tags=['CRUD'])
def obtener_usuario(no_licencia: str):
    for usr in lista_usuarios:
        if usr.no_licencia == no_licencia:
            return usr
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete('/usuario/{no_licencia}', tags=['CRUD'])
def delete_usuario(no_licencia: str):
    for index, usr in enumerate(lista_usuarios):
        if usr.no_licencia == no_licencia:
            lista_usuarios.pop(index)
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
