from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.repositories.sqlalchemy import SqlAlchemyPhotoRepository
from sini.schemas.photo import PhotoCreate, PhotoResponse, PhotoUpdate
from sini.services.exceptions import EntityNotFoundError
from sini.services.photo_service import PhotoService

router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)


SessionDep = Annotated[
    Session,
    Depends(get_session),
]


def get_photo_service(
    session: SessionDep,
) -> PhotoService:
    """Crée un PhotoService avec le repository PostgreSQL."""

    repository = SqlAlchemyPhotoRepository(session)

    return PhotoService(repository)


PhotoServiceDep = Annotated[
    PhotoService,
    Depends(get_photo_service),
]


@router.post(
    "",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_photo(
    data: PhotoCreate,
    service: PhotoServiceDep,
) -> PhotoResponse:
    """Crée une nouvelle photo."""

    try:
        return service.create(data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PhotoResponse],
)
def get_all_photos(
    service: PhotoServiceDep,
) -> list[PhotoResponse]:
    """Récupère toutes les photos."""

    return service.get_all()


@router.get(
    "/{photo_id}",
    response_model=PhotoResponse,
)
def get_photo(
    photo_id: int,
    service: PhotoServiceDep,
) -> PhotoResponse:
    """Récupère une photo par son ID."""

    try:
        return service.get_by_id(photo_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{photo_id}",
    response_model=PhotoResponse,
)
def update_photo(
    photo_id: int,
    data: PhotoUpdate,
    service: PhotoServiceDep,
) -> PhotoResponse:
    """Met à jour une photo."""

    try:
        return service.update(photo_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_photo(
    photo_id: int,
    service: PhotoServiceDep,
) -> None:
    """Supprime une photo."""

    try:
        service.delete(photo_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
