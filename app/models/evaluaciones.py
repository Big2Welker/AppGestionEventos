from beanie import Document
from pydantic import Field, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
from app.schemas.common import PyObjectId


class EstadoEvaluacionEnum(str, Enum):
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class EvaluacionModel(Document):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    estado: EstadoEvaluacionEnum
    fechaEvaluacion: datetime
    justificacion: str = ""
    actaAprovacion: bytes = b""
    eventoId: PyObjectId
    usuarioId: int 

    class Settings:
        name = "evaluacion"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True
    )
