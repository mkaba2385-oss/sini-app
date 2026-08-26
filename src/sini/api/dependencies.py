from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.factories.service_factory import ServiceFactory
from sini.schemas.user import UserResponse, UserRole
from sini.services.exceptions import EntityNotFoundError
from sini.services.token_service import TokenService
from sini.services.user_service import UserService

security = HTTPBearer()

SessionDep = Annotated[Session, Depends(get_session)]


def get_token_service() -> TokenService:
    """Crée le service de gestion des tokens JWT."""

    return TokenService()


TokenServiceDep = Annotated[
    TokenService,
    Depends(get_token_service),
]


def get_user_service(session: SessionDep) -> UserService:
    """Crée le service de gestion des utilisateurs."""

    return ServiceFactory.create_user_service(
        env="prod",
        session=session,
    )


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
    token_service: TokenServiceDep,
    user_service: UserServiceDep,
) -> UserResponse:
    """Récupère l'utilisateur authentifié à partir du JWT."""

    user_id = token_service.verify_token(
        credentials.credentials,
        expected_type="access",
    )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré.",
        )

    try:
        user = user_service.get_by_id(user_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable.",
        ) from exc

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur désactivé.",
        )

    return user


CurrentUserDep = Annotated[
    UserResponse,
    Depends(get_current_user),
]


def get_current_admin(
    current_user: CurrentUserDep,
) -> UserResponse:
    """Vérifie que l'utilisateur connecté est administrateur."""

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs.",
        )

    return current_user


CurrentAdminDep = Annotated[
    UserResponse,
    Depends(get_current_admin),
]
