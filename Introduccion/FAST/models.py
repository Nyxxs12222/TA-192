from pydantic import BaseModel, Field

# Modelo
class Usuario(BaseModel):
    id: int = Field(..., gt=0, description="ID único y solo positivos")
    nombre: str = Field(..., min_length=3, max_length=85, description="Solo letras: mínimo 3, máximo 85 caracteres")
    edad: int = Field(..., gt=0, description="Edad debe ser un número positivo y realista")
    correo: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Debe ser un correo electrónico válido")