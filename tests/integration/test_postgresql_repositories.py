from __future__ import annotations

import os
from collections.abc import Generator
from datetime import date, datetime, timezone
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from alembic import command
from sini.models import (  # noqa: F401
    DiagnosticModel,
    JournalEntryModel,
    ParcelleModel,
    PhotoModel,
    PrixModel,
    UserModel,
)
from sini.repositories.sqlalchemy import (
    SqlAlchemyDiagnosticRepository,
    SqlAlchemyJournalRepository,
    SqlAlchemyParcelleRepository,
    SqlAlchemyPhotoRepository,
    SqlAlchemyPrixRepository,
    SqlAlchemyUserRepository,
)
from sini.schemas.diagnostic import DiagnosticResponse, SeverityLevel
from sini.schemas.journal import ActionType, JournalEntryResponse
from sini.schemas.parcelle import CultureType, ParcelleResponse
from sini.schemas.photo import PhotoResponse
from sini.schemas.prix import PrixResponse, UnitePrix
from sini.schemas.user import Language, RegionMali, UserResponse, UserRole

TEST_DATABASE_URL = os.getenv("SINI_TEST_DATABASE_URL")


@pytest.fixture(scope="session")
def postgres_engine() -> Generator[Engine, None, None]:
    """Fournit une vraie base PostgreSQL de test dédiée."""
    if not TEST_DATABASE_URL:
        pytest.skip(
            "SINI_TEST_DATABASE_URL n'est pas définie : tests PostgreSQL non exécutés."
        )
    if not TEST_DATABASE_URL.startswith("postgresql"):
        pytest.fail("SINI_TEST_DATABASE_URL doit pointer vers PostgreSQL.")

    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    project_root = Path(__file__).resolve().parents[2]
    alembic_config = Config(str(project_root / "alembic.ini"))
    alembic_config.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)

    # La base utilisée ici doit être exclusivement dédiée aux tests.
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")

    yield engine

    command.downgrade(alembic_config, "base")
    engine.dispose()


@pytest.fixture
def db_session(
    postgres_engine: Engine,
) -> Generator[Session, None, None]:
    """Une transaction isolée pour chaque test."""
    with Session(postgres_engine) as session:
        try:
            yield session
        finally:
            session.rollback()


def make_user(user_id: int = 0, phone: str = "+22370000000") -> UserResponse:
    return UserResponse(
        id=user_id,
        full_name="Testeur Sini",
        phone_number=phone,
        region=RegionMali.BAMAKO,
        role=UserRole.FARMER,
        language=Language.FRENCH,
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )


def make_parcelle(owner_id: int, parcelle_id: int = 0) -> ParcelleResponse:
    return ParcelleResponse(
        id=parcelle_id,
        owner_id=owner_id,
        name="Champ de test",
        superficie_ha=2.5,
        culture=CultureType.MAIS,
        region=RegionMali.BAMAKO,
        commune="Bamako",
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )


def test_user_crud_and_phone_uniqueness(db_session: Session) -> None:
    repo = SqlAlchemyUserRepository(db_session)

    created = repo.create(make_user())
    assert created.id > 0
    assert repo.get_by_id(created.id) is not None

    created.full_name = "Testeur Sini Modifie"
    updated = repo.add(created)
    assert updated.full_name == "Testeur Sini Modifie"

    assert repo.get_by_phone(created.phone_number) is not None
    assert len(repo.get_all()) == 1

    with pytest.raises(IntegrityError):
        repo.create(make_user(phone=created.phone_number))
        db_session.flush()

    db_session.rollback()

    repo.delete(created.id)
    assert repo.get_by_id(created.id) is None


def test_parcelle_relation_and_crud(db_session: Session) -> None:
    user_repo = SqlAlchemyUserRepository(db_session)
    parcelle_repo = SqlAlchemyParcelleRepository(db_session)

    user = user_repo.create(make_user())
    parcelle = parcelle_repo.create(make_parcelle(user.id))

    assert parcelle.id > 0
    assert parcelle_repo.get_by_id(parcelle.id) is not None

    parcelle.name = "Champ modifie"
    updated = parcelle_repo.add(parcelle)
    assert updated.name == "Champ modifie"
    assert updated.owner_id == user.id

    assert len(parcelle_repo.get_all()) == 1

    parcelle_repo.delete(parcelle.id)
    assert parcelle_repo.get_by_id(parcelle.id) is None


def test_journal_photo_and_diagnostic_are_persisted(db_session: Session) -> None:
    user_repo = SqlAlchemyUserRepository(db_session)
    parcelle_repo = SqlAlchemyParcelleRepository(db_session)
    journal_repo = SqlAlchemyJournalRepository(db_session)
    photo_repo = SqlAlchemyPhotoRepository(db_session)
    diagnostic_repo = SqlAlchemyDiagnosticRepository(db_session)

    user = user_repo.create(make_user())
    parcelle = parcelle_repo.create(make_parcelle(user.id))

    journal = journal_repo.create(
        JournalEntryResponse(
            id=0,
            parcelle_id=parcelle.id,
            action_type=ActionType.IRRIGATION,
            title="Irrigation test",
            description="Arrosage de contrôle",
            cout_fcfa=1500,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )
    )
    photo = photo_repo.create(
        PhotoResponse(
            id=0,
            parcelle_id=parcelle.id,
            url="https://example.test/photo.jpg",
            caption="Photo test",
            taken_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
        )
    )
    diagnostic = diagnostic_repo.create(
        DiagnosticResponse(
            id=0,
            parcelle_id=parcelle.id,
            symptomes_observes="Feuilles jaunies avec taches brunes",
            pathologie_detectee="Helminthosporiose",
            niveau_severite=SeverityLevel.MEDIUM,
            recommandations="Surveiller la parcelle",
            score_confiance=0.85,
            predictions={"Helminthosporiose": 0.85},
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )
    )

    assert journal_repo.get_by_id(journal.id) is not None
    assert photo_repo.get_by_id(photo.id) is not None
    assert diagnostic_repo.get_by_id(diagnostic.id) is not None
    assert len(journal_repo.list_by_parcelle(parcelle.id)) == 1


def test_price_repository_persists_history(db_session: Session) -> None:
    repo = SqlAlchemyPrixRepository(db_session)

    price = repo.create(
        PrixResponse(
            id=0,
            culture=CultureType.MAIS,
            marche="Marché de Bamako",
            prix_moyen=250,
            unite=UnitePrix.KG,
            date_releve=date(2026, 8, 1),
            created_at=datetime.now(timezone.utc),
            updated_at=None,
        )
    )

    assert price.id > 0
    results = repo.get_all()
    assert len(results) == 1
    assert results[0].prix_moyen == 250
