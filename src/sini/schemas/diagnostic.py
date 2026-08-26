from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SeverityLevel(str, Enum):
    LOW = "Faible"
    MEDIUM = "Moyen"
    HIGH = "Élevé"
    CRITICAL = "Critique"


class PredictionItem(BaseModel):
    maladie: str = Field(..., examples=["Helminthosporiose"])
    probabilite: float = Field(..., ge=0.0, le=1.0, examples=[0.85])


class DiagnosticBase(BaseModel):
    parcelle_id: int
    symptomes_observes: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        examples=["Feuilles jaunies avec taches brunes"],
    )
    pathologie_detectee: str | None = Field(
        default=None, examples=["Helminthosporiose du maïs"]
    )
    niveau_severite: SeverityLevel = SeverityLevel.MEDIUM
    recommandations: str = Field(
        ..., examples=["Appliquer un fongicide homologué et réduire l'humidité."]
    )
    score_confiance: float = Field(
        ..., ge=0.0, le=1.0, description="Confiance du modèle IA (0 à 1)"
    )
    predictions: list[PredictionItem] | dict[str, float] | None = Field(
        default=None, description="Détail des prédictions brutes fournies par l'IA"
    )


class DiagnosticCreate(DiagnosticBase):
    pass


class DiagnosticUpdate(BaseModel):
    symptomes_observes: str | None = Field(
        default=None,
        min_length=5,
        max_length=1000,
    )
    pathologie_detectee: str | None = None
    niveau_severite: SeverityLevel | None = None
    recommandations: str | None = None
    score_confiance: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    predictions: list[PredictionItem] | dict[str, float] | None = None


class DiagnosticResponse(DiagnosticBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
