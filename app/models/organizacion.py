from beanie import Document
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from app.schemas.common import PyObjectId


class Ubicacion(BaseModel): 
    direccion: str
    ciudad: str


class OrganizacionModel(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombre: str
    representanteLegal: str
    ubicacion: Ubicacion
    sectorEconomico: str
    actividadPrincipal: str
    telefonos: List[str]

    class Settings:
        name = "organizacion"  # ✅ coincide con tu colección real

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True
    )


