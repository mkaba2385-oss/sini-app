from collections import Counter

from sini.db.session import SessionLocal
from sini.repositories.sqlalchemy import SqlAlchemyPrixRepository


def main() -> None:
    with SessionLocal() as session:
        repository = SqlAlchemyPrixRepository(session)

        prices = repository.get_all()

        print(f"Nombre total de prix : {len(prices)}")

        kg_prices = [price for price in prices if price.unite.value == "kg"]

        print(f"Nombre de prix en kg : {len(kg_prices)}")

        cultures = Counter(price.culture.value for price in kg_prices)

        print("\nPrix par culture :")
        for culture, count in sorted(cultures.items()):
            print(f"  {culture}: {count}")

        series = Counter((price.culture.value, price.marche) for price in kg_prices)

        print("\nNombre de prix par culture + marché :")
        for (culture, marche), count in sorted(series.items()):
            print(f"  {culture} / {marche}: {count}")


if __name__ == "__main__":
    main()
