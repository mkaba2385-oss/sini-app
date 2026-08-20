from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sini.db.base import Base
from sini.schemas.journal import ActionType

if TYPE_CHECKING:
    from sini.models.parcelle import ParcelleModel


class JournalEntryModel(Base):
    __tablename__ = "journal_entries"
    __table_args__ = (
        CheckConstraint("cout_fcfa >= 0", name="ck_journal_entries_cout_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parcelle_id: Mapped[int] = mapped_column(
        ForeignKey("parcelles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    action_type: Mapped[ActionType] = mapped_column(
        Enum(ActionType, name="action_type"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    cout_fcfa: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

    parcelle: Mapped[ParcelleModel] = relationship(back_populates="journal_entries")
