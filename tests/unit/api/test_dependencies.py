import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from sini.api.dependencies import get_current_user
from sini.schemas.user import (
    Language,
    RegionMali,
    UserResponse,
    UserRole,
)
from sini.services.exceptions import EntityNotFoundError


class FakeTokenService:
    def __init__(self, user_id: int | None) -> None:
        self.user_id = user_id

    def verify_token(
        self,
        token: str,
        expected_type: str,
    ) -> int | None:
        return self.user_id


class FakeUserService:
    def __init__(
        self,
        user: UserResponse | None = None,
        should_raise: bool = False,
    ) -> None:
        self.user = user
        self.should_raise = should_raise

    def get_by_id(self, user_id: int) -> UserResponse:
        if self.should_raise:
            raise EntityNotFoundError("Utilisateur", user_id)

        if self.user is None:
            raise EntityNotFoundError("Utilisateur", user_id)

        return self.user


def create_user(is_active: bool = True) -> UserResponse:
    return UserResponse(
        id=1,
        full_name="Kaba Coulibaly",
        phone_number="+22370000000",
        region=RegionMali.BAMAKO,
        role=UserRole.FARMER,
        language=Language.FRENCH,
        is_active=is_active,
        created_at="2026-08-25T10:00:00",
    )


def create_credentials() -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="valid-access-token",
    )


def test_get_current_user_returns_active_user() -> None:
    user = create_user()

    result = get_current_user(
        credentials=create_credentials(),
        token_service=FakeTokenService(user_id=1),
        user_service=FakeUserService(user=user),
    )

    assert result == user


def test_get_current_user_invalid_token_raises_401() -> None:
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=create_credentials(),
            token_service=FakeTokenService(user_id=None),
            user_service=FakeUserService(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token invalide ou expiré."


def test_get_current_user_refresh_token_raises_401() -> None:
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=create_credentials(),
            token_service=FakeTokenService(user_id=None),
            user_service=FakeUserService(),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token invalide ou expiré."


def test_get_current_user_unknown_user_raises_401() -> None:
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=create_credentials(),
            token_service=FakeTokenService(user_id=999),
            user_service=FakeUserService(should_raise=True),
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Utilisateur introuvable."


def test_get_current_user_inactive_user_raises_403() -> None:
    user = create_user(is_active=False)

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(
            credentials=create_credentials(),
            token_service=FakeTokenService(user_id=1),
            user_service=FakeUserService(user=user),
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Utilisateur désactivé."
