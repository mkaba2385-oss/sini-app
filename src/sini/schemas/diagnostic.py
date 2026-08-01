from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SeverityLevel(str, Enum):
    LOW = "Faible"
    MEDIUM = "Moyen"
    HIGH = "Élevé"
    CRITICAL = "Critique"

class DiagnosticBase(BaseModel):
    parcelle_id: int 
    symptomes_observes: str = Field(..., min_length=5, max_length=1000, examples=["Feuilles jaunies avec taches brunes"])
    pathologie_detectee: str | None = Field(default=None, examples=["Helminthosporiose du maïs "])
    niveau_severite: SeverityLevel = SeverityLevel.MEDIUM
    recommandations: str = Field(..., examples=["Appliquer un fongicide homologué et réduire l'humidité."])
    score_confiance: float = Field(..., ge=0.0, le=1.0, description="Confiance du modèle IA (0 à 1)")

class DiagnosticCreate(DiagnosticBase):
    pass

class DiagnosticResponse(DiagnosticBase):
    id: int 
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    