# Importa las clases necesarias para manejar excepciones HTTP y solicitudes de FastAPI.
from fastapi import HTTPException, Request
# Importa la clase HTTPBearer para manejar la autenticación basada en tokens Bearer.
from fastapi.security import HTTPBearer
# Importa la función validateToken que valida el token JWT.
from genToken import validateToken

# Crea una clase personalizada BearerJWT que hereda de HTTPBearer para usar en la autenticación.
class BearerJWT(HTTPBearer):
    # Sobrescribe el método __call__ para manejar la lógica de autenticación con el token JWT.
    async def __call__(self, request: Request):
        # Llama al método de la clase base para obtener el token desde los encabezados de la solicitud.
        auth = await super().__call__(request)

        # Valida el token recibido usando la función validateToken.
        data = validateToken(auth.credentials)

        # Si el dato validado no es un diccionario, se lanza un error de token inválido (401).
        if not isinstance(data, dict):  
            raise HTTPException(status_code=401, detail="Token inválido")

        # Verifica que el 'email' del token coincida con el valor esperado (en este caso 'uriel@example.com').
        # Si no coincide, se lanza un error de credenciales no válidas (403).
        if data.get('email') != "uriel@example.com": 
            raise HTTPException(status_code=403, detail="Credenciales no válidas")
