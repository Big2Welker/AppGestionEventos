from app.models.usuarios import UsuarioModel


async def authenticate_user(email: str, password: str):

    # Buscar usuario por email
    usuario = await UsuarioModel.find_one(UsuarioModel.email == email)

    if not usuario:
        return None

    # Obtener la última contraseña registrada
    if not usuario.password:
        return None

    password_guardada = usuario.password[-1].clave

    # Comparar contraseña
    if password != password_guardada:
        return None

    return usuario