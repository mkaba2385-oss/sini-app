from sqlalchemy.orm import Session

from sini.observers.base import EventPublisher
from sini.observers.sms_observer import SmsNotificationObserver
from sini.repositories.base import RepositoryInterface
from sini.repositories.memory import InMemoryParcelleRepository
from sini.repositories.sqlalchemy import SqlAlchemyParcelleRepository
from sini.schemas.parcelle import ParcelleResponse
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway
from sini.services.weather import MockWeatherProvider
from sini.strategies.alert_strategy import DroughtAlertStrategy


class ServiceFactory:
    """Factory dédiée au câblage de ParcelleService."""

    @staticmethod
    def create_parcelle_service(
        env: str = "dev", session: Session | None = None
    ) -> ParcelleService:
        """Crée un service avec le repository adapté à l'environnement.

        ``dev`` conserve l'InMemory pour les tests unitaires.
        ``prod`` utilise SQLAlchemy avec une session injectée par l'appelant.
        """
        repo: RepositoryInterface[ParcelleResponse]

        if env == "dev":
            repo = InMemoryParcelleRepository()
        elif env == "prod":
            if session is None:
                raise ValueError(
                    "Une session SQLAlchemy doit être fournie pour "
                    "l'environnement prod."
                )
            repo = SqlAlchemyParcelleRepository(session)
        else:
            raise ValueError(f"Environnement inconnu : {env!r}")

        weather = MockWeatherProvider()
        sms = ConsoleSmsGateway()

        publisher = EventPublisher()
        sms_observer = SmsNotificationObserver(sms_gateway=sms)
        publisher.attach(sms_observer)

        return ParcelleService(
            repository=repo,
            weather_provider=weather,
            publisher=publisher,
            alert_strategy=DroughtAlertStrategy(),
        )
