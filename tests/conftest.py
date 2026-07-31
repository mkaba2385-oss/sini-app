import pytest
from sini.services import ParcelleService

@pytest.fixture
def parcelle_service() -> ParcelleService:
    """Fixture injectant un service vierge pour chaque test."""
    service = ParcelleService()
    service.clear()
    return service 