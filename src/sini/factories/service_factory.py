from sini.repositories.memory import InMemoryParcelleRepository
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway
from sini.services.weather import MockWeatherProvider


class ServiceFactory:
    """Factory dédiée à la création et à l'injection de dépendances de ParcelleService."""

    @staticmethod
    def create_parcelle_service(env: str = "dev") -> ParcelleService:
        repo = InMemoryParcelleRepository()

        if env == "prod":
            raise NotImplementedError(
                "Les services de production (Base de données, API Météo, Gateway SMS) ne sont pas encore configurés."
            )

        weather = MockWeatherProvider()
        sms = ConsoleSmsGateway()

        return ParcelleService(
            repository=repo,
            weather_provider=weather,
            sms_gateway=sms,
        )