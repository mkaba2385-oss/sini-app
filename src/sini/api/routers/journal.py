from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from sini.api.dependencies import CurrentUserDep
from sini.db.session import get_session
from sini.repositories.sqlalchemy import (
    SqlAlchemyJournalRepository,
    SqlAlchemyParcelleRepository,
)
from sini.schemas.journal import (
    JournalEntryCreate,
    JournalEntryResponse,
    JournalEntryUpdate,
)
from sini.services.exceptions import EntityNotFoundError, UnauthorizedAccessError
from sini.services.journal_service import JournalService

router = APIRouter(
    prefix="/journal",
    tags=["Journal"],
)

SessionDep = Annotated[Session, Depends(get_session)]


def get_journal_service(
    session: SessionDep,
) -> JournalService:
    """Crée un JournalService avec le repository PostgreSQL."""

    journal_repository = SqlAlchemyJournalRepository(session)
    parcelle_repository = SqlAlchemyParcelleRepository(session)

    return JournalService(
        repository=journal_repository,
        parcelle_repository=parcelle_repository,
    )


JournalServiceDep = Annotated[
    JournalService,
    Depends(get_journal_service),
]


@router.post(
    "",
    response_model=JournalEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_journal_entry(
    data: JournalEntryCreate,
    service: JournalServiceDep,
    current_user: CurrentUserDep,
) -> JournalEntryResponse:
    """Ajoute une entrée au journal agricole."""

    try:
        return service.add_entry(
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
    "/parcelle/{parcelle_id}",
    response_model=list[JournalEntryResponse],
)
def get_journal_by_parcelle(
    parcelle_id: int,
    service: JournalServiceDep,
    current_user: CurrentUserDep,
) -> list[JournalEntryResponse]:
    """Récupère toutes les entrées du journal d'une parcelle."""

    try:
        return service.list_by_parcelle(
            parcelle_id,
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
    "/parcelle/{parcelle_id}/stats",
)
def get_journal_stats(
    parcelle_id: int,
    service: JournalServiceDep,
    current_user: CurrentUserDep,
) -> dict[str, object]:
    """Retourne les statistiques du journal d'une parcelle."""

    try:
        return service.stats(
            parcelle_id,
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
    "/{entry_id}",
    response_model=JournalEntryResponse,
)
def update_journal_entry(
    entry_id: int,
    data: JournalEntryUpdate,
    service: JournalServiceDep,
    current_user: CurrentUserDep,
) -> JournalEntryResponse:
    """Met à jour une entrée du journal."""

    try:
        return service.update(
            entry_id,
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
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_journal_entry(
    entry_id: int,
    service: JournalServiceDep,
    current_user: CurrentUserDep,
) -> Response:
    """Supprime une entrée du journal."""

    try:
        service.delete(
            entry_id,
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
