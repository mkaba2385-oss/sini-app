from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.observers.base import EventPublisher
from sini.observers.sms_observer import SmsNotificationObserver
from sini.repositories.sqlalchemy import SqlAlchemyParcelleRepository
from sini.schemas.parcelle import (
    CultureType,
    ParcelleCreate,
    ParcelleResponse,
    ParcelleUpdate,
)
from sini.schemas.user import RegionMali
from sini.services.exceptions import EntityNotFoundError
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway
from sini.services.weather import MockWeatherProvider
from sini.strategies.alert_strategy import DroughtAlertStrategy

router = APIRouter(
    prefix="/parcelles",
    tags=["Parcelles"],
)

SessionDep = Annotated[Session, Depends(get_session)]


def get_parcelle_service(
    session: SessionDep,
) -> ParcelleService:
    """Crée un ParcelleService avec ses dépendances."""

    repository = SqlAlchemyParcelleRepository(session)

    weather = MockWeatherProvider()
    sms = ConsoleSmsGateway()

    publisher = EventPublisher()
    sms_observer = SmsNotificationObserver(
        sms_gateway=sms,
    )
    publisher.attach(sms_observer)

    return ParcelleService(
        repository=repository,
        weather_provider=weather,
        publisher=publisher,
        alert_strategy=DroughtAlertStrategy(),
    )


ParcelleServiceDep = Annotated[
    ParcelleService,
    Depends(get_parcelle_service),
]


@router.post(
    "",
    response_model=ParcelleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_parcelle(
    data: ParcelleCreate,
    service: ParcelleServiceDep,
) -> ParcelleResponse:
    """Crée une nouvelle parcelle."""

    try:
        return service.create_parcelle(data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{parcelle_id}",
    response_model=ParcelleResponse,
)
def get_parcelle(
    parcelle_id: int,
    service: ParcelleServiceDep,
) -> ParcelleResponse:
    """Récupère une parcelle par son ID."""

    try:
        return service.get_by_id(parcelle_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ParcelleResponse],
)
def get_all_parcelles(
    service: ParcelleServiceDep,
    owner_id: int | None = None,
    region: RegionMali | None = None,
    culture: CultureType | None = None,
) -> list[ParcelleResponse]:
    """Récupère les parcelles avec filtres optionnels."""

    if owner_id is None and region is None and culture is None:
        return service.get_all()

    return service.filter_parcelles(
        owner_id=owner_id,
        region=region,
        culture=culture,
    )


@router.patch(
    "/{parcelle_id}",
    response_model=ParcelleResponse,
)
def update_parcelle(
    parcelle_id: int,
    data: ParcelleUpdate,
    service: ParcelleServiceDep,
) -> ParcelleResponse:
    """Met à jour une parcelle."""

    try:
        return service.updated_parcelle(
            parcelle_id,
            data,
        )
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{parcelle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_parcelle(
    parcelle_id: int,
    service: ParcelleServiceDep,
) -> None:
    """Supprime une parcelle."""

    try:
        service.delete_parcelle(parcelle_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
