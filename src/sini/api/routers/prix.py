from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository
from sini.schemas.prix import PrixCreate, PrixResponse, PrixUpdate
from sini.services.exceptions import EntityNotFoundError
from sini.services.prix_service import PrixService

router = APIRouter(
    prefix="/prix",
    tags=["Prix"],
)


SessionDep = Annotated[
    Session,
    Depends(get_session),
]


def get_prix_service(
    session: SessionDep,
) -> PrixService:
    """Crée un PrixService avec le repository PostgreSQL."""

    repository = SqlAlchemyPrixRepository(session)

    return PrixService(repository)


PrixServiceDep = Annotated[
    PrixService,
    Depends(get_prix_service),
]


@router.post(
    "",
    response_model=PrixResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prix(
    data: PrixCreate,
    service: PrixServiceDep,
) -> PrixResponse:
    """Crée un nouveau relevé de prix."""

    try:
        return service.create(data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PrixResponse],
)
def get_all_prix(
    service: PrixServiceDep,
) -> list[PrixResponse]:
    """Récupère tous les relevés de prix."""

    return service.get_all()


@router.get(
    "/{prix_id}",
    response_model=PrixResponse,
)
def get_prix(
    prix_id: int,
    service: PrixServiceDep,
) -> PrixResponse:
    """Récupère un relevé de prix par son ID."""

    try:
        return service.get_by_id(prix_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{prix_id}",
    response_model=PrixResponse,
)
def update_prix(
    prix_id: int,
    data: PrixUpdate,
    service: PrixServiceDep,
) -> PrixResponse:
    """Met à jour un relevé de prix."""

    try:
        return service.update(prix_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{prix_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_prix(
    prix_id: int,
    service: PrixServiceDep,
) -> Response:
    """Supprime un relevé de prix."""

    try:
        service.delete(prix_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
