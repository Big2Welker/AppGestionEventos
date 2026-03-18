from beanie import Document
from pydantic import Field, ConfigDict
from enum import Enum
from typing import Optional


class TipoInstalacionEnum(str, Enum):
    SALON = "salon"
    AUDITORIO = "auditorio"
    LABORATORIO = "laboratorio"
    CANCHA = "cancha"


class InstalacionModel(Document):
    id: Optional[str] = Field(alias="_id")
    ubicacion: str
    tipo: TipoInstalacionEnum
    capacidad: int

    class Settings:
        name = "instalacion"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        populate_by_name=True
    )
