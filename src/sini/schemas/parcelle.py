from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .user import RegionMali


class CultureType(str, Enum):
    COTON = "Coton"
    MAIS = "Maïs"
    RIZ = "Riz"
    MIL = "Mil"
    SORGHO = "Sorgho"
    ARACHIDE = "Arachide"
    MARAICHAGE = "Maraîchage"
    AUTRE = "Autre"


class ParcelleBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, examples=["Champ Ségou Nord"])
    superficie_ha: float = Field(
        ..., gt=0, description="Superficie en hectares (ex: 2.5)"
    )
    culture: CultureType = Field(..., examples=[CultureType.MAIS])
    region: RegionMali = Field(..., examples=[RegionMali.SEGOU])
    commune: str | None = Field(default=None, max_length=100, examples=["Pelengana"])


class ParcelleCreate(ParcelleBase):
    pass


class ParcelleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    superficie_ha: float | None = Field(default=None, gt=0)
    culture: CultureType | None = None
    region: RegionMali | None = None
    commune: str | None = None


class ParcelleResponse(ParcelleBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
