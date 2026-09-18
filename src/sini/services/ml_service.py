import httpx

from sini.config import ML_SERVICE_URL


async def predict_image(
    image_bytes: bytes,
    filename: str,
) -> dict:
    """Envoie une image au service ML et retourne la prédiction."""

    files = {
        "file": (
            filename,
            image_bytes,
        ),
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{ML_SERVICE_URL}/predict",
            files=files,
        )

    response.raise_for_status()

    return response.json()