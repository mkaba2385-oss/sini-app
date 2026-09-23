import httpx
from pydantic import BaseModel

from sini.config import ML_SERVICE_URL


class PredictionResponse(BaseModel):
    classe: str
    confiance: float


async def predict_image(
    image_bytes: bytes,
    filename: str,
) -> PredictionResponse:
    """Envoie une image au service ML et retourne la prédiction."""

    files = {
        "file": (
            filename,
            image_bytes,
        ),
    }

    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{ML_SERVICE_URL}/predict",
            files=files,
        )

    response.raise_for_status()

    return PredictionResponse.model_validate(response.json())