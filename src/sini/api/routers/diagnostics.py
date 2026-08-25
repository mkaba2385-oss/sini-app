from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.repositories.sqlalchemy import SqlAlchemyDiagnosticRepository
from sini.schemas.diagnostic import (
    DiagnosticCreate,
    DiagnosticResponse,
    DiagnosticUpdate,
)
from sini.services.diagnostic_service import DiagnosticService
from sini.services.exceptions import EntityNotFoundError

router = APIRouter(
    prefix="/diagnostics",
    tags=["Diagnostics"],
)


SessionDep = Annotated[
    Session,
    Depends(get_session),
]


def get_diagnostic_service(
    session: SessionDep,
) -> DiagnosticService:
    """Crée un DiagnosticService avec le repository PostgreSQL."""

    repository = SqlAlchemyDiagnosticRepository(session)

    return DiagnosticService(repository)


DiagnosticServiceDep = Annotated[
    DiagnosticService,
    Depends(get_diagnostic_service),
]


@router.post(
    "",
    response_model=DiagnosticResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_diagnostic(
    data: DiagnosticCreate,
    service: DiagnosticServiceDep,
) -> DiagnosticResponse:
    """Crée un nouveau diagnostic."""

    try:
        return service.create(data)

    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[DiagnosticResponse],
)
def get_all_diagnostics(
    service: DiagnosticServiceDep,
) -> list[DiagnosticResponse]:
    """Retourne tous les diagnostics."""

    return service.get_all()


@router.get(
    "/{diagnostic_id}",
    response_model=DiagnosticResponse,
)
def get_diagnostic(
    diagnostic_id: int,
    service: DiagnosticServiceDep,
) -> DiagnosticResponse:
    """Récupère un diagnostic par son ID."""

    try:
        return service.get_by_id(diagnostic_id)

    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{diagnostic_id}",
    response_model=DiagnosticResponse,
)
def update_diagnostic(
    diagnostic_id: int,
    data: DiagnosticUpdate,
    service: DiagnosticServiceDep,
) -> DiagnosticResponse:
    """Met à jour un diagnostic."""

    try:
        return service.update(diagnostic_id, data)

    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{diagnostic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_diagnostic(
    diagnostic_id: int,
    service: DiagnosticServiceDep,
) -> None:
    """Supprime un diagnostic."""

    try:
        service.delete(diagnostic_id)

    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
