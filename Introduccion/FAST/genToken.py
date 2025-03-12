# Importa la librería jwt que se usa para generar y verificar tokens.
import jwt
# Importa las excepciones ExpiredSignatureError e InvalidTokenError específicas de jwt para manejar errores al decodificar el token.
from jwt import ExpiredSignatureError, InvalidTokenError
# Importa HTTPException desde fastapi para poder lanzar errores HTTP personalizados si ocurre algún problema.
from fastapi import HTTPException

# Función para crear un token
def createToken(data: dict):
    # Usa el método encode de la librería jwt para crear un token. 
    # `payload=data` es la información que se va a codificar en el token.
    # `key='secretkey'` es la clave secreta que se usará para la firma (debe mantenerse en secreto).
    # `algorithm='HS256'` especifica que se usará el algoritmo HMAC con SHA-256 para firmar el token.
    token: str = jwt.encode(payload=data, key='secretkey', algorithm='HS256')
    # Retorna el token generado.
    return token

# Función para validar y decodificar un token
def validateToken(token: str):
    try:
        # Intenta decodificar el token usando la misma clave secreta.
        # `algorithms=['HS256']` indica que se usará el algoritmo HS256 para verificar la firma.
        data: dict = jwt.decode(token, key='secretkey', algorithms=['HS256'])
        # Si el token es válido, retorna los datos contenidos en el payload del token.
        return data
    except ExpiredSignatureError:
        # Si el token ha expirado, lanza una excepción HTTP con el código de estado 403 (Prohibido).
        # Detalle: 'token expirado'.
        raise HTTPException(status_code=403, detail='token expirado')
    except InvalidTokenError:
        # Si el token es inválido, lanza una excepción HTTP con el código de estado 403 (Prohibido).
        # Detalle: 'token no autorizado'.
        raise HTTPException(status_code=403, detail='token no autorizado')
