from pydantic import BaseModel


class EventoEstadoStats(BaseModel):
    estado: str
    total: int


class EventoTipoStats(BaseModel):
    tipo: str
    total: int


class TotalEventos(BaseModel):
    total_eventos: int