from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

from app.schemas.common import PyObjectId
from app.models.usuarios import (
    RolUsuarioEnum,
    EstadoVinculacionEnum,
    EstadoPasswordEnum
)


# 🔹 Subschemas

class PasswordSchema(BaseModel):
    clave: str
    fechaCambio: datetime
    estado: EstadoPasswordEnum


class VinculacionSchema(BaseModel):
    rol: RolUsuarioEnum
    programaId: Optional[PyObjectId] = None
    unidadId: Optional[PyObjectId] = None
    facultadId: Optional[PyObjectId] = None
    fecha: Optional[datetime] = None
    estado: Optional[EstadoVinculacionEnum] = None


# 🔹 Base para crear usuario
class UsuarioCreate(BaseModel):
    id: int = Field(..., alias="_id")

    nombre: str
    apellidos: str
    email: EmailStr
    telefonos: List[str]

    password: List[PasswordSchema]

    vinculacion: List[VinculacionSchema]

    class Config:
        populate_by_name = True
        from_attributes = True


# 🔹 Para actualización
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[EmailStr] = None
    telefonos: Optional[List[str]] = None

    password: Optional[List[PasswordSchema]] = None
    vinculacion: Optional[List[VinculacionSchema]] = None


# 🔹 Respuesta del API
class UsuarioResponse(UsuarioCreate):
    class Config:
        populate_by_name = True
        from_attributes = True