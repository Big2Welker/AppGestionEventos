from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import LoginSchema
from app.crud.auth_crud import authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(data: LoginSchema):

    usuario = await authenticate_user(data.email, data.password)

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    rol = usuario.vinculacion[0].rol

    token = create_access_token({
        "user_id": usuario.id,
        "rol": rol
    })

    return {
        "access_token": token,
        "rol": rol,
        "user_id": usuario.id,
        "nombre": usuario.nombre,
        "apellidos": usuario.apellidos,
        "email": usuario.email
    }