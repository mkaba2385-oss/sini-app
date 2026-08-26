from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ActionType(str, Enum):
    SEMIS = "Semis"
    IRRIGATION = "Irrigation"
    FERTILISATION = "Fertilisation"
    TRAITEMENT = "Traitement phytosanitaire"
    DESHERBAGE = "Désherbage"
    RECOLTE = "Récolte"
    OBSERVATION = "Observation"


class JournalEntryBase(BaseModel):
    parcelle_id: int
    action_type: ActionType
    title: str = Field(
        ..., min_length=3, max_length=150, examples=["Apport d'engrais NPK"]
    )
    description: str | None = Field(default=None, max_length=1000)
    cout_fcfa: float = Field(default=0.0, ge=0.0, description="Coût associé en FCFA")


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryUpdate(BaseModel):
    action_type: ActionType | None = None
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
    )
    cout_fcfa: float | None = Field(
        default=None,
        ge=0.0,
    )


class JournalEntryResponse(JournalEntryBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
