from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.eventos import (
    EstadoEventoEnum,
    TipoEventoEnum,
    TipoAvalEnum,
    OrganizacionParticipante,
    UsuarioTipo,
)
from app.schemas.common import PyObjectId


# 🔹 Subschemas (idénticos al modelo para compatibilidad con Beanie)
class InstalacionSchema(BaseModel):
    instalacionId: str
    capacidadInstalacion: int


class RealizacionSchema(BaseModel):
    instalaciones: List[InstalacionSchema]
    fecha: datetime
    horaInicio: str
    horaFin: str


class OrganizadorSchema(BaseModel):
    usuarioId: int
    avalPDF: Optional[bytes] = None
    tipoAval: TipoAvalEnum
    tipo: UsuarioTipo


class OrganizacionSchema(BaseModel):
    organizacionId: PyObjectId
    participante: OrganizacionParticipante
    nombreParticipante: str
    certificadoParticipacion: Optional[bytes] = None


# 🔹 Base para creación
class EventoCreate(BaseModel):
    nombre: str
    estado: EstadoEventoEnum = EstadoEventoEnum.REGISTRADO
    tipo: TipoEventoEnum
    realizacion: RealizacionSchema
    organizador: List[OrganizadorSchema]
    organizacion: Optional[List[OrganizacionSchema]] = None
    capacidad: int


# 🔹 Para actualización parcial
class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    estado: Optional[EstadoEventoEnum] = None
    tipo: Optional[TipoEventoEnum] = None
    realizacion: Optional[RealizacionSchema] = None
    organizador: Optional[List[OrganizadorSchema]] = None
    organizacion: List[OrganizacionSchema] = Field(default_factory=list)
    capacidad: Optional[int] = None


# 🔹 Para respuesta (GET)
class EventoResponse(EventoCreate):
    id: PyObjectId = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
        from_attributes = True
