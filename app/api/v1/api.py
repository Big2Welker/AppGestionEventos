from fastapi import APIRouter
from app.api.v1.routes import (
    auth_routes,
    evento_routes,
    evaluacion_routes,
    instalacion_routes,
    usuarios_routes,
    dashboard_routes
)

api_router_v1 = APIRouter()

api_router_v1.include_router(auth_routes.router)
api_router_v1.include_router(evento_routes.router)
api_router_v1.include_router(evaluacion_routes.router)
api_router_v1.include_router(instalacion_routes.router)
api_router_v1.include_router(usuarios_routes.router)
api_router_v1.include_router(dashboard_routes.router)