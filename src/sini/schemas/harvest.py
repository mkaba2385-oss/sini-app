from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class HarvestBase(BaseModel):
    parcelle_id: int
    season_id: int
    quantite_recoltee: float = Field(..., gt=0)
    unite: str = Field(..., min_length=1, max_length=20)
    date_recolte: date


class HarvestCreate(HarvestBase):
    pass


class HarvestUpdate(BaseModel):
    season_id: int | None = None
    quantite_recoltee: float | None = Field(
        default=None,
        gt=0,
    )
    unite: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    date_recolte: date | None = None


class HarvestResponse(HarvestBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
