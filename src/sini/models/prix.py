from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, Enum, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from sini.db.base import Base
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import UnitePrix


class PrixModel(Base):
    __tablename__ = "prices"
    __table_args__ = (
        CheckConstraint("prix_moyen > 0", name="ck_prices_prix_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    culture: Mapped[CultureType] = mapped_column(
        Enum(CultureType, name="culture_type"), nullable=False, index=True
    )
    marche: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    prix_moyen: Mapped[float] = mapped_column(Float, nullable=False)
    unite: Mapped[UnitePrix] = mapped_column(
        Enum(UnitePrix, name="unite_prix"), nullable=False
    )
    date_releve: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )
