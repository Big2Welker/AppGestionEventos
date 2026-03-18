from typing import List
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from bson import ObjectId

from app.models.eventos import EventoModel
from app.models.usuarios import UsuarioModel, RolUsuarioEnum, EstadoVinculacionEnum
from app.schemas.evento_schema import EventoCreate, EventoUpdate, EventoResponse


# ✅ Validar capacidad total de las instalaciones
async def validar_capacidad_evento(evento_data: EventoCreate | EventoUpdate):
    total_capacidad_instalaciones = sum(
        i.capacidadInstalacion for i in evento_data.realizacion.instalaciones
    )
    if evento_data.capacidad > total_capacidad_instalaciones:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La capacidad del evento ({evento_data.capacidad}) supera la capacidad total de las instalaciones ({total_capacidad_instalaciones})."
        )

# ✅ Validar que el organizador principal sea el usuario logueado
def validar_organizador_principal(evento_data: EventoCreate, user_id: int):
    if not evento_data.organizador or len(evento_data.organizador) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe existir al menos un organizador."
        )

    organizador_principal = evento_data.organizador[0]

    if organizador_principal.tipo != "principal":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El primer organizador debe ser principal."
        )

    if organizador_principal.usuarioId != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes crear un evento usando otro usuario como organizador principal."
        )


# ✅ Validar que los organizadores sean estudiantes o docentes
async def validar_organizadores(evento_data: EventoCreate | EventoUpdate):
    for organizador in evento_data.organizador:
        usuario = await UsuarioModel.find_one(UsuarioModel.id == organizador.usuarioId)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {organizador.usuarioId} no encontrado."
            )

        roles_activos = [
            v.rol for v in usuario.vinculacion
            if v.estado == EstadoVinculacionEnum.ACTIVO
        ]

        # ❌ Si tiene rol de secretaria activa → no puede organizar
        if RolUsuarioEnum.SECRETARIA in roles_activos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario {usuario.nombre} {usuario.apellidos} no puede organizar eventos (rol: secretaria académica)."
            )

        # ✅ Solo estudiante o docente pueden organizar
        if not any(r in [RolUsuarioEnum.ESTUDIANTE, RolUsuarioEnum.DOCENTE] for r in roles_activos):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario {usuario.nombre} {usuario.apellidos} debe ser estudiante o docente para organizar eventos."
            )


# ✅ Validar que las instalaciones no estén ocupadas
async def validar_disponibilidad_instalaciones(evento_data: EventoCreate | EventoUpdate, evento_id: str | None = None):
    fecha_nueva = evento_data.realizacion.fecha
    inicio_nuevo = evento_data.realizacion.horaInicio
    fin_nuevo = evento_data.realizacion.horaFin
    instalaciones_nuevas = [i.instalacionId for i in evento_data.realizacion.instalaciones]

    if not (inicio_nuevo and fin_nuevo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe especificar hora de inicio y hora de fin para el evento."
        )

    eventos_mismo_dia = await EventoModel.find({"realizacion.fecha": fecha_nueva}).to_list()

    for evento in eventos_mismo_dia:
        if evento_id and str(evento.id) == evento_id:
            continue

        for instalacion in evento.realizacion.instalaciones:
            if instalacion.instalacionId in instalaciones_nuevas:
                if (
                    (inicio_nuevo < evento.realizacion.horaFin)
                    and (fin_nuevo > evento.realizacion.horaInicio)
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"La instalación {instalacion.instalacionId} está ocupada el {fecha_nueva.strftime('%Y-%m-%d')} entre {evento.realizacion.horaInicio} y {evento.realizacion.horaFin}."
                    )


# 🔹 Utilidad: convertir IDs de organización a ObjectId
def convertir_ids_organizacion(data_dict: dict):
    organizaciones = data_dict.get("organizacion")

    if not organizaciones:
        return

    for org in organizaciones:
        if isinstance(org.get("organizacionId"), str):
            try:
                org["organizacionId"] = ObjectId(org["organizacionId"])
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"organizacionId '{org['organizacionId']}' no es un ObjectId válido."
                )


