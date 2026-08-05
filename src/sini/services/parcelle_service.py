from datetime import datetime, timezone
from typing import Iterator

from sini.schemas.parcelle import (
    ParcelleCreate,
    ParcelleResponse,
    ParcelleUpdate,
    CultureType,
    RegionMali,
)
from sini.repositories.base import RepositoryInterface
from sini.services.exceptions import EntityNotFoundError
from sini.services.sms import SmsGateway
from sini.services.weather import WeatherProvider
from sini.services.utils import timer


class ParcelleService:
    """Service métier appliquant les principes SOLID à 100%."""

    def __init__(
        self,
        repository: RepositoryInterface[ParcelleResponse],
        weather_provider: WeatherProvider,
        sms_gateway: SmsGateway,
    ) -> None:
        self.repo = repository
        self.weather = weather_provider
        self.sms = sms_gateway

    @timer
    def create_parcelle(self, data: ParcelleCreate) -> ParcelleResponse:
        parcelle_id = self.repo.get_next_id()
        now = datetime.now(timezone.utc)

        parcelle = ParcelleResponse(
            id=parcelle_id,
            created_at=now,
            update_at=None,  # <-- Corrigé (aligné sur ParcelleResponse.update_at)
            **data.model_dump(),
        )
        return self.repo.add(parcelle)

    @timer
    def get_by_id(self, parcelle_id: int) -> ParcelleResponse:
        parcelle = self.repo.get_by_id(parcelle_id)
        if not parcelle:
            raise EntityNotFoundError("Parcelle", parcelle_id)
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
            p for p in self.repo.get_all()
            if (owner_id is None or p.owner_id == owner_id)
            and (region is None or p.region == region)
            and (culture is None or p.culture == culture)
        ]

    @timer
    def updated_parcelle(self, parcelle_id: int, data: ParcelleUpdate) -> ParcelleResponse:
        current = self.get_by_id(parcelle_id)
        updated_data = data.model_dump(exclude_unset=True)
        if not updated_data:
            return current

        updated_dict = current.model_dump()
        updated_dict.update(updated_data)
        updated_dict["update_at"] = datetime.now(timezone.utc)  # <-- Corrigé

        updated_parcelle = ParcelleResponse(**updated_dict)
        return self.repo.add(updated_parcelle)

    @timer
    def delete_parcelle(self, parcelle_id: int) -> None:
        self.get_by_id(parcelle_id)  # Lève EntityNotFoundError si introuvable
        self.repo.delete(parcelle_id)

    def verifier_et_alerter(self, parcelle_id: int, telephone_owner: str) -> None:
        parcelle = self.get_by_id(parcelle_id)
        meteo = self.weather.get_meteo(parcelle.region.value)

        if meteo.alerte_secheresse:
            msg = (
                f"Alerte sécheresse sur la parcelle {parcelle.name} ({parcelle.region.value}) ! "
                f"Température : {meteo.temperature}°C."
            )
            self.sms.send_sms(telephone_owner, msg)