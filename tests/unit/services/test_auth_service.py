from sini.repositories.memory import InMemoryUserRepository
from sini.schemas.user import RegionMali, UserCreate
from sini.services.auth_service import AuthService
from sini.services.otp_service import OtpService
from sini.services.sms import ConsoleSmsGateway
from sini.services.token_service import TokenService
from sini.services.user_service import UserService


def make_auth_service() -> AuthService:
    user_service = UserService(InMemoryUserRepository())
    otp_service = OtpService()
    sms_gateway = ConsoleSmsGateway()
    token_service = TokenService()

    return AuthService(
        user_service=user_service,
        otp_service=otp_service,
        sms_gateway=sms_gateway,
        token_service=token_service,
    )


def make_user() -> UserCreate:
    return UserCreate(
        full_name="Moussa Diarra",
        phone_number="70 00 00 00",
        region=RegionMali.BAMAKO,
        password="password123",
    )


def test_request_otp_for_existing_user() -> None:
    auth_service = make_auth_service()

    user_service = auth_service.user_service
    user = user_service.create(make_user())

    result = auth_service.request_otp(user.phone_number)

    assert result is True


def test_request_otp_for_unknown_user() -> None:
    auth_service = make_auth_service()

    result = auth_service.request_otp("+22370000000")

    assert result is False


def test_verify_valid_otp_returns_tokens() -> None:
    auth_service = make_auth_service()

    user = auth_service.user_service.create(make_user())

    code = auth_service.otp_service.create_otp(
        user.phone_number,
    )

    result = auth_service.verify_otp(
        user.phone_number,
        code,
    )

    assert result is not None
    assert result.access_token
    assert result.refresh_token
    assert result.token_type == "bearer"


def test_verify_invalid_otp_returns_none() -> None:
    auth_service = make_auth_service()

    user = auth_service.user_service.create(make_user())

    result = auth_service.verify_otp(
        user.phone_number,
        "000000",
    )

    assert result is None


def test_verify_otp_for_unknown_user_returns_none() -> None:
    auth_service = make_auth_service()

    code = auth_service.otp_service.create_otp(
        "+22370000000",
    )

    result = auth_service.verify_otp(
        "+22370000000",
        code,
    )

    assert result is None


def test_refresh_access_token_with_valid_token() -> None:
    auth_service = make_auth_service()

    refresh_token = auth_service.token_service.create_refresh_token(
        1,
    )

    result = auth_service.refresh_access_token(
        refresh_token,
    )

    assert result is not None
    assert result.access_token
    assert result.refresh_token


def test_refresh_access_token_with_invalid_token() -> None:
    auth_service = make_auth_service()

    result = auth_service.refresh_access_token(
        "invalid-token",
    )

    assert result is None
