from beanie import Document
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from enum import Enum
from datetime import datetime
from app.schemas.common import PyObjectId


# 🔹 ENUMS
class EstadoPasswordEnum(str, Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"


class RolUsuarioEnum(str, Enum):
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    SECRETARIA = "secretariaAcademica"


class EstadoVinculacionEnum(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"


# 🔹 Subdocumentos
class Password(BaseModel):
    clave: str
    fechaCambio: datetime
    estado: EstadoPasswordEnum


class Vinculacion(BaseModel):
    rol: RolUsuarioEnum
    programaId: Optional[PyObjectId] = None
    unidadId: Optional[PyObjectId] = None
    facultadId: Optional[PyObjectId] = None
    fecha: Optional[datetime] = None
    estado: Optional[EstadoVinculacionEnum] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


# 🔹 Documento principal
class UsuarioModel(Document):
    id: Optional[int] = Field(alias="_id")
    nombre: str
    apellidos: str
    email: EmailStr
    telefonos: List[str]
    password: List[Password]
    vinculacion: List[Vinculacion]

    class Settings:
        name = "usuario"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True
    )