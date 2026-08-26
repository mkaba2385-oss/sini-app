import jwt

from sini.config import JWT_ALGORITHM, JWT_SECRET_KEY
from sini.services.token_service import TokenService


def test_create_access_token() -> None:
    service = TokenService()

    token = service.create_access_token(user_id=1)

    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )

    assert payload["sub"] == "1"
    assert payload["type"] == "access"


def test_create_refresh_token() -> None:
    service = TokenService()

    token = service.create_refresh_token(user_id=1)

    payload = jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )

    assert payload["sub"] == "1"
    assert payload["type"] == "refresh"


def test_verify_valid_access_token() -> None:
    service = TokenService()

    token = service.create_access_token(user_id=1)

    user_id = service.verify_token(
        token,
        expected_type="access",
    )

    assert user_id == 1


def test_verify_valid_refresh_token() -> None:
    service = TokenService()

    token = service.create_refresh_token(user_id=1)

    user_id = service.verify_token(
        token,
        expected_type="refresh",
    )

    assert user_id == 1


def test_verify_token_with_wrong_type() -> None:
    service = TokenService()

    refresh_token = service.create_refresh_token(user_id=1)

    user_id = service.verify_token(
        refresh_token,
        expected_type="access",
    )

    assert user_id is None


def test_verify_invalid_token() -> None:
    service = TokenService()

    user_id = service.verify_token(
        "invalid-token",
        expected_type="access",
    )

    assert user_id is None


def test_verify_token_with_invalid_user_id() -> None:
    service = TokenService()

    token = jwt.encode(
        {
            "sub": "invalid-user-id",
            "type": "access",
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    user_id = service.verify_token(
        token,
        expected_type="access",
    )

    assert user_id is None
