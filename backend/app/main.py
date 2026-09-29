from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de configuración y motor de base de datos
from backend.app.core.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from backend.app.core.database import engine, Base

# Importación de los módulos de rutas refactorizados
from backend.app.routes import set_routes, card_routes


# ==============================================================================
# 1. GESTOR DE CICLO DE VIDA (LIFESPAN)
# ==============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se ejecuta al iniciar el servidor antes de aceptar peticiones HTTP.
    Crea automáticamente las tablas en SQLite si todavía no existen.
    """
    Base.metadata.create_all(bind=engine)
    yield


# ==============================================================================
# 2. INICIALIZACIÓN DE LA INSTANCIA PRINCIPAL DE FASTAPI
# ==============================================================================
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan
)


# ==============================================================================
# 3. MIDDLEWARE DE CORS (Cross-Origin Resource Sharing)
# ==============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,   
    allow_methods=["*"],       
    allow_headers=["*"],       
)


# ==============================================================================
# 4. REGISTRO Y MONTAJE DE ROUTERS
# ==============================================================================
app.include_router(set_routes.router, prefix="/sets", tags=["Sets"])

app.include_router(card_routes.router, prefix="/cards", tags=["Cards"])


# ==============================================================================
# 5. RUTA RAÍZ / HEALTH CHECK
# ==============================================================================
@app.get("/", tags=["Health Check"])
def read_root():
    """
    Ruta de comprobación rápida para verificar que el servidor está online
    y proporcionar enlaces directos a la documentación interactiva.
    """
    return {
        "status": "online",
        "message": f"Welcome to {APP_TITLE}",
        "version": APP_VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }