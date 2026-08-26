from fastapi.testclient import TestClient

from backend.main import app
from sini.api.routers.auth import get_auth_service
from sini.schemas.auth import TokenResponse


class FakeAuthService:
    def __init__(self) -> None:
        self.request_otp_result = True
        self.verify_otp_result: TokenResponse | None = None
        self.refresh_token_result: TokenResponse | None = None

    def request_otp(self, phone_number: str) -> bool:
        return self.request_otp_result

    def verify_otp(
        self,
        phone_number: str,
        code: str,
    ) -> TokenResponse | None:
        return self.verify_otp_result

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> TokenResponse | None:
        return self.refresh_token_result


fake_service = FakeAuthService()


def override_get_auth_service() -> FakeAuthService:
    return fake_service


app.dependency_overrides[get_auth_service] = override_get_auth_service

client = TestClient(app)


def test_request_otp_success() -> None:
    fake_service.request_otp_result = True

    response = client.post(
        "/auth/otp",
        json={
            "phone_number": "+22370000000",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Code OTP envoyé.",
    }


def test_request_otp_unknown_user() -> None:
    fake_service.request_otp_result = False

    response = client.post(
        "/auth/otp",
        json={
            "phone_number": "+22370000000",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Utilisateur introuvable."


def test_verify_otp_success() -> None:
    fake_service.verify_otp_result = TokenResponse(
        access_token="access-token",
        refresh_token="refresh-token",
    )

    response = client.post(
        "/auth/verify",
        json={
            "phone_number": "+22370000000",
            "code": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"] == "access-token"
    assert data["refresh_token"] == "refresh-token"
    assert data["token_type"] == "bearer"


def test_verify_otp_invalid() -> None:
    fake_service.verify_otp_result = None

    response = client.post(
        "/auth/verify",
        json={
            "phone_number": "+22370000000",
            "code": "123456",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Code OTP invalide ou expiré."


def test_refresh_token_success() -> None:
    fake_service.refresh_token_result = TokenResponse(
        access_token="new-access-token",
        refresh_token="new-refresh-token",
    )

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "valid-refresh-token",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"] == "new-access-token"
    assert data["refresh_token"] == "new-refresh-token"
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid() -> None:
    fake_service.refresh_token_result = None

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == ("Refresh token invalide ou expiré.")
