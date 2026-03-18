from fastapi import APIRouter, Depends, status
from typing import List

from app.core.dependencies import get_current_user
from app.crud.evento_crud import (
    actualizar_evento_por_rol,
    crear_evento,
    listar_eventos,
    listar_eventos_por_rol,
    obtener_evento,
    actualizar_evento,
    eliminar_evento,
    eliminar_evento_por_rol
)
from app.schemas.evento_schema import EventoCreate, EventoUpdate, EventoResponse

router = APIRouter(prefix="/eventos", tags=["Eventos"])


# ✅ Crear evento
@router.post("/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
async def crear(data: EventoCreate, user=Depends(get_current_user)):
    user_id = int(user["user_id"])
    rol = user["rol"]
    return await crear_evento(data, user_id, rol)

@router.get("/", response_model=List[EventoResponse])
async def listar(user=Depends(get_current_user)):
    user_id = int(user["user_id"])
    rol = user["rol"]

    return await listar_eventos_por_rol(user_id, rol)


# ✅ Obtener evento por ID
@router.get("/{id}", response_model=EventoResponse)
async def obtener(id: str):
    return await obtener_evento(id)


# ✅ Actualizar evento según rol
@router.put("/{id}", response_model=EventoResponse)
async def actualizar(id: str, data: EventoUpdate, user=Depends(get_current_user)):
    user_id = int(user["user_id"])
    rol = user["rol"]

    return await actualizar_evento_por_rol(id, data, user_id, rol)


# ✅ Eliminar evento
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar(id: str, user=Depends(get_current_user)):
    user_id = int(user["user_id"])
    rol = user["rol"]
    return await eliminar_evento_por_rol(id, user_id, rol)