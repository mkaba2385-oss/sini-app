from sini.db.session import SessionLocal
from sini.ml.model_comparison import compare_regression_models
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository


def main() -> None:
    with SessionLocal() as session:
        repository = SqlAlchemyPrixRepository(session)
        prices = repository.get_all()

        results = compare_regression_models(prices)

        print("\nComparaison des modèles")
        print("=" * 50)

        for result in results:
            print(f"\nModèle : {result.model_name}")
            print(f"MAE    : {result.mae}")
            print(f"RMSE   : {result.rmse}")


if __name__ == "__main__":
    main()
