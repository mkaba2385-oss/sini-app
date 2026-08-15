from typing import Optional

from sini.schemas.user import RegionMali, UserRole


class User:
    """Modèle domaine représentant un utilisateur de l'application Sini."""

    def __init__(
        self,
        user_id: int,
        full_name: str,
        phone_number: str,
        role: UserRole = UserRole.FARMER,
        region: Optional[RegionMali] = None,
    ) -> None:
        self.id = user_id
        self.full_name = full_name
        self._phone_number = phone_number  # Encapsulation / Attribut protégé (Jour 16)
        self.role = role
        self.region = region
        self.is_active: bool = True

    @property
    def phone_number(self) -> str:
        """Accès en lecture seule au numéro de téléphone."""
        return self._phone_number

    def deactivate(self) -> None:
        """Désactive le compte utilisateur."""
        self.is_active = False

    def __repr__(self) -> str:
        return f"<User id={self.id} name='{self.full_name}' role='{self.role.value}'>"
