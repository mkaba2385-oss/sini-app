from sini.observers.base import EventPublisher
from sini.observers.sms_observer import SmsNotificationObserver
from sini.repositories.memory import InMemoryParcelleRepository
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway
from sini.services.weather import MockWeatherProvider
from sini.strategies.alert_strategy import DroughtAlertStrategy


class ServiceFactory:
    """Factory dédiée à la création et au câblage de ParcelleService."""

    @staticmethod
    def create_parcelle_service(env: str = "dev") -> ParcelleService:
        repo = InMemoryParcelleRepository()

        if env == "prod":
            raise NotImplementedError(
                "Les services de production ne sont pas encore configurés."
            )

        weather = MockWeatherProvider()
        sms = ConsoleSmsGateway()

        publisher = EventPublisher()
        sms_observer = SmsNotificationObserver(sms_gateway=sms)
        publisher.attach(sms_observer)

        alert_strategy = DroughtAlertStrategy()

        return ParcelleService(
            repository=repo,
            weather_provider=weather,
            publisher=publisher,
            alert_strategy=alert_strategy,
        )
