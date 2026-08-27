from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import sini.factories.service_factory as service_factory_module
from sini.db.base import Base
from sini.factories.service_factory import ServiceFactory
from sini.providers.openweather import OpenWeatherMapProvider
from sini.repositories.sqlalchemy import SqlAlchemyParcelleRepository


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    factory = sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
    )

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


def test_factory_prod_uses_sqlalchemy(
    monkeypatch: pytest.MonkeyPatch,
    db_session: Session,
) -> None:
    monkeypatch.setattr(
        service_factory_module,
        "OPENWEATHER_API_KEY",
        "fake-api-key",
    )

    service = ServiceFactory.create_parcelle_service(
        env="prod",
        session=db_session,
    )

    assert isinstance(
        service.repo,
        SqlAlchemyParcelleRepository,
    )

    assert isinstance(
        service.weather,
        OpenWeatherMapProvider,
    )
