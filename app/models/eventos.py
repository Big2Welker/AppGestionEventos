from beanie import Document
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum
from app.schemas.common import PyObjectId


# 🔹 ENUMS
class EstadoEventoEnum(str, Enum):
    REGISTRADO = "registrado"
    EN_REVISION = "enRevision"
    APROVADO = "aprovado"


class TipoEventoEnum(str, Enum):
    LUDICO = "ludico"
    ACADEMICO = "academico"


class TipoAvalEnum(str, Enum):
    DIRECTOR_PROGRAMA = "directorPrograma"
    DIRECTOR_DOCENCIA = "directorDocencia"


class OrganizacionParticipante(str, Enum):
    REPRESENTANTE_LEGAL = "representanteLegal"
    OTRO = "otro"


class UsuarioTipo(str, Enum):
    PRINCIPAL = "principal"
    SECUNDARIO = "secundario"


# 🔹 Subdocumentos
class Instalacion(BaseModel):
    instalacionId: str
    capacidadInstalacion: int


class Realizacion(BaseModel):
    instalaciones: List[Instalacion]
    fecha: datetime
    horaInicio: str
    horaFin: str


class Organizador(BaseModel):
    usuarioId: int
    avalPDF: bytes
    tipoAval: TipoAvalEnum
    tipo: UsuarioTipo

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Organizacion(BaseModel):
    organizacionId: PyObjectId
    participante: OrganizacionParticipante
    nombreParticipante: str
    certificadoParticipacion: bytes

    model_config = ConfigDict(arbitrary_types_allowed=True)


# 🔹 Documento principal
class EventoModel(Document):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    nombre: str
    estado: EstadoEventoEnum
    tipo: TipoEventoEnum
    realizacion: Realizacion
    organizador: List[Organizador]
    organizacion: List[Organizacion] = Field(default_factory=list)
    capacidad: int

    class Settings:
        name = "evento"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )