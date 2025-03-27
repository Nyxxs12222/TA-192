from pydantic import BaseModel, Field, EmailStr

class Usuario(BaseModel):
    name: str = Field(..., min_length=3, max_length=85, description="Solo letras: mínimo 3, máximo 85 caracteres")
    age: int = Field(..., gt=0, description="Edad debe ser un número positivo y realista")
    email: EmailStr = Field(..., description="Correo electronico valido", example="correo@example.com")

class modeloAuth(BaseModel):
    email: EmailStr = Field(..., description="Correo Electrónico Válido", example="correo@example.com")
    passw: str = Field(..., min_length=8, strip_whitespace=True, description="Contraseña min 8 caracteres")
