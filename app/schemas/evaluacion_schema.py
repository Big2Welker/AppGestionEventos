from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from app.models.evaluaciones import EstadoEvaluacionEnum
from app.schemas.common import PyObjectId


# 🧩 Esquema para creación
class EvaluacionCrear(BaseModel):
    estado: EstadoEvaluacionEnum
    fechaEvaluacion: datetime
    justificacion: Optional[str] = None
    actaAprovacion: Optional[bytes] = None
    eventoId: PyObjectId
    usuarioId: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


# 🧱 Esquema base común (para heredar)
class EvaluacionBase(BaseModel):
    estado: EstadoEvaluacionEnum
    fechaEvaluacion: datetime
    justificacion: Optional[str] = None
    actaAprovacion: Optional[bytes] = None
    eventoId: PyObjectId
    usuarioId: int

    model_config = ConfigDict(arbitrary_types_allowed=True)


# ✏️ Esquema para actualización parcial
class EvaluacionActualizar(BaseModel):
    estado: Optional[EstadoEvaluacionEnum] = None
    fechaEvaluacion: Optional[datetime] = None
    justificacion: Optional[str] = None
    actaAprovacion: Optional[bytes] = None
    eventoId: Optional[PyObjectId] = None
    usuarioId: Optional[int] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


# 📤 Esquema para salida / lectura
class Evaluacion(EvaluacionBase):
    id: PyObjectId = Field(..., alias="_id", description="ID único de la evaluación")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
