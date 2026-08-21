from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select

from sini.db.session import SessionLocal
from sini.models.diagnostic import DiagnosticModel
from sini.models.harvest import HarvestModel
from sini.models.journal import JournalEntryModel
from sini.models.parcelle import ParcelleModel
from sini.models.photo import PhotoModel
from sini.models.prix import PrixModel
from sini.models.season import SeasonModel
from sini.models.user import UserModel
from sini.schemas.diagnostic import SeverityLevel
from sini.schemas.journal import ActionType
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import UnitePrix
from sini.schemas.user import Language, RegionMali, UserRole

USERS = [
    ("Moussa Traoré", "+22376000001", RegionMali.SEGOU, "moussa"),
    ("Aïssata Coulibaly", "+22377000002", RegionMali.SIKASSO, "aissata"),
    ("Oumar Diarra", "+22378000003", RegionMali.KOULIKORO, "oumar"),
    ("Fatoumata Keïta", "+22379000004", RegionMali.MOPTI, "fatoumata"),
    ("Ibrahim Konaté", "+22325000005", RegionMali.KAYES, "ibrahim"),
]

PARCELLES = [
    ("Champ Ségou Nord", 2.5, CultureType.MAIS, RegionMali.SEGOU, "Pelengana", 0),
    ("Rizière Niono", 3.2, CultureType.RIZ, RegionMali.SEGOU, "Niono", 0),
    ("Champ Sikasso Est", 1.8, CultureType.COTON, RegionMali.SIKASSO, "Sikasso", 1),
    (
        "Maraîchage Koulikoro",
        0.9,
        CultureType.MARAICHAGE,
        RegionMali.KOULIKORO,
        "Kati",
        2,
    ),
    ("Champ Mopti Sud", 4.0, CultureType.MIL, RegionMali.MOPTI, "Mopti", 3),
    ("Champ Kayes Ouest", 2.1, CultureType.ARACHIDE, RegionMali.KAYES, "Kayes", 4),
]

JOURNALS = [
    (
        "Semis du maïs",
        ActionType.SEMIS,
        "Semis de la parcelle après préparation du sol.",
        15000.0,
        0,
    ),
    (
        "Apport NPK",
        ActionType.FERTILISATION,
        "Apport d'engrais NPK sur les rangs de maïs.",
        25000.0,
        0,
    ),
    ("Irrigation", ActionType.IRRIGATION, "Irrigation de la rizière.", 12000.0, 1),
    ("Désherbage", ActionType.DESHERBAGE, "Premier désherbage manuel.", 8000.0, 1),
    (
        "Traitement coton",
        ActionType.TRAITEMENT,
        "Traitement phytosanitaire préventif.",
        18000.0,
        2,
    ),
    (
        "Observation feuilles",
        ActionType.OBSERVATION,
        "Observation de quelques taches sur les feuilles.",
        0.0,
        2,
    ),
    ("Semis mil", ActionType.SEMIS, "Semis après les premières pluies.", 10000.0, 4),
    (
        "Récolte arachide",
        ActionType.RECOLTE,
        "Début de récolte de l'arachide.",
        30000.0,
        5,
    ),
]


def get_or_create_user(session, name, phone, region, _slug):
    user = session.scalar(select(UserModel).where(UserModel.phone_number == phone))
    if user is None:
        user = UserModel(
            full_name=name,
            phone_number=phone,
            region=region,
            role=UserRole.FARMER,
            language=Language.FRENCH,
            is_active=True,
        )
        session.add(user)
        session.flush()
    return user


