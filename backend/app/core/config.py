import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
load_dotenv()

APP_TITLE: str = os.getenv("APP_TITLE", "MTG Collection API")
APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "API de gestion de cartas MTG")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mtg.db")