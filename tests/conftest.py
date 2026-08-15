import pytest

from sini.factories.service_factory import ServiceFactory
from sini.services.parcelle_service import ParcelleService


@pytest.fixture
def parcelle_service() -> ParcelleService:
    return ServiceFactory.create_parcelle_service(env="dev")
