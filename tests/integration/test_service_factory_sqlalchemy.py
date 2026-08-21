from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from sini.db.base import Base
from sini.factories.service_factory import ServiceFactory
from sini.repositories.sqlalchemy import SqlAlchemyParcelleRepository
from sini.schemas.parcelle import CultureType, ParcelleCreate, RegionMali
from sini.services.parcelle_service import ParcelleService


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)
    session = factory()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_factory_dev_uses_inmemory() -> None:
    service = ServiceFactory.create_parcelle_service(env="dev")
    assert service.repo.__class__.__name__ == "InMemoryParcelleRepository"


def test_factory_prod_requires_session() -> None:
    with pytest.raises(ValueError, match="session SQLAlchemy"):
        ServiceFactory.create_parcelle_service(env="prod")


def test_factory_prod_uses_sqlalchemy(db_session: Session) -> None:
    service = ServiceFactory.create_parcelle_service(env="prod", session=db_session)

    assert isinstance(service, ParcelleService)
    assert isinstance(service.repo, SqlAlchemyParcelleRepository)

    created = service.create_parcelle(
        ParcelleCreate(
            name="Champ SQLAlchemy",
            superficie_ha=2.5,
            culture=CultureType.MAIS,
            region=RegionMali.SEGOU,
            owner_id=1,
        )
    )

    assert created.id == 1
    assert service.get_by_id(created.id).name == "Champ SQLAlchemy"
