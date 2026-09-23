from typing import Annotated, TypedDict

from fastapi import APIRouter, File, UploadFile

from sini.api.dependencies import CurrentUserDep
from sini.services.ml_service import predict_image
from sini.services.plant_diseases import PLANT_DISEASES

router = APIRouter(
    prefix="/plant-diagnosis",
    tags=["Plant Diagnosis"],
)


class PlantDiagnosisResponse(TypedDict):
    maladie: str
    confiance: float
    traitement: str


@router.post("/predict")
async def predict_plant(
    file: Annotated[UploadFile, File(...)],
    current_user: CurrentUserDep,
) -> PlantDiagnosisResponse:
    """Analyse une photo de plante avec le modèle ML."""

    image_bytes = await file.read()

    prediction = await predict_image(
        image_bytes=image_bytes,
        filename=file.filename or "plant.jpg",
    )

    classe = prediction.classe
    confidence = prediction.confiance

    disease_info = PLANT_DISEASES.get(
        classe,
        {
            "maladie": classe,
            "traitement": "Aucune recommandation disponible.",
        },
    )

    return {
        "maladie": disease_info["maladie"],
        "confiance": confidence,
        "traitement": disease_info["traitement"],
    }