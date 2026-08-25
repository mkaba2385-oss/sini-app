from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.repositories.sqlalchemy import SqlAlchemySeasonRepository
from sini.schemas.season import SeasonCreate, SeasonResponse, SeasonUpdate
from sini.services.exceptions import EntityNotFoundError
from sini.services.season_service import SeasonService

router = APIRouter(
    prefix="/seasons",
    tags=["Seasons"],
)


SessionDep = Annotated[
    Session,
    Depends(get_session),
]


def get_season_service(
    session: SessionDep,
) -> SeasonService:
    """Crée un SeasonService avec le repository PostgreSQL."""

    repository = SqlAlchemySeasonRepository(session)

    return SeasonService(repository)


SeasonServiceDep = Annotated[
    SeasonService,
    Depends(get_season_service),
]


@router.post(
    "",
    response_model=SeasonResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_season(
    data: SeasonCreate,
    service: SeasonServiceDep,
) -> SeasonResponse:
    """Crée une nouvelle saison."""

    return service.create(data)


@router.get(
    "",
    response_model=list[SeasonResponse],
)
def get_all_seasons(
    service: SeasonServiceDep,
) -> list[SeasonResponse]:
    """Récupère toutes les saisons."""

    return service.get_all()


@router.get(
    "/{season_id}",
    response_model=SeasonResponse,
)
def get_season(
    season_id: int,
    service: SeasonServiceDep,
) -> SeasonResponse:
    """Récupère une saison par son ID."""

    try:
        return service.get_by_id(season_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{season_id}",
    response_model=SeasonResponse,
)
def update_season(
    season_id: int,
    data: SeasonUpdate,
    service: SeasonServiceDep,
) -> SeasonResponse:
    """Met à jour une saison."""

    try:
        return service.update(season_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{season_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_season(
    season_id: int,
    service: SeasonServiceDep,
) -> Response:
    """Supprime une saison."""

    try:
        service.delete(season_id)

    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Impossible de supprimer cette saison "
                "car des récoltes y sont associées."
            ),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
