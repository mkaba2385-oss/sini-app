from datetime import datetime, timezone
from typing import Iterator

from sini.observers.base import Event, EventPublisher
from sini.repositories.base import RepositoryInterface
from sini.schemas.parcelle import (
    CultureType,
    ParcelleCreate,
    ParcelleResponse,
    ParcelleUpdate,
)
from sini.schemas.user import RegionMali
from sini.services.exceptions import EntityNotFoundError, PermissionDeniedError
from sini.services.utils import timer
from sini.services.weather import WeatherProvider
from sini.strategies.alert_strategy import AlertStrategy, DroughtAlertStrategy


class ParcelleService:
    """Service métier appliquant les principes SOLID, Strategy et Observer."""

    def __init__(
        self,
        repository: RepositoryInterface[ParcelleResponse],
        weather_provider: WeatherProvider,
        publisher: EventPublisher,
        alert_strategy: AlertStrategy | None = None,
    ) -> None:
        self.repo = repository
        self.weather = weather_provider
        self.publisher = publisher
        self.alert_strategy = alert_strategy or DroughtAlertStrategy()

    @timer
    def create_parcelle(
        self,
        data: ParcelleCreate,
        owner_id: int,
    ) -> ParcelleResponse:
        now = datetime.now(timezone.utc)

        parcelle = ParcelleResponse(
            id=0,
            owner_id=owner_id,
            created_at=now,
            updated_at=None,
            **data.model_dump(),
        )

        created = self.repo.create(parcelle)

        self.publisher.notify(
            Event(
                name="PARCELLE_CREATED",
                payload={"parcelle": created},
            )
        )

        return created

    @timer
    def get_by_id(self, parcelle_id: int) -> ParcelleResponse:
        parcelle = self.repo.get_by_id(parcelle_id)
        if not parcelle:
            raise EntityNotFoundError("Parcelle", parcelle_id)
        return parcelle

    def get_owned_parcelle(
        self,
        parcelle_id: int,
        user_id: int,
    ) -> ParcelleResponse:
        """Récupère une parcelle si elle appartient à l'utilisateur."""

        parcelle = self.get_by_id(parcelle_id)

        if parcelle.owner_id != user_id:
            raise PermissionDeniedError()

        return parcelle

    @timer
    def get_all(self) -> list[ParcelleResponse]:
        return self.repo.get_all()

    def stream_by_owner(self, owner_id: int) -> Iterator[ParcelleResponse]:
        for parcelle in self.repo.get_all():
            if parcelle.owner_id == owner_id:
                yield parcelle

    @timer
    def filter_parcelles(
        self,
        owner_id: int | None = None,
        region: RegionMali | None = None,
        culture: CultureType | None = None,
    ) -> list[ParcelleResponse]:
        return [
            p
            for p in self.repo.get_all()
            if (owner_id is None or p.owner_id == owner_id)
            and (region is None or p.region == region)
            and (culture is None or p.culture == culture)
        ]

    @timer
    def updated_parcelle(
        self, parcelle_id: int, data: ParcelleUpdate
    ) -> ParcelleResponse:
        current = self.get_by_id(parcelle_id)
        updated_data = data.model_dump(exclude_unset=True)
        if not updated_data:
            return current

        updated_dict = current.model_dump()
        updated_dict.update(updated_data)
        updated_dict["updated_at"] = datetime.now(timezone.utc)

        updated_parcelle = ParcelleResponse(**updated_dict)
        return self.repo.add(updated_parcelle)

    @timer
    def delete_parcelle(self, parcelle_id: int) -> None:
        self.get_by_id(parcelle_id)
        self.repo.delete(parcelle_id)

    def verifier_et_alerter(self, parcelle_id: int, telephone_owner: str) -> None:
        parcelle = self.get_by_id(parcelle_id)
        region_val = (
            parcelle.region.value
            if hasattr(parcelle.region, "value")
            else str(parcelle.region)
        )
        meteo = self.weather.get_meteo(region_val)

        if self.alert_strategy.should_alert(parcelle, meteo):
            msg = self.alert_strategy.build_message(parcelle, meteo)
            self.publisher.notify(
                Event(
                    name="ALERT_TRIGGERED",
                    payload={
                        "telephone": telephone_owner,
                        "message": msg,
                        "parcelle": parcelle,
                    },
                )
            )
