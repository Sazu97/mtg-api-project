from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Campos base compartidos
class SetBase(BaseModel):
    code: str
    name: str
    release_date: Optional[date] = None

# Esquema para crear un Set
class SetCreate(SetBase):
    pass

# Esquema para actualizar un Set
class SetUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    release_date: Optional[date] = None

# Esquema de respuesta
class SetResponse(SetBase):
    id: int

    model_config = ConfigDict(from_attributes=True)