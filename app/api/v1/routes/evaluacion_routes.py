from fastapi import APIRouter, status
from typing import List

from app.schemas.evaluacion_schema import (
    EvaluacionCrear,
    EvaluacionActualizar,
    Evaluacion
)
from app.crud.evaluacion_crud import (
    crear_evaluacion,
    listar_evaluaciones,
    obtener_evaluacion,
    actualizar_evaluacion,
    eliminar_evaluacion
)

router = APIRouter(
    prefix="/evaluaciones",
    tags=["Evaluaciones"]
)

# ✅ Crear evaluación
@router.post(
    "/",
    response_model=Evaluacion,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva evaluación",
    description="Crea una evaluación asociada a un evento y un usuario evaluador."
)
async def crear_evaluacion_endpoint(data: EvaluacionCrear):
    return await crear_evaluacion(data)


# ✅ Listar todas las evaluaciones
@router.get(
    "/",
    response_model=List[Evaluacion],
    summary="Listar todas las evaluaciones",
    description="Devuelve todas las evaluaciones registradas en el sistema."
)
async def listar_evaluaciones_endpoint():
    return await listar_evaluaciones()


# ✅ Obtener evaluación por ID
@router.get(
    "/{id}",
    response_model=Evaluacion,
    summary="Obtener una evaluación por ID",
    description="Devuelve los detalles de una evaluación específica según su ID."
)
async def obtener_evaluacion_endpoint(id: str):
    return await obtener_evaluacion(id)


# ✅ Actualizar evaluación
@router.put(
    "/{id}",
    response_model=Evaluacion,
    summary="Actualizar una evaluación",
    description="Permite modificar los campos de una evaluación existente."
)
async def actualizar_evaluacion_endpoint(id: str, data: EvaluacionActualizar):
    return await actualizar_evaluacion(id, data)


# ✅ Eliminar evaluación
@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar una evaluación",
    description="Elimina una evaluación existente del sistema."
)
async def eliminar_evaluacion_endpoint(id: str):
    return await eliminar_evaluacion(id)
