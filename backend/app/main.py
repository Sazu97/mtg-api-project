from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.database import engine, Base
from backend.app.core.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION
from backend.app.routes import sets, card

# Crea las tablas en SQLite si aún no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar las rutas
app.include_router(sets.router, prefix="/sets", tags=["Sets"])
app.include_router(card.router, prefix="/cards", tags=["Cards"])


@app.get("/")
def root():
    return {
        "status": "online",
        "title": APP_TITLE,
        "version": APP_VERSION,
        "docs_url": "/docs"
    }