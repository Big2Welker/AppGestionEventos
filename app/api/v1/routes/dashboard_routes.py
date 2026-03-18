from fastapi import APIRouter

from app.crud.dashboard_crud import (
    eventos_por_estado,
    eventos_por_tipo,
    total_eventos
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/eventos-estado")
async def dashboard_estado():
    return await eventos_por_estado()


@router.get("/eventos-tipo")
async def dashboard_tipo():
    return await eventos_por_tipo()


@router.get("/total-eventos")
async def dashboard_total():
    return await total_eventos()