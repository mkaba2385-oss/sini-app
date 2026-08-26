import secrets
from datetime import datetime, timedelta, timezone


class OtpService:
    def __init__(self) -> None:
        self._otps: dict[str, tuple[str, datetime]] = {}

    def generate_code(self) -> str:
        """Génère un code OTP à 6 chiffres."""
        return f"{secrets.randbelow(1_000_000):06d}"

    def create_otp(
        self,
        phone_number: str,
        expires_in_minutes: int = 5,
    ) -> str:
        """Crée et enregistre un OTP pour un numéro de téléphone."""
        code = self.generate_code()

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=expires_in_minutes,
        )

        self._otps[phone_number] = (code, expires_at)

        return code

    def verify_otp(
        self,
        phone_number: str,
        code: str,
    ) -> bool:
        """Vérifie qu'un OTP est valide et non expiré."""

        otp_data = self._otps.get(phone_number)

        if otp_data is None:
            return False

        stored_code, expires_at = otp_data

        if datetime.now(timezone.utc) > expires_at:
            del self._otps[phone_number]
            return False

        if stored_code != code:
            return False

        del self._otps[phone_number]

        return True
