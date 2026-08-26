from sqlalchemy.orm import Session

from sini.observers.base import EventPublisher
from sini.observers.sms_observer import SmsNotificationObserver
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
from sini.services.sms import ConsoleSmsGateway
from sini.services.token_service import TokenService
from sini.services.user_service import UserService
from sini.services.weather import MockWeatherProvider
from sini.strategies.alert_strategy import DroughtAlertStrategy

otp_service = OtpService()


class ServiceFactory:
    """Factory dédiée au câblage des services."""

    @staticmethod
    def create_parcelle_service(
        env: str = "dev",
        session: Session | None = None,
    ) -> ParcelleService:
        """Crée un ParcelleService avec le repository adapté."""

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

        sms_gateway = ConsoleSmsGateway()
        token_service = TokenService()

        return AuthService(
            user_service=user_service,
            otp_service=otp_service,
            sms_gateway=sms_gateway,
            token_service=token_service,
        )
