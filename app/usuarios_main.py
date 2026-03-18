from app.common_app import create_service_app
from app.api.v1.routes.usuarios_routes import router as usuarios_router

app = create_service_app(
    title="Usuarios Service",
    routers=[usuarios_router]
)