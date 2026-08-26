from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PhotoBase(BaseModel):
    """Champs communs d'une photo associée à une parcelle."""

    parcelle_id: int
    url: str = Field(..., min_length=1, max_length=500)
    caption: str | None = Field(default=None, max_length=300)
    taken_at: datetime | None = None


class PhotoCreate(PhotoBase):
    """Données nécessaires à l'ajout d'une photo."""


class PhotoUpdate(BaseModel):
    """Champs modifiables d'une photo."""

    url: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    caption: str | None = Field(
        default=None,
        max_length=300,
    )
    taken_at: datetime | None = None


class PhotoResponse(PhotoBase):
    """Représentation d'une photo renvoyée par l'application."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


PhotoOut = PhotoResponse
