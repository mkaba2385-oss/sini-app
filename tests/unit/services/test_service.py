from unittest.mock import MagicMock
from datetime import datetime, timezone
import pytest

from sini.repositories.base import RepositoryInterface
from sini.schemas.parcelle import (
    CultureType,
    ParcelleCreate,
    ParcelleResponse,
    ParcelleUpdate,
    RegionMali,
)
from sini.services.exceptions import EntityNotFoundError
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import SmsGateway
from sini.services.weather import MeteoData, WeatherProvider


@pytest.fixture
def mock_repo() -> MagicMock:
    return MagicMock(spec=RepositoryInterface)


@pytest.fixture
def mock_weather() -> MagicMock:
    return MagicMock(spec=WeatherProvider)


@pytest.fixture
def mock_sms() -> MagicMock:
    return MagicMock(spec=SmsGateway)


@pytest.fixture
def service(mock_repo: MagicMock, mock_weather: MagicMock, mock_sms: MagicMock) -> ParcelleService:
    return ParcelleService(
        repository=mock_repo,
        weather_provider=mock_weather,
        sms_gateway=mock_sms,
    )


def test_create_parcelle(service: ParcelleService, mock_repo: MagicMock) -> None:
    mock_repo.get_next_id.return_value = 1
    mock_repo.add.side_effect = lambda parcelle: parcelle

    data = ParcelleCreate(
        name="Champ Ségou",
        superficie_ha=5.0,
        culture=CultureType.COTON,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=2,
    )

    result = service.create_parcelle(data)

    assert result.id == 1
    assert result.name == "Champ Ségou"
    mock_repo.get_next_id.assert_called_once()
    mock_repo.add.assert_called_once()


def test_get_by_id_raises_exception_when_not_found(service: ParcelleService, mock_repo: MagicMock) -> None:
    mock_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundError):
        service.get_by_id(99)


def test_verifier_et_alerter_triggers_sms_on_drought(
    service: ParcelleService,
    mock_repo: MagicMock,
    mock_weather: MagicMock,
    mock_sms: MagicMock,
) -> None:
    parcelle = ParcelleResponse(
        id=1,
        name="Parcelle Test",
        superficie_ha=2.0,
        culture=CultureType.MAIS,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=1,
        created_at=datetime.now(timezone.utc),
    )
    mock_repo.get_by_id.return_value = parcelle

    # Simulation météo sécheresse
    mock_weather.get_meteo.return_value = MeteoData(
        temperature=40.0,
        humidite=15.0,
        alerte_secheresse=True,
    )

    service.verifier_et_alerter(parcelle_id=1, telephone_owner="+22370000000")

    mock_weather.get_meteo.assert_called_once_with("Ségou")
    mock_sms.send_sms.assert_called_once()


def test_verifier_et_alerter_does_not_trigger_sms_when_no_drought(
    service: ParcelleService,
    mock_repo: MagicMock,
    mock_weather: MagicMock,
    mock_sms: MagicMock,
) -> None:
    parcelle = ParcelleResponse(
        id=1,
        name="Parcelle Test",
        superficie_ha=2.0,
        culture=CultureType.MAIS,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=1,
        created_at=datetime.now(timezone.utc),
    )
    mock_repo.get_by_id.return_value = parcelle

    # Simulation météo normale
    mock_weather.get_meteo.return_value = MeteoData(
        temperature=28.0,
        humidite=60.0,
        alerte_secheresse=False,
    )

    service.verifier_et_alerter(parcelle_id=1, telephone_owner="+22370000000")

    mock_sms.send_sms.assert_not_called()