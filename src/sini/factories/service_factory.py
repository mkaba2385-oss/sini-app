from sqlalchemy.orm import Session

from sini.config import (
    AFRICASTALKING_API_KEY,
    AFRICASTALKING_USERNAME,
    OPENWEATHER_API_KEY,
)
from sini.observers.base import EventPublisher
from sini.observers.sms_observer import SmsNotificationObserver
from sini.providers.africa_talking import AfricaTalkingSmsGateway
from sini.providers.openweather import OpenWeatherMapProvider
from sini.repositories.base import RepositoryInterface, UserRepositoryInterface
from sini.repositories.memory import (
    InMemoryParcelleRepository,
    InMemoryUserRepository,
)
from sini.repositories.sqlalchemy import (
    SqlAlchemyParcelleRepository,
    SqlAlchemyUserRepository,
)
from sini.schemas.parcelle import ParcelleResponse
from sini.services.auth_service import AuthService
from sini.services.otp_service import OtpService
from sini.services.parcelle_service import ParcelleService
from sini.services.sms import ConsoleSmsGateway, SmsGateway
from sini.services.token_service import TokenService
from sini.services.user_service import UserService
from sini.services.weather import MockWeatherProvider, WeatherProvider
from sini.strategies.alert_strategy import DroughtAlertStrategy

otp_service = OtpService()


class ServiceFactory:
    """Factory dédiée au câblage des services."""

    @staticmethod
    def _create_sms_gateway(env: str) -> SmsGateway:
        """Crée le gateway SMS adapté à l'environnement."""

        if env == "dev":
            return ConsoleSmsGateway()

        if env == "prod":
            if AFRICASTALKING_USERNAME is None:
                raise ValueError(
                    "AFRICASTALKING_USERNAME doit être définie "
                    "pour utiliser Africa's Talking en production."
                )

            if AFRICASTALKING_API_KEY is None:
                raise ValueError(
                    "AFRICASTALKING_API_KEY doit être définie "
                    "pour utiliser Africa's Talking en production."
                )

            return AfricaTalkingSmsGateway(
                username=AFRICASTALKING_USERNAME,
                api_key=AFRICASTALKING_API_KEY,
            )

        raise ValueError(f"Environnement inconnu : {env!r}")

    @staticmethod
    def create_parcelle_service(
        env: str = "dev",
        session: Session | None = None,
    ) -> ParcelleService:
        """Crée un ParcelleService avec les dépendances adaptées."""

        repo: RepositoryInterface[ParcelleResponse]
        weather: WeatherProvider

        if env == "dev":
            repo = InMemoryParcelleRepository()
            weather = MockWeatherProvider()

        elif env == "prod":
            if session is None:
                raise ValueError(
                    "Une session SQLAlchemy doit être fournie pour "
                    "l'environnement prod."
                )

            if OPENWEATHER_API_KEY is None:
                raise ValueError(
                    "OPENWEATHER_API_KEY doit être définie "
                    "pour utiliser OpenWeatherMap en production."
                )

            repo = SqlAlchemyParcelleRepository(session)

            weather = OpenWeatherMapProvider(
                api_key=OPENWEATHER_API_KEY,
            )

        else:
            raise ValueError(f"Environnement inconnu : {env!r}")

        sms = ServiceFactory._create_sms_gateway(env)

        publisher = EventPublisher()

        sms_observer = SmsNotificationObserver(
            sms_gateway=sms,
        )

        publisher.attach(sms_observer)

        return ParcelleService(
            repository=repo,
            weather_provider=weather,
            publisher=publisher,
            alert_strategy=DroughtAlertStrategy(),
        )

    @staticmethod
    def create_user_service(
        env: str = "dev",
        session: Session | None = None,
    ) -> UserService:
        """Crée un UserService avec le repository adapté."""

        repo: UserRepositoryInterface

        if env == "dev":
            repo = InMemoryUserRepository()

        elif env == "prod":
            if session is None:
                raise ValueError(
                    "Une session SQLAlchemy doit être fournie pour "
                    "l'environnement prod."
                )

            repo = SqlAlchemyUserRepository(session)

        else:
            raise ValueError(f"Environnement inconnu : {env!r}")

        return UserService(
            repository=repo,
        )

    @staticmethod
    def create_auth_service(
        env: str = "dev",
        session: Session | None = None,
    ) -> AuthService:
        """Crée le service d'authentification."""

        user_service = ServiceFactory.create_user_service(
            env=env,
            session=session,
        )

        sms_gateway = ServiceFactory._create_sms_gateway(env)

        token_service = TokenService()

        return AuthService(
            user_service=user_service,
            otp_service=otp_service,
            sms_gateway=sms_gateway,
            token_service=token_service,
        )
