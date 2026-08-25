from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.repositories.sqlalchemy import SqlAlchemyJournalRepository
from sini.schemas.journal import (
    JournalEntryCreate,
    JournalEntryResponse,
    JournalEntryUpdate,
)
from sini.services.exceptions import EntityNotFoundError
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

    repository = SqlAlchemyJournalRepository(session)

    return JournalService(repository)


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
) -> JournalEntryResponse:
    """Ajoute une entrée au journal agricole."""

    return service.add_entry(data)


@router.get(
    "/parcelle/{parcelle_id}",
    response_model=list[JournalEntryResponse],
)
def get_journal_by_parcelle(
    parcelle_id: int,
    service: JournalServiceDep,
) -> list[JournalEntryResponse]:
    """Récupère toutes les entrées du journal d'une parcelle."""

    return service.list_by_parcelle(parcelle_id)


@router.get(
    "/parcelle/{parcelle_id}/stats",
)
def get_journal_stats(
    parcelle_id: int,
    service: JournalServiceDep,
) -> dict[str, object]:
    """Retourne les statistiques du journal d'une parcelle."""

    return service.stats(parcelle_id)


@router.patch(
    "/{entry_id}",
    response_model=JournalEntryResponse,
)
def update_journal_entry(
    entry_id: int,
    data: JournalEntryUpdate,
    service: JournalServiceDep,
) -> JournalEntryResponse:
    """Met à jour une entrée du journal."""

    try:
        return service.update(entry_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_journal_entry(
    entry_id: int,
    service: JournalServiceDep,
) -> Response:
    """Supprime une entrée du journal."""

    try:
        service.delete(entry_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
