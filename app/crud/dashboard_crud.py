from app.models.eventos import EventoModel
from app.schemas.dashboard_schema import (
    EventoEstadoStats,
    EventoTipoStats,
    TotalEventos
)


# eventos por estado
async def eventos_por_estado():

    pipeline = [
        {
            "$group": {
                "_id": "$estado",
                "total": {"$sum": 1}
            }
        }
    ]

    resultados = await EventoModel.aggregate(pipeline).to_list()

    return [
        EventoEstadoStats(
            estado=r["_id"],
            total=r["total"]
        )
        for r in resultados
    ]


# eventos por tipo
async def eventos_por_tipo():

    pipeline = [
        {
            "$group": {
                "_id": "$tipo",
                "total": {"$sum": 1}
            }
        }
    ]

    resultados = await EventoModel.aggregate(pipeline).to_list()

    return [
        EventoTipoStats(
            tipo=r["_id"],
            total=r["total"]
        )
        for r in resultados
    ]


# total eventos
async def total_eventos():

    total = await EventoModel.find_all().count()

    return TotalEventos(total_eventos=total)