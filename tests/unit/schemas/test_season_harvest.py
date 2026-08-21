from datetime import date

import pytest
from pydantic import ValidationError

from sini.schemas.harvest import HarvestCreate
from sini.schemas.season import SeasonCreate


def test_season_rejects_invalid_dates() -> None:
    with pytest.raises(ValidationError):
        SeasonCreate(
            name="Saison des pluies",
            year=2026,
            start_date=date(2026, 11, 30),
            end_date=date(2026, 5, 1),
        )


def test_harvest_requires_positive_quantity() -> None:
    with pytest.raises(ValidationError):
        HarvestCreate(
            parcelle_id=1,
            season_id=1,
            quantite_recoltee=0,
            unite="kg",
            date_recolte=date(2026, 10, 15),
        )
