from datetime import datetime, timedelta, timezone

import jwt

from sini.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class TokenService:
    def create_access_token(self, user_id: int) -> str:
        """Crée un token d'accès JWT."""

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": expires_at,
        }

        return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    def create_refresh_token(self, user_id: int) -> str:
        """Crée un refresh token JWT."""

        expires_at = datetime.now(timezone.utc) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS,
        )

        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expires_at,
        }

        return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    def verify_token(
        self,
        token: str,
        expected_type: str,
    ) -> int | None:
        """Vérifie un JWT et retourne l'identifiant utilisateur."""

        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.PyJWTError:
            return None

        if payload.get("type") != expected_type:
            return None

        user_id = payload.get("sub")

        if user_id is None:
            return None

        try:
            return int(user_id)
        except (TypeError, ValueError):
            return None
