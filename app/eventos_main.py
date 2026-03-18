from app.common_app import create_service_app
from app.api.v1.routes.evento_routes import router as evento_router
from app.api.v1.routes.dashboard_routes import router as dashboard_router

app = create_service_app(
    title="Eventos Service",
    routers=[evento_router, dashboard_router]
)