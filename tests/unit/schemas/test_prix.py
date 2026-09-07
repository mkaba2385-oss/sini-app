from datetime import date

from sini.schemas.parcelle import CultureType
from sini.schemas.prix import PrixPredictionResponse, UnitePrix


def test_prix_prediction_response() -> None:
    prediction = PrixPredictionResponse(
        culture=CultureType.MAIS,
        marche="Marché de Ségou",
        date_prediction=date(2026, 10, 1),
        prix_predit=285.42,
        unite=UnitePrix.KG,
    )

    assert prediction.culture == CultureType.MAIS
    assert prediction.marche == "Marché de Ségou"
    assert prediction.date_prediction == date(2026, 10, 1)
    assert prediction.prix_predit == 285.42
    assert prediction.unite == UnitePrix.KG
