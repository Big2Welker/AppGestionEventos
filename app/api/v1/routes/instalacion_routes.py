from fastapi import APIRouter
from app.crud.instalacion_crud import listar_instalaciones, obtener_ocupacion_instalaciones

router = APIRouter(prefix="/instalaciones", tags=["Instalaciones"])

@router.get("/ocupacion")
async def get_ocupacion_instalaciones():
    return await obtener_ocupacion_instalaciones()

@router.get("/")
async def listar_instalaciones_endpoint():
    return await listar_instalaciones()