# ✅ Verificar si un usuario puede editar un evento
async def verificar_permiso_edicion(id: str, user_id: int, rol: str) -> EventoModel:
    try:
        evento = await EventoModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )

    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )
    
    if evento.estado == "aprovado":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El evento ya fue aprobado y no puede ser editado."
        )

    # Docente puede editar cualquier evento
    if rol == "docente":
        return evento

    # Estudiante solo puede editar eventos donde sea organizador
    if rol == "estudiante":
        es_organizador = any(org.usuarioId == user_id for org in evento.organizador)

        if not es_organizador:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para editar este evento"
            )

        return evento

    # Secretaría no puede editar eventos
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para editar eventos"
    )

# ✅ Crear evento
async def crear_evento(data: EventoCreate, user_id: int, rol: str) -> EventoResponse:
    validar_organizador_principal(data, user_id)
    await validar_capacidad_evento(data)
    await validar_organizadores(data)
    await validar_disponibilidad_instalaciones(data)

    data_dict = data.model_dump(exclude_none=True)
    convertir_ids_organizacion(data_dict)

    evento = EventoModel(**data_dict)
    await evento.insert()
    return EventoResponse(**evento.model_dump())



# ✅ Listar eventos
async def listar_eventos() -> List[EventoResponse]:
    eventos = await EventoModel.find_all().to_list()
    return [EventoResponse(**e.model_dump()) for e in eventos]

# ✅ Listar eventos según rol
async def listar_eventos_por_rol(user_id: int, rol: str) -> List[EventoResponse]:
    if rol == "estudiante":
        eventos = await EventoModel.find({
            "$or": [
                {"organizador.usuarioId": user_id},
                {"estado": "aprovado"}
            ]
        }).to_list()
    else:
        eventos = await EventoModel.find_all().to_list()

    return [EventoResponse(**e.model_dump()) for e in eventos]


# ✅ Obtener evento por ID
async def obtener_evento(id: str) -> EventoResponse:
    try:
        evento = await EventoModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")

    return EventoResponse(**evento.model_dump())


# ✅ Actualizar evento con control por rol
async def actualizar_evento_por_rol(id: str, data: EventoUpdate, user_id: int, rol: str) -> EventoResponse:
    evento = await verificar_permiso_edicion(id, user_id, rol)

    await validar_capacidad_evento(data)
    await validar_organizadores(data)
    await validar_disponibilidad_instalaciones(data, evento_id=id)

    actualizaciones = data.model_dump(exclude_unset=True, exclude_none=True)
    convertir_ids_organizacion(actualizaciones)

    await evento.set(actualizaciones)
    return EventoResponse(**evento.model_dump())


# ✅ Actualizar evento
async def actualizar_evento(id: str, data: EventoUpdate) -> EventoResponse:
    try:
        evento = await EventoModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")

    await validar_capacidad_evento(data)
    await validar_organizadores(data)
    await validar_disponibilidad_instalaciones(data, evento_id=id)

    actualizaciones = data.model_dump(exclude_unset=True, exclude_none=True)
    convertir_ids_organizacion(actualizaciones)

    await evento.set(actualizaciones)
    return EventoResponse(**evento.model_dump())

# ✅ Eliminar evento
async def eliminar_evento(id: str):
    try:
        evento = await EventoModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")

    if evento.estado == "aprovado":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El evento ya fue aprobado y no puede ser eliminado."
        )

    await evento.delete()
    return {"mensaje": "Evento eliminado correctamente"}

# Verificar si un usuario puede eliminar un evento
async def verificar_permiso_eliminacion(id: str, user_id: int, rol: str) -> EventoModel:
    try:
        evento = await EventoModel.get(PydanticObjectId(id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID inválido"
        )

    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )

    # Si el evento ya fue aprobado, no se puede eliminar
    if evento.estado == "aprovado":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El evento ya fue aprobado y no puede ser eliminado."
        )

    # Solo estudiante o docente pueden eliminar, si son organizador principal
    if rol in ["estudiante", "docente"]:
        organizador_principal = None

        for org in evento.organizador:
            if org.tipo == "principal":
                organizador_principal = org
                break

        if not organizador_principal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El evento no tiene organizador principal definido."
            )

        if organizador_principal.usuarioId != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo el organizador principal puede eliminar este evento."
            )

        return evento

    # Secretaría no puede eliminar
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para eliminar eventos."
    )

# Eliminar evento con control por rol
async def eliminar_evento_por_rol(id: str, user_id: int, rol: str):
    evento = await verificar_permiso_eliminacion(id, user_id, rol)
    await evento.delete()
    return {"mensaje": "Evento eliminado correctamente"}