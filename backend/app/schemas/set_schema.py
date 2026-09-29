from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator


class SetBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=10, description="Código de la colección (ej. BLB, LTR)")
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la colección")
    release_date: date | None = Field(default=None, description="Fecha de lanzamiento")

    @field_validator("code")
    @classmethod
    def code_to_uppercase(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("El nombre no puede estar vacío.")
        return cleaned


class SetCreate(SetBase):
    pass


class SetUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=2, max_length=10)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    release_date: date | None = None

    @field_validator("code")
    @classmethod
    def code_to_uppercase(cls, v: str | None) -> str | None:
        return v.strip().upper() if v else None


class SetResponse(SetBase):
    id: int

    model_config = ConfigDict(from_attributes=True)