def seed() -> None:
    session = SessionLocal()
    try:
        users = [get_or_create_user(session, *data) for data in USERS]

        parcels: list[ParcelleModel] = []
        for name, superficie, culture, region, commune, user_index in PARCELLES:
            owner = users[user_index]
            parcel = session.scalar(
                select(ParcelleModel).where(
                    ParcelleModel.owner_id == owner.id,
                    ParcelleModel.name == name,
                )
            )
            if parcel is None:
                parcel = ParcelleModel(
                    owner_id=owner.id,
                    name=name,
                    superficie_ha=superficie,
                    culture=culture,
                    region=region,
                    commune=commune,
                )
                session.add(parcel)
                session.flush()
            parcels.append(parcel)

        for title, action_type, description, cost, parcel_index in JOURNALS:
            parcel = parcels[parcel_index]
            exists = session.scalar(
                select(JournalEntryModel).where(
                    JournalEntryModel.parcelle_id == parcel.id,
                    JournalEntryModel.title == title,
                )
            )
            if exists is None:
                session.add(
                    JournalEntryModel(
                        parcelle_id=parcel.id,
                        action_type=action_type,
                        title=title,
                        description=description,
                        cout_fcfa=cost,
                    )
                )

        photo_data = [
            (
                parcels[0].id,
                "https://example.com/sini/champ-segou-nord.jpg",
                "Vue générale du champ",
            ),
            (
                parcels[2].id,
                "https://example.com/sini/champ-sikasso-est.jpg",
                "Feuillage du coton",
            ),
        ]
        for parcel_id, url, caption in photo_data:
            if session.scalar(select(PhotoModel).where(PhotoModel.url == url)) is None:
                session.add(PhotoModel(parcelle_id=parcel_id, url=url, caption=caption))

        diagnostic_exists = session.scalar(
            select(DiagnosticModel).where(DiagnosticModel.parcelle_id == parcels[2].id)
        )
        if diagnostic_exists is None:
            session.add(
                DiagnosticModel(
                    parcelle_id=parcels[2].id,
                    symptomes_observes=(
                        "Quelques taches brunes sur les feuilles du coton."
                    ),
                    pathologie_detectee="Suspicion de maladie foliaire",
                    niveau_severite=SeverityLevel.MEDIUM,
                    recommandations=(
                        "Surveiller l'évolution et appliquer le traitement recommandé "
                        "si les symptômes progressent."
                    ),
                    score_confiance=0.82,
                    predictions=[
                        {"maladie": "Maladie foliaire", "probabilite": 0.82},
                        {"maladie": "Autre cause", "probabilite": 0.18},
                    ],
                )
            )

        today = datetime.now(timezone.utc).date()
        season = session.scalar(
            select(SeasonModel).where(
                SeasonModel.name == "Saison des pluies", SeasonModel.year == today.year
            )
        )
        if season is None:
            season = SeasonModel(
                name="Saison des pluies",
                year=today.year,
                start_date=date(today.year, 5, 1),
                end_date=date(today.year, 11, 30),
            )
            session.add(season)
            session.flush()

        harvest_data = [
            (parcels[0].id, 1800.0, "kg", date(today.year, 7, 15)),
            (parcels[1].id, 5200.0, "kg", date(today.year, 8, 5)),
            (parcels[5].id, 2500.0, "kg", date(today.year, 7, 20)),
        ]
        for parcel_id, quantity, unit, harvested_at in harvest_data:
            exists = session.scalar(
                select(HarvestModel).where(
                    HarvestModel.parcelle_id == parcel_id,
                    HarvestModel.season_id == season.id,
                )
            )
            if exists is None:
                session.add(
                    HarvestModel(
                        parcelle_id=parcel_id,
                        season_id=season.id,
                        quantite_recoltee=quantity,
                        unite=unit,
                        date_recolte=harvested_at,
                    )
                )

        prices = [
            (
                CultureType.MAIS,
                "Marché de Ségou",
                275.0,
                UnitePrix.KG,
                today - timedelta(days=10),
            ),
            (
                CultureType.MAIS,
                "Marché de Ségou",
                290.0,
                UnitePrix.KG,
                today - timedelta(days=3),
            ),
            (
                CultureType.RIZ,
                "Marché de Niono",
                425.0,
                UnitePrix.KG,
                today - timedelta(days=7),
            ),
            (
                CultureType.COTON,
                "Marché de Sikasso",
                310.0,
                UnitePrix.KG,
                today - timedelta(days=5),
            ),
        ]
        for culture, market, price, unit, recorded_at in prices:
            exists = session.scalar(
                select(PrixModel).where(
                    PrixModel.culture == culture,
                    PrixModel.marche == market,
                    PrixModel.date_releve == recorded_at,
                )
            )
            if exists is None:
                session.add(
                    PrixModel(
                        culture=culture,
                        marche=market,
                        prix_moyen=price,
                        unite=unit,
                        date_releve=recorded_at,
                    )
                )

        session.commit()
        print(
            "Seed de développement terminé : 5 utilisateurs, "
            "6 parcelles et 8 entrées de journal préparés."
        )
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
