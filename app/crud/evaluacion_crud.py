from typing import List
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId
from app.models.eventos import EventoModel, EstadoEventoEnum
from app.models.evaluaciones import EstadoEvaluacionEnum, EvaluacionModel
from app.schemas.evaluacion_schema import (
    EvaluacionCrear,
    EvaluacionActualizar,
    Evaluacion
)
from app.models.usuarios import UsuarioModel, RolUsuarioEnum, EstadoVinculacionEnum


# ✅ Crear evaluación
async def crear_evaluacion(data: EvaluacionCrear) -> Evaluacion:
    # Verificar que el usuario exista
    usuario = await UsuarioModel.find_one(UsuarioModel.id == data.usuarioId)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {data.usuarioId} no encontrado"
        )

    # Verificar que el usuario tenga rol activo de secretaria académica
    roles_activos = [
        v.rol for v in usuario.vinculacion
        if v.estado == EstadoVinculacionEnum.ACTIVO
    ]

    if RolUsuarioEnum.SECRETARIA not in roles_activos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo una secretaria académica puede realizar una evaluación"
        )

    # Verificar que el evento exista
    try:
        evento = await EventoModel.get(PydanticObjectId(str(data.eventoId)))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="eventoId no es válido"
        )

    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )

    # Convertir eventoId a ObjectId
    data_dict = data.model_dump(exclude_none=True)
    if "eventoId" in data_dict and isinstance(data_dict["eventoId"], str):
        data_dict["eventoId"] = ObjectId(data_dict["eventoId"])

    evaluacion = EvaluacionModel(**data_dict)
    await evaluacion.insert()

    # ✅ Actualizar estado del evento según la evaluación
    if data.estado == EstadoEvaluacionEnum.APROBADO:
        evento.estado = EstadoEventoEnum.APROVADO
    elif data.estado == EstadoEvaluacionEnum.RECHAZADO:
        evento.estado = EstadoEventoEnum.EN_REVISION

    await evento.save()

    return evaluacion

# ✅ Listar todas las evaluaciones
async def listar_evaluaciones() -> List[Evaluacion]:
    return await EvaluacionModel.find_all().to_list()


# ✅ Obtener evaluación por ID
async def obtener_evaluacion(id: str) -> Evaluacion:
    try:
        evaluacion = await EvaluacionModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID enviado no es un ObjectId válido"
        )

    if not evaluacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada"
        )

    return evaluacion


# ✅ Actualizar evaluación
async def actualizar_evaluacion(id: str, data: EvaluacionActualizar) -> Evaluacion:
    try:
        evaluacion = await EvaluacionModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID enviado no es un ObjectId válido"
        )

    if not evaluacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada"
        )

    actualizaciones = data.model_dump(exclude_unset=True, exclude_none=True)
    
    # ⚠️ Convertir eventoId a ObjectId si viene en string
    if "eventoId" in actualizaciones and isinstance(actualizaciones["eventoId"], str):
        actualizaciones["eventoId"] = ObjectId(actualizaciones["eventoId"])

    await evaluacion.set(actualizaciones)
    return evaluacion


# ✅ Eliminar evaluación
async def eliminar_evaluacion(id: str):
    try:
        evaluacion = await EvaluacionModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID enviado no es un ObjectId válido"
        )

    if not evaluacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evaluación no encontrada"
        )

    await evaluacion.delete()
    return {"mensaje": "Evaluación eliminada correctamente"}
