from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔌 Conectando a MongoDB...")
    await connect_to_mongo()
    print("✅ Beanie inicializado correctamente.")
    yield
    await close_mongo_connection()
    print("🔒 Conexión Mongo cerrada.")


def create_service_app(title: str, routers: list):
    app = FastAPI(
        title=title,
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://GestorEventos.com",
            "http://192.168.100.10",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in routers:
        app.include_router(router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"service": title, "status": "ok"}

    return app