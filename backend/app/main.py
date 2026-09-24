from fastapi import FastAPI
from backend.app.core.database import engine, Base
from backend.app.routes import sets, card

# Crea las tablas en SQLite si aún no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MTG Collection API",
    version="1.0.0"
)

# Conectar las rutas de Sets y Cards a la aplicación
app.include_router(sets.router, prefix="/sets", tags=["Sets"])
app.include_router(card.router, prefix="/cards", tags=["Cards"])

@app.get("/")
def root():
    return {"message": "MTG Collection API funcionando correctamente"}