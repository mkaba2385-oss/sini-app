from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sini.db.base import Base
from sini.schemas.parcelle import CultureType
from sini.schemas.user import RegionMali

if TYPE_CHECKING:
    from sini.models.diagnostic import DiagnosticModel
    from sini.models.harvest import HarvestModel
    from sini.models.journal import JournalEntryModel
    from sini.models.photo import PhotoModel
    from sini.models.user import UserModel


class ParcelleModel(Base):
    __tablename__ = "parcelles"
    __table_args__ = (
        CheckConstraint("superficie_ha > 0", name="ck_parcelles_superficie_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    superficie_ha: Mapped[float] = mapped_column(Float, nullable=False)
    culture: Mapped[CultureType] = mapped_column(
        Enum(CultureType, name="culture_type"), nullable=False, index=True
    )
    region: Mapped[RegionMali] = mapped_column(
        Enum(RegionMali, name="region_mali"), nullable=False, index=True
    )
    commune: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

    owner: Mapped[UserModel] = relationship(back_populates="parcelles")
    journal_entries: Mapped[list[JournalEntryModel]] = relationship(
        back_populates="parcelle",
        cascade="all, delete-orphan",
    )
    photos: Mapped[list[PhotoModel]] = relationship(
        back_populates="parcelle",
        cascade="all, delete-orphan",
    )
    harvests: Mapped[list[HarvestModel]] = relationship(
        back_populates="parcelle",
    )
    diagnostics: Mapped[list[DiagnosticModel]] = relationship(
        back_populates="parcelle",
        cascade="all, delete-orphan",
    )
