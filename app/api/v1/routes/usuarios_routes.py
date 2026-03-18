from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user
from app.crud.usuario_crud import crear_usuario, listar_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear(data: UsuarioCreate, user=Depends(get_current_user)):
    rol = user["rol"]

    if rol != "secretariaAcademica":
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="Solo una secretaria académica puede crear usuarios"
        )

    return await crear_usuario(data)


@router.get("/", response_model=list[UsuarioResponse])
async def listar():
    return await listar_usuarios()


@router.get("/{id}", response_model=UsuarioResponse)
async def obtener(id: int):
    return await obtener_usuario(id)


@router.put("/{id}", response_model=UsuarioResponse)
async def actualizar(id: int, data: UsuarioUpdate):
    return await actualizar_usuario(id, data)


@router.delete("/{id}")
async def eliminar(id: int):
    return await eliminar_usuario(id)