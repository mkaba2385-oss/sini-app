from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from sini.api.dependencies import CurrentUserDep
from sini.db.session import get_session
from sini.repositories.sqlalchemy import (
    SqlAlchemyHarvestRepository,
    SqlAlchemyParcelleRepository,
)
from sini.schemas.harvest import (
    HarvestCreate,
    HarvestResponse,
    HarvestUpdate,
)
from sini.services.exceptions import (
    EntityNotFoundError,
    UnauthorizedAccessError,
)
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
    """Crée un HarvestService avec ses repositories."""

    harvest_repository = SqlAlchemyHarvestRepository(session)
    parcelle_repository = SqlAlchemyParcelleRepository(session)

    return HarvestService(
        repository=harvest_repository,
        parcelle_repository=parcelle_repository,
    )


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
    current_user: CurrentUserDep,
) -> HarvestResponse:
    """Crée une nouvelle récolte."""

    try:
        return service.create(
            data,
            current_user.id,
        )
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnauthorizedAccessError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[HarvestResponse],
)
def get_all_harvests(
    service: HarvestServiceDep,
    current_user: CurrentUserDep,
) -> list[HarvestResponse]:
    """Récupère uniquement les récoltes de l'utilisateur connecté."""

    return service.get_all(
        current_user.id,
    )


@router.get(
    "/{harvest_id}",
    response_model=HarvestResponse,
)
def get_harvest(
    harvest_id: int,
    service: HarvestServiceDep,
    current_user: CurrentUserDep,
) -> HarvestResponse:
    """Récupère une récolte par son ID."""

    try:
        return service.get_by_id(
            harvest_id,
            current_user.id,
        )
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnauthorizedAccessError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
    current_user: CurrentUserDep,
) -> HarvestResponse:
    """Met à jour une récolte."""

    try:
        return service.update(
            harvest_id,
            data,
            current_user.id,
        )
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnauthorizedAccessError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{harvest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_harvest(
    harvest_id: int,
    service: HarvestServiceDep,
    current_user: CurrentUserDep,
) -> Response:
    """Supprime une récolte."""

    try:
        service.delete(
            harvest_id,
            current_user.id,
        )
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnauthorizedAccessError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
