from enum import Enum
import re 
from datetime import datetime
from functools import lru_cache
from pydantic import BaseModel, ConfigDict, Field, field_validator

class UserRole(str, Enum):
    FARMER = "FARMER"
    AGRONOMIST = "AGRONOMIST"
    ADMIN = "ADMIN"

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
   """Compile et met en cache la regex pour validation rapide du téléphone malien."""
   return re.compile(r"^\+223[256789]\d{7}$") 

class UserBase(BaseModel):
    full_name: str =Field(..., min_length=2, max_length=100, examples=["Kabine Kaba"])
    phone_number: str=Field(..., examples=["+22370000000"])
    region: RegionMali = Field(..., examples=[RegionMali.BAMAKO])
    is_active: bool = True

    @field_validator("phone_number")
    @classmethod
    def validate_malian_phone(cls, v: str) -> str:
        # Nettoyage idiomatique des espaces
        cleaned = "".join(v.split())
        pattern = _get_mali_phone_pattern()
        if not pattern.match(cleaned):
            raise ValueError(
                f"le numéro '{v}' est invalide. Format attendu : +223XXXXXXXX (8 chiffres)."

            )
        return cleaned

class UserCreate(UserBase):
    password: str= Field(..., min_length=8, description="Mot de passe sécurisé")

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    phone_number: str | None = None
    is_active: bool | None = None

    @field_validator("phone_number")
    @classmethod
    def validate_malian_phone(cls, v: str | None) -> str | None:
        if v is None :
            return None
        return UserBase.validate_malian_phone(v)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    