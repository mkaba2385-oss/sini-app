from statistics import mean

from sini.db.session import SessionLocal
from sini.ml.price_prediction import PricePredictionModel
from sini.ml.random_forest_prediction import RandomForestPricePredictionModel
from sini.ml.regression_prediction import RidgePricePredictionModel
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository
from sini.schemas.prix import PrixResponse


def mae(actual: list[float], predicted: list[float]) -> float:
    """Calcule la MAE."""
    return mean(
        abs(real - prediction)
        for real, prediction in zip(actual, predicted, strict=True)
    )


def rmse(actual: list[float], predicted: list[float]) -> float:
    """Calcule la RMSE."""
    return (
        mean(
            (real - prediction) ** 2
            for real, prediction in zip(actual, predicted, strict=True)
        )
        ** 0.5
    )


def load_prices() -> list[PrixResponse]:
    """Charge les prix depuis la base de données."""
    session = SessionLocal()

    try:
        repository = SqlAlchemyPrixRepository(session)
        return repository.get_all()
    finally:
        session.close()


def main() -> None:
    """Exécute le backtest chronologique."""
    prices = load_prices()

    # Le modèle travaille sur les prix en FCFA/kg.
    prices = [price for price in prices if price.unite.value == "kg"]

    prices.sort(key=lambda price: price.date_releve)

    if not prices:
        print("Aucun relevé en kg trouvé.")
        return

    dates = sorted({price.date_releve for price in prices})

    print("=" * 70)
    print("BACKTEST DES MODÈLES DE PRÉDICTION DES PRIX")
    print("=" * 70)
    print()

    print(f"Nombre de relevés : {len(prices)}")
    print(f"Période disponible : {dates[0]} → {dates[-1]}")
    print()

    print("Attention : les données disponibles ne couvrent pas 3 mois continus.")
    print()

    all_actual: list[float] = []
    all_baseline: list[float] = []
    all_ridge: list[float] = []
    all_random_forest: list[float] = []

    tested_dates: list[str] = []

    for target_date in dates:
        historical_prices = [
            price for price in prices if price.date_releve < target_date
        ]

        test_prices = [price for price in prices if price.date_releve == target_date]

        print("-" * 70)
        print(f"Date test : {target_date}")
        print(f"Historique disponible : {len(historical_prices)} relevés")
        print(f"Relevés à tester : {len(test_prices)}")

        date_actual: list[float] = []
        date_baseline: list[float] = []
        date_ridge: list[float] = []
        date_random_forest: list[float] = []

        # Un modèle est entraîné sur tout l'historique disponible
        # avant la date de test.
        ridge = RidgePricePredictionModel(lag_size=3)

        random_forest = RandomForestPricePredictionModel(
            lag_size=3,
            n_estimators=100,
            max_depth=None,
            min_samples_leaf=4,
        )

        try:
            ridge.fit(historical_prices)
            random_forest.fit(historical_prices)
        except ValueError as error:
            print(f"Date ignorée : {error}")
            continue

        baseline = PricePredictionModel(window_size=3)

        for test_price in test_prices:
            series_history = [
                price
                for price in historical_prices
                if price.culture == test_price.culture
                and price.marche == test_price.marche
            ]

            # Chaque culture/marché doit avoir au moins 3
            # observations historiques pour utiliser les lags.
            if len(series_history) < 3:
                continue

            try:
                baseline_prediction = baseline.predict(
                    series_history,
                    test_price.culture,
                    test_price.marche,
                    target_date,
                )

                ridge_prediction = ridge.predict(
                    series_history,
                    target_date,
                )

                random_forest_prediction = random_forest.predict(
                    historical_prices,
                    test_price.culture,
                    test_price.marche,
                    target_date,
                )

            except ValueError:
                continue

            date_actual.append(test_price.prix_moyen)
            date_baseline.append(baseline_prediction)
            date_ridge.append(ridge_prediction)
            date_random_forest.append(random_forest_prediction)

        if not date_actual:
            print("Aucun cas exploitable.")
            continue

        tested_dates.append(str(target_date))

        all_actual.extend(date_actual)
        all_baseline.extend(date_baseline)
        all_ridge.extend(date_ridge)
        all_random_forest.extend(date_random_forest)

        print(f"Cas testés : {len(date_actual)}")
        print(f"MAE Baseline       : {mae(date_actual, date_baseline):.2f}")
        print(f"MAE Ridge          : {mae(date_actual, date_ridge):.2f}")
        print(f"MAE Random Forest  : {mae(date_actual, date_random_forest):.2f}")

    if not all_actual:
        print()
        print("Aucun cas exploitable pour le backtest.")
        return

    print()
    print("=" * 70)
    print("RÉSULTATS GLOBAUX")
    print("=" * 70)
    print()

    print(f"Nombre de prédictions : {len(all_actual)}")
    print(f"Dates testées : {', '.join(tested_dates)}")
    print()

    baseline_mae = mae(all_actual, all_baseline)
    baseline_rmse = rmse(all_actual, all_baseline)

    ridge_mae = mae(all_actual, all_ridge)
    ridge_rmse = rmse(all_actual, all_ridge)

    random_forest_mae = mae(
        all_actual,
        all_random_forest,
    )
    random_forest_rmse = rmse(
        all_actual,
        all_random_forest,
    )

    print(f"{'Modèle':<25} {'MAE':>10} {'RMSE':>10}")
    print("-" * 50)

    print(f"{'Baseline':<25} {baseline_mae:>10.2f} {baseline_rmse:>10.2f}")

    print(f"{'Ridge Regression':<25} {ridge_mae:>10.2f} {ridge_rmse:>10.2f}")

    print(
        f"{'Random Forest':<25} {random_forest_mae:>10.2f} {random_forest_rmse:>10.2f}"
    )

    print()

    if baseline_mae > 0:
        mae_improvement = (baseline_mae - random_forest_mae) / baseline_mae * 100

        print(
            "Amélioration Random Forest / Baseline : "
            f"{mae_improvement:.1f} % sur la MAE"
        )

    if baseline_rmse > 0:
        rmse_improvement = (baseline_rmse - random_forest_rmse) / baseline_rmse * 100

        print(
            "Amélioration Random Forest / Baseline : "
            f"{rmse_improvement:.1f} % sur la RMSE"
        )


if __name__ == "__main__":
    main()
