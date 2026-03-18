from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.v1.api import api_router_v1
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Conexión a Mongo antes de aceptar requests
    print("🔌 Conectando a MongoDB...")
    await connect_to_mongo()
    print("✅ Beanie inicializado correctamente.")
    yield
    # ✅ Cierre limpio al apagar servidor
    await close_mongo_connection()
    print("🔒 Conexión Mongo cerrada.")


app = FastAPI(
    title=settings.APP_NAME,
    description="Una API para gestionar Eventos de un sistema académico.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router_v1, prefix="/api/v1")

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
