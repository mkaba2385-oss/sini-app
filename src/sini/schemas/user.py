import re
from datetime import datetime
from enum import Enum
from functools import lru_cache

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserRole(str, Enum):
    FARMER = "FARMER"
    AGRONOMIST = "AGRONOMIST"
    ADMIN = "ADMIN"


class Language(str, Enum):
    """Langues disponibles pour les notifications et messages Sini."""

    FRENCH = "fr"
    BAMBARA = "bm"


class RegionMali(str, Enum):
    BAMAKO = "Bamako"
    KAYES = "Kayes"
    KOULIKORO = "Koulikoro"
    SIKASSO = "Sikasso"
    SEGOU = "Ségou"
    MOPTI = "Mopti"
    TOMBOUCTOU = "Tombouctou"
    GAO = "Gao"
    KIDAL = "Kidal"
    MENAKA = "Ménaka"
    TAOUDENIT = "Taoudénit"


@lru_cache(maxsize=1)
def _get_mali_phone_pattern() -> re.Pattern[str]:
    """Compile et met en cache la regex des numéros maliens normalisés."""
    return re.compile(r"^\+223[256789]\d{7}$")


def normalize_malian_phone(value: str) -> str:
    """Normalise un numéro malien vers le format international ``+223XXXXXXXX``."""
    cleaned = re.sub(r"[\s.()\-]", "", value)

    if cleaned.startswith("00223"):
        cleaned = "+223" + cleaned[5:]
    elif cleaned.startswith("223"):
        cleaned = "+223" + cleaned[3:]
    elif re.fullmatch(r"[256789]\d{7}", cleaned):
        cleaned = "+223" + cleaned

    if not _get_mali_phone_pattern().fullmatch(cleaned):
        raise ValueError(
            f"Le numéro '{value}' est invalide. "
            "Format attendu : +223XXXXXXXX (8 chiffres)."
        )
    return cleaned


class UserBase(BaseModel):
    """Champs communs d'un utilisateur."""

    full_name: str = Field(..., min_length=2, max_length=100, examples=["Kabine Kaba"])
    phone_number: str = Field(..., examples=["+22370000000"])
    region: RegionMali = Field(..., examples=[RegionMali.BAMAKO])
    role: UserRole = Field(default=UserRole.FARMER, examples=[UserRole.FARMER])
    language: Language = Field(default=Language.FRENCH)
    is_active: bool = True

    @field_validator("phone_number")
    @classmethod
    def validate_malian_phone(cls, value: str) -> str:
        """Valide et normalise le numéro de téléphone malien."""
        return normalize_malian_phone(value)


class UserCreate(UserBase):
    """Données nécessaires à la création d'un utilisateur."""

    password: str = Field(..., min_length=8, description="Mot de passe sécurisé")


class UserUpdate(BaseModel):
    """Champs modifiables d'un utilisateur."""

    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    phone_number: str | None = None
    region: RegionMali | None = None
    role: UserRole | None = None
    language: Language | None = None
    is_active: bool | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_malian_phone(cls, value: str | None) -> str | None:
        """Valide et normalise le numéro lorsqu'il est fourni."""
        return None if value is None else normalize_malian_phone(value)


class UserResponse(UserBase):
    """Représentation publique d'un utilisateur."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Alias métier demandé par la checklist.
UserOut = UserResponse
