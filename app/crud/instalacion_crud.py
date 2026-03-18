from app.models.instalacion import InstalacionModel
from app.models.eventos import EventoModel

async def listar_instalaciones():
    return await InstalacionModel.find_all().to_list()

async def obtener_ocupacion_instalaciones():
    instalaciones = await InstalacionModel.find_all().to_list()
    eventos = await EventoModel.find_all().to_list()

    resultado = []

    for instalacion in instalaciones:
        eventos_ocupando = []

        for evento in eventos:
            for inst in evento.realizacion.instalaciones:
                if inst.instalacionId == instalacion.id:
                    eventos_ocupando.append({
                        "nombre": evento.nombre,
                        "fecha": evento.realizacion.fecha,
                        "horaInicio": evento.realizacion.horaInicio,
                        "horaFin": evento.realizacion.horaFin,
                        "capacidadUsada": inst.capacidadInstalacion
                    })

        resultado.append({
            "instalacionId": instalacion.id,
            "ubicacion": instalacion.ubicacion,
            "tipo": instalacion.tipo,
            "capacidad": instalacion.capacidad,
            "eventos": eventos_ocupando
        })

    return resultado