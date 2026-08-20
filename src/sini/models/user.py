from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sini.db.base import Base
from sini.schemas.user import Language, RegionMali, UserRole

if TYPE_CHECKING:
    from sini.models.parcelle import ParcelleModel


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("phone_number", name="uq_users_phone_number"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    region: Mapped[RegionMali] = mapped_column(
        Enum(RegionMali, name="region_mali"), nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), nullable=False, default=UserRole.FARMER
    )
    language: Mapped[Language] = mapped_column(
        Enum(Language, name="language"), nullable=False, default=Language.FRENCH
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    parcelles: Mapped[list[ParcelleModel]] = relationship(back_populates="owner")
