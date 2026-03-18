from app.common_app import create_service_app
from app.api.v1.routes.evaluacion_routes import router as evaluacion_router

app = create_service_app(
    title="Evaluaciones Service",
    routers=[evaluacion_router]
)