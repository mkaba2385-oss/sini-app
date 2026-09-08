from datetime import date

from sini.db.session import SessionLocal
from sini.ml.random_forest_prediction import RandomForestPricePredictionModel
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository
from sini.schemas.parcelle import CultureType

with SessionLocal() as session:
    repository = SqlAlchemyPrixRepository(session)
    prices = repository.get_all()

    model = RandomForestPricePredictionModel()

    model.fit(prices)

    prediction = model.predict(
        prices=prices,
        culture=CultureType.MAIS,
        marche="Bamako",
        target_date=date(2021, 11, 20),
    )

    print(f"Nombre de prix : {len(prices)}")
    print(f"Prédiction Maïs / Bamako : {prediction} FCFA/kg")
