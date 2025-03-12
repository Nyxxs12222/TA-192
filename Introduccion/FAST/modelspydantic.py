# Importa las clases y funciones necesarias de Pydantic para crear modelos de datos y validarlos.
from pydantic import BaseModel, Field, EmailStr

# Modelo para representar a un usuario.
class Usuario(BaseModel):
    # Define el campo 'id' como un entero que debe ser mayor que 0. El campo es obligatorio.
    id: int = Field(..., gt=0, description="ID único y solo positivos")
    
    # Define el campo 'nombre' como una cadena de texto que debe tener entre 3 y 85 caracteres.
    # Además, se asegura de que sea obligatorio y se describe con un mensaje.
    nombre: str = Field(..., min_length=3, max_length=85, description="Solo letras: mínimo 3, máximo 85 caracteres")
    
    # Define el campo 'edad' como un entero mayor que 0 (edad positiva).
    # También es obligatorio y tiene un mensaje descriptivo.
    edad: int = Field(..., gt=0, description="Edad debe ser un número positivo y realista")
    
    # Define el campo 'correo' como un correo electrónico válido utilizando la clase EmailStr de Pydantic.
    # Se describe también como obligatorio y con un ejemplo de formato.
    correo: EmailStr = Field(..., description="Correo electronico valido", example="correo@example.com")

# Modelo para representar la autenticación de usuario con email y contraseña.
class modeloAuth(BaseModel):
    # Define el campo 'email' como un correo electrónico válido.
    # Es obligatorio y tiene un ejemplo de formato de correo.
    email: EmailStr = Field(..., description="Correo Electrónico Válido", example="correo@example.com")
    
    # Define el campo 'passw' como una contraseña que debe tener al menos 8 caracteres.
    # También es obligatorio y se quitan los espacios en blanco extra antes y después de la contraseña.
    passw: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña min 8 caracteres")
