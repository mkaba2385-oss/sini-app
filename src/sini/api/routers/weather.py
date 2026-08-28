from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sini.config import OPENWEATHER_API_KEY
from sini.providers.openweather import OpenWeatherMapProvider
from sini.schemas.user import RegionMali
from sini.services.weather import MeteoData, WeatherProvider

router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


def get_weather_provider() -> WeatherProvider:
    """Retourne le provider météo configuré."""

    if OPENWEATHER_API_KEY is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="La clé OpenWeather n'est pas configurée.",
        )

    return OpenWeatherMapProvider(
        api_key=OPENWEATHER_API_KEY,
    )


WeatherProviderDep = Annotated[
    WeatherProvider,
    Depends(get_weather_provider),
]


@router.get(
    "",
    response_model=MeteoData,
)
def get_weather(
    region: RegionMali,
    weather_provider: WeatherProviderDep,
) -> MeteoData:
    """Récupère la météo actuelle d'une région du Mali."""

    return weather_provider.get_meteo(
        region.value,
    )
