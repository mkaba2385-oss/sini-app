import pytest
from sini.factories.service_factory import ServiceFactory
from sini.observers.base import EventPublisher
from sini.repositories.memory import InMemoryParcelleRepository
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway  
from sini.services.weather import MockWeatherProvider


@pytest.fixture
def parcelle_service() -> ParcelleService:
    return ServiceFactory.create_parcelle_service(env="dev")  