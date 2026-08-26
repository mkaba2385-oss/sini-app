from sini.schemas.auth import TokenResponse
from sini.services.otp_service import OtpService
from sini.services.sms import SmsGateway
from sini.services.token_service import TokenService
from sini.services.user_service import UserService


class AuthService:
    """Service métier responsable de l'authentification."""

    def __init__(
        self,
        user_service: UserService,
        otp_service: OtpService,
        sms_gateway: SmsGateway,
        token_service: TokenService,
    ) -> None:
        self.user_service = user_service
        self.otp_service = otp_service
        self.sms_gateway = sms_gateway
        self.token_service = token_service

    def request_otp(self, phone_number: str) -> bool:
        """Génère et envoie un code OTP à un utilisateur."""

        user = self.user_service.get_by_phone(phone_number)

        if user is None:
            return False

        code = self.otp_service.create_otp(phone_number)

        message = f"Votre code de vérification Sini est : {code}"

        return self.sms_gateway.send_sms(
            phone_number,
            message,
        )

    def verify_otp(
        self,
        phone_number: str,
        code: str,
    ) -> TokenResponse | None:
        """Vérifie un OTP et retourne les tokens JWT."""

        user = self.user_service.get_by_phone(phone_number)

        if user is None:
            return None

        is_valid = self.otp_service.verify_otp(
            phone_number,
            code,
        )

        if not is_valid:
            return None

        return TokenResponse(
            access_token=self.token_service.create_access_token(user.id),
            refresh_token=self.token_service.create_refresh_token(user.id),
        )

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> TokenResponse | None:
        """Crée une nouvelle paire de tokens à partir d'un refresh token."""

        user_id = self.token_service.verify_token(
            refresh_token,
            expected_type="refresh",
        )

        if user_id is None:
            return None

        return TokenResponse(
            access_token=self.token_service.create_access_token(user_id),
            refresh_token=self.token_service.create_refresh_token(user_id),
        )
