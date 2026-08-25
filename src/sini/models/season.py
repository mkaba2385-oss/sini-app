from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sini.db.base import Base

if TYPE_CHECKING:
    from sini.models.harvest import HarvestModel


class SeasonModel(Base):
    __tablename__ = "seasons"
    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="ck_seasons_dates"),
        CheckConstraint("year >= 2000", name="ck_seasons_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False, index=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    harvests: Mapped[list[HarvestModel]] = relationship(
        back_populates="season",
        passive_deletes=True,
    )
