from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from backend.app.core.database import engine, Base
from backend.app.routes import sets, cards


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida (Lifespan).
    Crea las tablas en SQLite automáticamente al arrancar la aplicación.
    """
    Base.metadata.create_all(bind=engine)
    yield


# Inicialización de la aplicación FastAPI
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers con sus prefijos y tags
app.include_router(sets.router, prefix="/sets", tags=["Sets"])
app.include_router(cards.router, prefix="/cards", tags=["Cards"])


@app.get("/", tags=["Health Check"])
def read_root():
    """
    Ruta raíz para verificar que el servidor está online.
    """
    return {
        "status": "online",
        "message": f"Welcome to {APP_TITLE}",
        "version": APP_VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }