from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class MeteoData(BaseModel):
    temperature: float
    humidite: float = Field(..., ge=0, le=100)
    pluie_mm: float = Field(default=0.0, ge=0)
    vent_kmh: float = Field(default=0.0, ge=0)
    alerte_secheresse: bool = False


class WeatherProvider(ABC):
    @abstractmethod
    def get_meteo(self, region: str) -> MeteoData:
        pass


class MockWeatherProvider(WeatherProvider):
    def get_meteo(self, region: str) -> MeteoData:
        # Données de simulation
        return MeteoData(temperature=38.5, humidite=20.0, alerte_secheresse=True)
