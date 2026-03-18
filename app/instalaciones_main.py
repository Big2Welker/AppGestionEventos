from app.common_app import create_service_app
from app.api.v1.routes.instalacion_routes import router as instalacion_router

app = create_service_app(
    title="Instalaciones Service",
    routers=[instalacion_router]
)