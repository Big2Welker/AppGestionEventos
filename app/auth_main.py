from app.common_app import create_service_app
from app.api.v1.routes.auth_routes import router as auth_router

app = create_service_app(
    title="Auth Service",
    routers=[auth_router]
)