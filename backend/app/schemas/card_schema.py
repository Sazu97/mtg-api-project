from pydantic import BaseModel, ConfigDict, Field, field_validator
from backend.app.schemas.set_schema import SetResponse


class CardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    mana_cost: str | None = Field(default=None, max_length=30)
    type_line: str = Field(..., min_length=1, max_length=150)
    rarity: str = Field(..., min_length=1, max_length=20)
    power: str | None = Field(default=None, max_length=10)
    toughness: str | None = Field(default=None, max_length=10)

    @field_validator("name", "type_line", "rarity")
    @classmethod
    def ensure_not_blank(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Este campo no puede estar compuesto únicamente de espacios.")
        return cleaned


class CardCreate(CardBase):
    set_id: int = Field(..., gt=0, description="ID de la colección a la que pertenece")


class CardUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    mana_cost: str | None = Field(default=None, max_length=30)
    type_line: str | None = Field(default=None, min_length=1, max_length=150)
    rarity: str | None = Field(default=None, min_length=1, max_length=20)
    power: str | None = Field(default=None, max_length=10)
    toughness: str | None = Field(default=None, max_length=10)
    set_id: int | None = Field(default=None, gt=0)


class CardResponse(CardBase):
    id: int
    set_id: int
    set: SetResponse | None = None

    model_config = ConfigDict(from_attributes=True)