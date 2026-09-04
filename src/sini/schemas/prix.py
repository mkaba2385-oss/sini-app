from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .parcelle import CultureType


class UnitePrix(str, Enum):
    KG = "kg"
    SAC = "sac"
    TONNE = "tonne"
    PANIER = "panier"


class PrixBase(BaseModel):
    culture: CultureType = Field(..., examples=[CultureType.MAIS])

    variete: str | None = Field(
        default=None,
        max_length=100,
        examples=["Gambiaka"],
    )

    type_prix: str = Field(
        ...,
        min_length=2,
        max_length=50,
        examples=["detaillant"],
    )

    marche: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Marché de Ségou"],
    )

    prix_moyen: float = Field(
        ...,
        gt=0,
        description="Prix moyen en FCFA (doit être > 0)",
        examples=[250.0],
    )

    unite: UnitePrix = Field(
        default=UnitePrix.KG,
        examples=[UnitePrix.KG],
    )

    date_releve: date = Field(
        ...,
        examples=["2026-08-01"],
    )

    source: str = Field(
        ...,
        min_length=2,
        max_length=255,
        examples=["OMA"],
    )

    @field_validator("date_releve")
    @classmethod
    def validate_date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError(
                "La date de relevé du prix ne peut pas être dans le futur."
            )
        return v


class PrixCreate(PrixBase):
    pass


class PrixUpdate(BaseModel):
    culture: CultureType | None = None

    variete: str | None = Field(
        default=None,
        max_length=100,
    )

    type_prix: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    marche: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    prix_moyen: float | None = Field(
        default=None,
        gt=0,
    )

    unite: UnitePrix | None = None

    date_releve: date | None = None

    source: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    @field_validator("date_releve")
    @classmethod
    def validate_date_not_future(cls, v: date | None) -> date | None:
        if v is not None and v > date.today():
            raise ValueError(
                "La date de relevé du prix ne peut pas être dans le futur."
            )
        return v


class PrixResponse(PrixBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)