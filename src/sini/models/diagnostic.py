from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sini.db.base import Base
from sini.schemas.diagnostic import SeverityLevel

if TYPE_CHECKING:
    from sini.models.parcelle import ParcelleModel


class DiagnosticModel(Base):
    __tablename__ = "diagnostics"
    __table_args__ = (
        CheckConstraint(
            "score_confiance >= 0 AND score_confiance <= 1",
            name="ck_diagnostics_score_confiance_range",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parcelle_id: Mapped[int] = mapped_column(
        ForeignKey("parcelles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    symptomes_observes: Mapped[str] = mapped_column(String(1000), nullable=False)
    pathologie_detectee: Mapped[str | None] = mapped_column(String(255), nullable=True)
    niveau_severite: Mapped[SeverityLevel] = mapped_column(
        Enum(SeverityLevel, name="severity_level"), nullable=False
    )
    recommandations: Mapped[str] = mapped_column(String, nullable=False)
    score_confiance: Mapped[float] = mapped_column(Float, nullable=False)
    predictions: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(
        JSON, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )

    parcelle: Mapped[ParcelleModel] = relationship(back_populates="diagnostics")
