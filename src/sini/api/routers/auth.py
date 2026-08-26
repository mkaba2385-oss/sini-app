from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from sini.db.session import get_session
from sini.factories.service_factory import ServiceFactory
from sini.schemas.auth import (
    OtpRequest,
    OtpVerify,
    RefreshTokenRequest,
    TokenResponse,
)
from sini.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

SessionDep = Annotated[Session, Depends(get_session)]


def get_auth_service(session: SessionDep) -> AuthService:
    """Crée le service d'authentification."""

    return ServiceFactory.create_auth_service(
        env="prod",
        session=session,
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]


@router.post(
    "/otp",
    status_code=status.HTTP_200_OK,
)
def request_otp(
    data: OtpRequest,
    service: AuthServiceDep,
) -> dict[str, str]:
    """Demande l'envoi d'un code OTP."""

    success = service.request_otp(data.phone_number)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable.",
        )

    return {
        "message": "Code OTP envoyé.",
    }


@router.post(
    "/verify",
    response_model=TokenResponse,
)
def verify_otp(
    data: OtpVerify,
    service: AuthServiceDep,
) -> TokenResponse:
    """Vérifie un code OTP et retourne les tokens."""

    tokens = service.verify_otp(
        data.phone_number,
        data.code,
    )

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Code OTP invalide ou expiré.",
        )

    return tokens


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    data: RefreshTokenRequest,
    service: AuthServiceDep,
) -> TokenResponse:
    """Renouvelle les tokens à partir d'un refresh token."""

    tokens = service.refresh_access_token(
        data.refresh_token,
    )

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré.",
        )

    return tokens
