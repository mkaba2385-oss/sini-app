import pytest
from sini.repositories.memory import InMemoryParcelleRepository
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway
from sini.services.weather import MockWeatherProvider

@pytest.fixture
def parcelle_service() -> ParcelleService:
    return ParcelleService(
        repository=InMemoryParcelleRepository(),
        weather_provider=MockWeatherProvider(),
        sms_gateway=ConsoleSmsGateway(),
    )