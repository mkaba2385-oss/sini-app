from datetime import datetime, timezone

from fastapi.testclient import TestClient

from backend.main import app
from sini.api.dependencies import get_current_user
from sini.api.routers.users import get_user_service
from sini.schemas.user import (
    Language,
    RegionMali,
    UserCreate,
    UserResponse,
    UserRole,
    UserUpdate,
)
from sini.services.exceptions import EntityNotFoundError, SiniServiceError


class FakeUserService:
    def __init__(self) -> None:
        self.user = create_user()
        self.create_error: Exception | None = None
        self.get_error: Exception | None = None
        self.update_error: Exception | None = None
        self.deactivate_error: Exception | None = None

    def create(self, data: UserCreate) -> UserResponse:
        if self.create_error is not None:
            raise self.create_error

        return self.user

    def get_by_id(self, user_id: int) -> UserResponse:
        if self.get_error is not None:
            raise self.get_error

        return self.user

    def update(
        self,
        user_id: int,
        data: UserUpdate,
    ) -> UserResponse:
        if self.update_error is not None:
            raise self.update_error

        return self.user

    def deactivate(self, user_id: int) -> UserResponse:
        if self.deactivate_error is not None:
            raise self.deactivate_error

        return self.user


def create_user(
    user_id: int = 1,
    is_active: bool = True,
) -> UserResponse:
    return UserResponse(
        id=user_id,
        full_name="Kaba Coulibaly",
        phone_number="+22370000000",
        region=RegionMali.BAMAKO,
        role=UserRole.FARMER,
        language=Language.FRENCH,
        is_active=is_active,
        created_at=datetime(
            2026,
            8,
            25,
            10,
            0,
            0,
            tzinfo=timezone.utc,
        ),
    )


fake_service = FakeUserService()
current_user = create_user()


def override_get_user_service() -> FakeUserService:
    return fake_service


def override_get_current_user() -> UserResponse:
    return current_user


app.dependency_overrides[get_user_service] = override_get_user_service

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


def test_create_user_success() -> None:
    fake_service.create_error = None
    fake_service.user = create_user()

    response = client.post(
        "/users",
        json={
            "full_name": "Kaba Coulibaly",
            "phone_number": "+22370000000",
            "region": "Bamako",
            "role": "FARMER",
            "language": "fr",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["full_name"] == "Kaba Coulibaly"


def test_create_user_service_error_returns_400() -> None:
    fake_service.create_error = SiniServiceError("Erreur lors de la création.")

    response = client.post(
        "/users",
        json={
            "full_name": "Kaba Coulibaly",
            "phone_number": "+22370000000",
            "region": "Bamako",
            "role": "FARMER",
            "language": "fr",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == ("Erreur lors de la création.")

    fake_service.create_error = None


def test_get_user_success() -> None:
    fake_service.get_error = None
    fake_service.user = create_user(user_id=1)

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_other_user_returns_403() -> None:
    response = client.get("/users/2")

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Vous ne pouvez consulter que votre propre profil."
    )


def test_get_user_not_found_returns_404() -> None:
    fake_service.get_error = EntityNotFoundError(
        "Utilisateur",
        1,
    )

    response = client.get("/users/1")

    assert response.status_code == 404

    fake_service.get_error = None


def test_update_user_success() -> None:
    fake_service.update_error = None
    fake_service.user = create_user(user_id=1)

    response = client.patch(
        "/users/1",
        json={
            "full_name": "Nouveau nom",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_update_other_user_returns_403() -> None:
    response = client.patch(
        "/users/2",
        json={
            "full_name": "Nouveau nom",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Vous ne pouvez modifier que votre propre profil."
    )


def test_update_user_not_found_returns_404() -> None:
    fake_service.update_error = EntityNotFoundError(
        "Utilisateur",
        1,
    )

    response = client.patch(
        "/users/1",
        json={
            "full_name": "Nouveau nom",
        },
    )

    assert response.status_code == 404

    fake_service.update_error = None


def test_update_user_service_error_returns_400() -> None:
    fake_service.update_error = SiniServiceError("Erreur de modification.")

    response = client.patch(
        "/users/1",
        json={
            "full_name": "Nouveau nom",
        },
    )

    assert response.status_code == 400

    fake_service.update_error = None


def test_deactivate_user_success() -> None:
    fake_service.deactivate_error = None
    fake_service.user = create_user(
        user_id=1,
        is_active=False,
    )

    response = client.patch("/users/1/deactivate")

    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_deactivate_other_user_returns_403() -> None:
    response = client.patch("/users/2/deactivate")

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "Vous ne pouvez désactiver que votre propre compte."
    )


def test_deactivate_user_not_found_returns_404() -> None:
    fake_service.deactivate_error = EntityNotFoundError(
        "Utilisateur",
        1,
    )

    response = client.patch("/users/1/deactivate")

    assert response.status_code == 404

    fake_service.deactivate_error = None
