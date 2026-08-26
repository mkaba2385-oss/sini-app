from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sini.api.dependencies import CurrentUserDep
from sini.db.session import get_session
from sini.repositories.sqlalchemy import (
    SqlAlchemyDiagnosticRepository,
    SqlAlchemyParcelleRepository,
)
from sini.schemas.diagnostic import (
    DiagnosticCreate,
    DiagnosticResponse,
    DiagnosticUpdate,
)
from sini.services.diagnostic_service import DiagnosticService
from sini.services.exceptions import (
    EntityNotFoundError,
    UnauthorizedAccessError,
)

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
    """Crée un DiagnosticService avec les repositories PostgreSQL."""

    diagnostic_repository = SqlAlchemyDiagnosticRepository(session)
    parcelle_repository = SqlAlchemyParcelleRepository(session)

    return DiagnosticService(
        repository=diagnostic_repository,
        parcelle_repository=parcelle_repository,
    )


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
    current_user: CurrentUserDep,
) -> DiagnosticResponse:
    """Crée un nouveau diagnostic."""

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
    response_model=list[DiagnosticResponse],
)
def get_all_diagnostics(
    service: DiagnosticServiceDep,
    current_user: CurrentUserDep,
) -> list[DiagnosticResponse]:
    """Retourne uniquement les diagnostics de l'utilisateur."""

    return service.get_all(
        current_user.id,
    )


@router.get(
    "/{diagnostic_id}",
    response_model=DiagnosticResponse,
)
def get_diagnostic(
    diagnostic_id: int,
    service: DiagnosticServiceDep,
    current_user: CurrentUserDep,
) -> DiagnosticResponse:
    """Récupère un diagnostic par son ID."""

    try:
        return service.get_by_id(
            diagnostic_id,
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
    "/{diagnostic_id}",
    response_model=DiagnosticResponse,
)
def update_diagnostic(
    diagnostic_id: int,
    data: DiagnosticUpdate,
    service: DiagnosticServiceDep,
    current_user: CurrentUserDep,
) -> DiagnosticResponse:
    """Met à jour un diagnostic."""

    try:
        return service.update(
            diagnostic_id,
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
    "/{diagnostic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_diagnostic(
    diagnostic_id: int,
    service: DiagnosticServiceDep,
    current_user: CurrentUserDep,
) -> None:
    """Supprime un diagnostic."""

    try:
        service.delete(
            diagnostic_id,
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
