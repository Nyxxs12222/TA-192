from fastapi.responses import JSONResponse
from modelspydantic import modeloAuth  
from genToken import createToken  
from middleware import BearerJWT  
from fastapi import APIRouter

routerAuth = APIRouter()

@routerAuth.post("/auth", tags=["Autenticación"])
def login(autorizacion: modeloAuth):
    """Autenticación de usuario y generación de token."""
    if autorizacion.email == "uriel@example.com" and autorizacion.passw == "123456789":
        token: str = createToken(autorizacion.model_dump())
        return JSONResponse(content=token)
    return JSONResponse(status_code=401, content={"Aviso": "Usuario sin autorización"})
