import pytest

from sini.factories.service_factory import ServiceFactory
from sini.observers.base import Event, Observer
from sini.schemas.parcelle import (
    CultureType,
    ParcelleCreate,
    ParcelleResponse,
    ParcelleUpdate,
    RegionMali,
)
from sini.services.exceptions import EntityNotFoundError
from sini.services.parcelle_service import ParcelleService
from sini.strategies.alert_strategy import HighTemperatureAlertStrategy


@pytest.fixture
def service() -> ParcelleService:
    return ServiceFactory.create_parcelle_service(env="dev")


def test_create_parcelle_success(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="Champ Nord",
        superficie_ha=2.5,
        culture=CultureType.MAIS,
        region=RegionMali.SIKASSO,
        commune="Sikasso",
        owner_id=1,
    )

    parcelle = service.create_parcelle(payload)

    assert isinstance(parcelle, ParcelleResponse)
    assert parcelle.name == "Champ Nord"
    assert parcelle.superficie_ha == 2.5
    assert parcelle.id is not None


def test_get_parcelle_by_id_success(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="Champ Sud",
        superficie_ha=1.8,
        culture=CultureType.COTON,
        region=RegionMali.SIKASSO,
        commune="Sikasso",
        owner_id=1,
    )
    created = service.create_parcelle(payload)
    retrieved = service.get_by_id(created.id)

    assert retrieved.id == created.id
    assert retrieved.name == "Champ Sud"


def test_get_parcelle_not_found_raises_exception(service: ParcelleService) -> None:
    with pytest.raises(EntityNotFoundError):
        service.get_by_id(9999)


def test_list_and_filter_parcelles(service: ParcelleService) -> None:
    p1 = ParcelleCreate(
        name="P1",
        superficie_ha=1.0,
        culture=CultureType.RIZ,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=1,
    )
    p2 = ParcelleCreate(
        name="P2",
        superficie_ha=2.0,
        culture=CultureType.MIL,
        region=RegionMali.MOPTI,
        commune="Mopti",
        owner_id=2,
    )

    service.create_parcelle(p1)
    service.create_parcelle(p2)

    assert len(service.get_all()) == 2
    assert len(service.filter_parcelles(owner_id=1)) == 1
    assert len(list(service.stream_by_owner(1))) == 1


def test_update_parcelle_success(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="Champ Test",
        superficie_ha=1.0,
        culture=CultureType.RIZ,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=1,
    )
    created = service.create_parcelle(payload)

    updated = service.updated_parcelle(
        created.id,
        ParcelleUpdate(name="Champ Modifié", superficie_ha=2.0),
    )
    assert updated.name == "Champ Modifié"
    assert updated.updated_at is not None


def test_update_parcelle_no_change(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="Inchangé",
        superficie_ha=1.0,
        culture=CultureType.RIZ,
        region=RegionMali.SEGOU,
        owner_id=1,
    )
    created = service.create_parcelle(payload)
    same = service.updated_parcelle(created.id, ParcelleUpdate())
    assert same.name == "Inchangé"


def test_delete_parcelle_success(service: ParcelleService) -> None:
    payload = ParcelleCreate(
        name="À Supprimer",
        superficie_ha=1.0,
        culture=CultureType.MAIS,
        region=RegionMali.SIKASSO,
        commune="Sikasso",
        owner_id=1,
    )
    created = service.create_parcelle(payload)
    service.delete_parcelle(created.id)

    with pytest.raises(EntityNotFoundError):
        service.get_by_id(created.id)


def test_update_and_delete_not_found(service: ParcelleService) -> None:
    with pytest.raises(EntityNotFoundError):
        service.updated_parcelle(999, ParcelleUpdate(name="Parcelle Inexistante"))

    with pytest.raises(EntityNotFoundError):
        service.delete_parcelle(999)


def test_verifier_et_alerter_observer_and_strategy(service: ParcelleService) -> None:
    """Teste l'alerte météo et la notification via Observer."""
    created = service.create_parcelle(
        ParcelleCreate(
            name="Champ Alerte",
            superficie_ha=3.0,
            culture=CultureType.MAIS,
            region=RegionMali.SEGOU,
            owner_id=1,
        )
    )

    events_received: list[Event] = []

    class MockObserver(Observer):
        def update(self, event: Event) -> None:
            events_received.append(event)

    mock_obs = MockObserver()
    service.publisher.attach(mock_obs)

    service.verifier_et_alerter(created.id, "+22370000000")

    assert len(events_received) == 1
    assert events_received[0].name == "ALERT_TRIGGERED"
    assert events_received[0].payload["telephone"] == "+22370000000"

    service.publisher.detach(mock_obs)
    service.verifier_et_alerter(created.id, "+22370000000")
    assert len(events_received) == 1


def test_custom_strategy_no_alert(service: ParcelleService) -> None:
    """Vérifie qu'aucune alerte n'est émise."""
    service.alert_strategy = HighTemperatureAlertStrategy(temp_threshold=50.0)
    created = service.create_parcelle(
        ParcelleCreate(
            name="Champ Calme",
            superficie_ha=1.0,
            culture=CultureType.MIL,
            region=RegionMali.SEGOU,
            owner_id=1,
        )
    )

    events_received: list[Event] = []

    class MockObserver(Observer):
        def update(self, event: Event) -> None:
            events_received.append(event)

    service.publisher.attach(MockObserver())
    service.verifier_et_alerter(created.id, "+22370000000")

    assert len(events_received) == 0
