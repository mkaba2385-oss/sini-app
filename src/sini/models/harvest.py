from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sini.db.base import Base

if TYPE_CHECKING:
    from sini.models.parcelle import ParcelleModel
    from sini.models.season import SeasonModel


class HarvestModel(Base):
    __tablename__ = "harvests"
    __table_args__ = (
        CheckConstraint(
            "quantite_recoltee > 0",
            name="ck_harvests_quantity_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parcelle_id: Mapped[int] = mapped_column(
        ForeignKey("parcelles.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantite_recoltee: Mapped[float] = mapped_column(Float, nullable=False)
    unite: Mapped[str] = mapped_column(String(20), nullable=False)
    date_recolte: Mapped[date] = mapped_column(Date, nullable=False)

    parcelle: Mapped[ParcelleModel] = relationship(back_populates="harvests")
    season: Mapped[SeasonModel] = relationship(back_populates="harvests")
