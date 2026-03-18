from beanie import Document
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.schemas.common import PyObjectId

class UnidadAcademica(BaseModel):
    unidadId: PyObjectId = Field(default_factory=PyObjectId)
    nombre: str

class Programa(BaseModel):
    programaId: PyObjectId = Field(default_factory=PyObjectId)
    nombre: str

class FacultadModel(Document):
    nombre: str
    unidadAcademica: List[UnidadAcademica] = []
    programa: List[Programa] = []

    class Settings:
        name = "facultad"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )
