from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.repositories.sqlalchemy import SqlAlchemyHarvestRepository
from sini.schemas.harvest import HarvestCreate, HarvestResponse, HarvestUpdate
from sini.services.exceptions import EntityNotFoundError
from sini.services.harvest_service import HarvestService

router = APIRouter(
    prefix="/harvests",
    tags=["Harvests"],
)


SessionDep = Annotated[
    Session,
    Depends(get_session),
]


def get_harvest_service(
    session: SessionDep,
) -> HarvestService:
    """Crée un HarvestService avec le repository PostgreSQL."""

    repository = SqlAlchemyHarvestRepository(session)

    return HarvestService(repository)


HarvestServiceDep = Annotated[
    HarvestService,
    Depends(get_harvest_service),
]


@router.post(
    "",
    response_model=HarvestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_harvest(
    data: HarvestCreate,
    service: HarvestServiceDep,
) -> HarvestResponse:
    """Crée une nouvelle récolte."""

    return service.create(data)


@router.get(
    "",
    response_model=list[HarvestResponse],
)
def get_all_harvests(
    service: HarvestServiceDep,
) -> list[HarvestResponse]:
    """Récupère toutes les récoltes."""

    return service.get_all()


@router.get(
    "/{harvest_id}",
    response_model=HarvestResponse,
)
def get_harvest(
    harvest_id: int,
    service: HarvestServiceDep,
) -> HarvestResponse:
    """Récupère une récolte par son ID."""

    try:
        return service.get_by_id(harvest_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{harvest_id}",
    response_model=HarvestResponse,
)
def update_harvest(
    harvest_id: int,
    data: HarvestUpdate,
    service: HarvestServiceDep,
) -> HarvestResponse:
    """Met à jour une récolte."""

    try:
        return service.update(harvest_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{harvest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_harvest(
    harvest_id: int,
    service: HarvestServiceDep,
) -> Response:
    """Supprime une récolte."""

    try:
        service.delete(harvest_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
