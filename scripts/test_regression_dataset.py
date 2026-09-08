from sini.db.session import SessionLocal
from sini.ml.price_regression_dataset import build_global_training_data
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository


def main() -> None:
    with SessionLocal() as session:
        repository = SqlAlchemyPrixRepository(session)
        prices = repository.get_all()

        features, targets = build_global_training_data(prices)

        print(f"Nombre d'observations ML : {len(features)}")
        print(f"Nombre de variables : {features.shape[1]}")
        print(f"Taille des cibles : {len(targets)}")

        print("\nPremière observation :")
        print(features[0])

        print("\nPremière cible :")
        print(targets[0])


if __name__ == "__main__":
    main()
