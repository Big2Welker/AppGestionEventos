from typing import List
from fastapi import HTTPException, status
from app.models.usuarios import UsuarioModel
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from bson import ObjectId


def limpiar_none_recursivo(valor):
    if isinstance(valor, dict):
        return {
            k: limpiar_none_recursivo(v)
            for k, v in valor.items()
            if v is not None
        }
    elif isinstance(valor, list):
        return [limpiar_none_recursivo(v) for v in valor]
    return valor


async def crear_usuario(data: UsuarioCreate):
    data_dict = data.model_dump(by_alias=True, exclude_none=True)

    # Convertir IDs de vinculacion a ObjectId si vienen como string
    for vinc in data_dict.get("vinculacion", []):
        if "programaId" in vinc and isinstance(vinc["programaId"], str):
            vinc["programaId"] = ObjectId(vinc["programaId"])
        if "unidadId" in vinc and isinstance(vinc["unidadId"], str):
            vinc["unidadId"] = ObjectId(vinc["unidadId"])
        if "facultadId" in vinc and isinstance(vinc["facultadId"], str):
            vinc["facultadId"] = ObjectId(vinc["facultadId"])

    data_dict = limpiar_none_recursivo(data_dict)

    # Insertar directamente limpio
    await UsuarioModel.get_motor_collection().insert_one(data_dict)

    usuario = await UsuarioModel.get(data_dict["_id"])
    return UsuarioResponse(**usuario.model_dump(by_alias=True))

# Listar usuarios
async def listar_usuarios() -> List[UsuarioResponse]:

    usuarios = await UsuarioModel.find_all().to_list()

    return [UsuarioResponse(**u.model_dump()) for u in usuarios]


# Obtener usuario
async def obtener_usuario(id: int) -> UsuarioResponse:

    usuario = await UsuarioModel.get(id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return UsuarioResponse(**usuario.model_dump())


# Actualizar usuario
async def actualizar_usuario(id: int, data: UsuarioUpdate) -> UsuarioResponse:

    usuario = await UsuarioModel.get(id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    actualizaciones = data.model_dump(exclude_unset=True)

    await usuario.set(actualizaciones)

    return UsuarioResponse(**usuario.model_dump())


# Eliminar usuario
async def eliminar_usuario(id: int):

    usuario = await UsuarioModel.get(id)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    await usuario.delete()

    return {"mensaje": "Usuario eliminado"}