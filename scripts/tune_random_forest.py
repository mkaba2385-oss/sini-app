from __future__ import annotations

from itertools import product

from sklearn.ensemble import RandomForestRegressor  # type: ignore[import-untyped]
from sklearn.metrics import (  # type: ignore[import-untyped]
    mean_absolute_error,
    root_mean_squared_error,
)
from sklearn.preprocessing import OneHotEncoder  # type: ignore[import-untyped]

from sini.db.session import SessionLocal
from sini.ml.model_comparison import (
    _build_global_training_data,
    _build_test_data,
    _group_prices,
)
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository
from sini.schemas.prix import PrixResponse


def main() -> None:
    """Teste plusieurs configurations de Random Forest."""

    with SessionLocal() as session:
        repository = SqlAlchemyPrixRepository(session)

        prices: list[PrixResponse] = repository.get_all()

    groups = _group_prices(prices)

    latest_date = max(price.date_releve for group in groups.values() for price in group)

    lag_size = 3

    test_groups: list[tuple[tuple[str, str], PrixResponse, list[PrixResponse]]] = []

    for key, group in groups.items():
        history = [price for price in group if price.date_releve < latest_date]

        test_prices = [price for price in group if price.date_releve == latest_date]

        if len(history) >= lag_size and test_prices:
            test_groups.append(
                (
                    key,
                    test_prices[0],
                    history,
                )
            )

    x_train, y_train, categories = _build_global_training_data(
        groups,
        latest_date,
        lag_size,
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    encoder.fit(categories)

    x_test, y_test = _build_test_data(
        test_groups,
        encoder,
        lag_size,
    )

    configurations = list(
        product(
            [50, 100, 200, 300],
            [None, 5, 10, 15],
            [1, 2, 4],
        )
    )

    results: list[tuple[int, int | None, int, float, float]] = []

    for n_estimators, max_depth, min_samples_leaf in configurations:
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
        )

        model.fit(x_train, y_train)

        predictions = model.predict(x_test)

        mae = float(
            mean_absolute_error(
                y_test,
                predictions,
            )
        )

        rmse = float(
            root_mean_squared_error(
                y_test,
                predictions,
            )
        )

        results.append(
            (
                n_estimators,
                max_depth,
                min_samples_leaf,
                mae,
                rmse,
            )
        )

    results.sort(key=lambda result: result[4])

    print()
    print("Tuning Random Forest")
    print("=" * 65)
    print()
    print(" n_estimators | max_depth | min_samples_leaf |    MAE |   RMSE")
    print("-" * 65)

    for (
        n_estimators,
        max_depth,
        min_samples_leaf,
        mae,
        rmse,
    ) in results[:10]:
        depth = str(max_depth) if max_depth is not None else "None"

        print(
            f" {n_estimators:12} | "
            f"{depth:9} | "
            f"{min_samples_leaf:16} | "
            f"{mae:6.2f} | "
            f"{rmse:6.2f}"
        )

    best = results[0]

    print()
    print("Meilleure configuration")
    print("-" * 30)
    print(f"n_estimators     : {best[0]}")
    print(f"max_depth        : {best[1]}")
    print(f"min_samples_leaf : {best[2]}")
    print(f"MAE              : {best[3]:.2f}")
    print(f"RMSE             : {best[4]:.2f}")


if __name__ == "__main__":
    main()
