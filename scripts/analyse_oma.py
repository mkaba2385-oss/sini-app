from datetime import date
from pathlib import Path

import pandas as pd

from sini.parsers.oma import OmaPriceParser
from sini.scrapers.oma import OmaScraper


PDF_PATH = Path("data/oma/communique_du_04_au_10_novembre_2021.pdf")


def main() -> None:
    pdf_content = PDF_PATH.read_bytes()

    scraper = OmaScraper()
    text = scraper.extract_text(pdf_content)

    parser = OmaPriceParser()
    date_releve = date(2021, 11, 10)

    records = []

    records.extend(
        parser.parse_tableau_1(
            text=text,
            date_releve=date_releve,
        )
    )

    records.extend(
        parser.parse_tableau_2(
            text=text,
            date_releve=date_releve,
        )
    )

    records.extend(
        parser.parse_tableau_3(
            text=text,
            date_releve=date_releve,
        )
    )

    records.extend(
        parser.parse_tableau_4(
            text=text,
            date_releve=date_releve,
        )
    )

    df = pd.DataFrame([record.__dict__ for record in records])
    df["date_releve"] = pd.to_datetime(df["date_releve"])

    df["prix_kg"] = df["prix"]

    df.loc[df["unite"] == "100kg", "prix_kg"] = (
        df.loc[df["unite"] == "100kg", "prix"] / 100
    )

    print("Nombre total de records :", len(df))
    print()
    print("Colonnes :")
    print(df.columns.tolist())
    print()
    print("Répartition par type de prix :")
    print(df["type_prix"].value_counts())
    print()
    print("Répartition par unité :")
    print(df["unite"].value_counts())
    print()
    print("Aperçu :")
    print(df.head(10))

    print()
    print("=== VALEURS MANQUANTES ===")
    print(df.isna().sum())

    print()
    print("=== DOUBLONS ===")
    print("Nombre de doublons :", df.duplicated().sum())

    print()
    print("=== DOUBLONS MÉTIER ===")

    colonnes_uniques = [
        "date_releve",
        "type_prix",
        "culture",
        "variete",
        "marche",
    ]

    doublons_metier = df[
        df.duplicated(subset=colonnes_uniques, keep=False)
    ]

    print("Nombre de lignes concernées :", len(doublons_metier))
    print(doublons_metier)

    print()
    print("=== PRIX INVALIDES ===")
    print(df[df["prix"] <= 0])

    print()
    print("=== TYPES DE DONNÉES ===")
    print(df.dtypes)

    print()
    print("=== STATISTIQUES DES PRIX AU KG ===")
    print(df["prix_kg"].describe())

    print()
    print("=== PRIX PAR CULTURE ET TYPE ===")

    analyse_culture = (
        df.groupby(["type_prix", "culture"])["prix_kg"]
        .agg(["count", "min", "mean", "max"])
        .round(2)
    )

    print(analyse_culture)


    print()
    print("=== PRIX PAR MARCHÉ ===")

    analyse_marche = (
        df.groupby(["type_prix", "marche"])["prix_kg"]
        .agg(["count", "min", "mean", "max"])
        .round(2)
    )

    print(analyse_marche)


    print()
    print("=== VALEURS ABERRANTES PAR CULTURE ET VARIÉTÉ ===")

    groupes = [
        "type_prix",
        "culture",
        "variete",
    ]

    statistiques = (
        df.groupby(groupes, dropna=False)["prix_kg"]
        .agg(["count", "mean", "std"])
        .rename(
            columns={
                "mean": "moyenne",
                "std": "ecart_type",
            }
        )
    )

    df_analyse = df.merge(
        statistiques,
        on=groupes,
        how="left",
    )

    df_analyse["z_score"] = (
        df_analyse["prix_kg"] - df_analyse["moyenne"]
    ) / df_analyse["ecart_type"]

    valeurs_aberrantes = df_analyse[
        (df_analyse["count"] >= 3)
        & (df_analyse["z_score"].abs() > 2)
    ]

    print(
        valeurs_aberrantes[
            [
                "type_prix",
                "culture",
                "variete",
                "marche",
                "prix_kg",
                "moyenne",
                "ecart_type",
                "z_score",
            ]
        ]
    )


    print()
    print("=== PRIX DU MAÏS PILÉ ===")

    mais_pile = df[
        (df["culture"] == "Maïs")
        & (df["variete"] == "Pilé")
    ][
        [
            "date_releve",
            "type_prix",
            "marche",
            "prix_kg",
        ]
    ].sort_values("prix_kg")

    print(mais_pile.to_string(index=False))




if __name__ == "__main__":
    main()