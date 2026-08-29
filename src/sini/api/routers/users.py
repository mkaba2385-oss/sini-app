from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sini.api.dependencies import CurrentUserDep
from sini.db.session import get_session
from sini.factories.service_factory import ServiceFactory
from sini.schemas.user import UserCreate, UserResponse, UserUpdate
from sini.services.exceptions import EntityNotFoundError, SiniServiceError
from sini.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

SessionDep = Annotated[Session, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    """Crée un UserService avec le repository PostgreSQL."""
    return ServiceFactory.create_user_service(
        env="prod",
        session=session,
    )


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
    service: UserServiceDep,
) -> UserResponse:
    """Crée un nouvel utilisateur."""
    try:
        user = service.create(data)
        return user
    except SiniServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_profile(
    current_user: CurrentUserDep,
) -> UserResponse:
    """Récupère le profil de l'utilisateur connecté."""

    return current_user

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    service: UserServiceDep,
    current_user: CurrentUserDep,
) -> UserResponse:
    """Récupère un utilisateur par son ID."""

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez consulter que votre propre profil.",
        )

    try:
        return service.get_by_id(user_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserServiceDep,
    current_user: CurrentUserDep,
) -> UserResponse:
    """Met à jour un utilisateur."""

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez modifier que votre propre profil.",
        )

    try:
        return service.update(user_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except SiniServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{user_id}/deactivate",
    response_model=UserResponse,
)
def deactivate_user(
    user_id: int,
    service: UserServiceDep,
    current_user: CurrentUserDep,
) -> UserResponse:
    """Désactive un utilisateur."""

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez désactiver que votre propre compte.",
        )

    try:
        return service.deactivate(user_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
