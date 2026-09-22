from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.set import SetResponse

# Campos base de una carta
class CardBase(BaseModel):
    name: str
    mana_cost: Optional[str] = None
    type_line: str
    rarity: str
    power: Optional[str] = None
    toughness: Optional[str] = None

# Esquema para crear una carta
class CardCreate(CardBase):
    set_id: int

# Esquema para actualizar una carta
class CardUpdate(BaseModel):
    name: Optional[str] = None
    mana_cost: Optional[str] = None
    type_line: Optional[str] = None
    rarity: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None
    set_id: Optional[int] = None

# Esquema de respuesta completo con relación anidada
class CardResponse(CardBase):
    id: int
    set_id: int
    set: Optional[SetResponse] = None

    model_config = ConfigDict(from_attributes=True)