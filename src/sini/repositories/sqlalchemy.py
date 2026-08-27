from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from sini.models.diagnostic import DiagnosticModel
from sini.models.harvest import HarvestModel
from sini.models.journal import JournalEntryModel
from sini.models.parcelle import ParcelleModel
from sini.models.photo import PhotoModel
from sini.models.prix import PrixModel
from sini.models.season import SeasonModel
from sini.models.user import UserModel
from sini.repositories.base import (
    PrixRepositoryInterface,
    RepositoryInterface,
    UserRepositoryInterface,
)
from sini.schemas.diagnostic import DiagnosticResponse
from sini.schemas.harvest import HarvestResponse
from sini.schemas.journal import JournalEntryResponse
from sini.schemas.parcelle import CultureType, ParcelleResponse
from sini.schemas.photo import PhotoResponse
from sini.schemas.prix import PrixResponse
from sini.schemas.season import SeasonResponse
from sini.schemas.user import UserResponse


def _values(entity: BaseModel) -> dict[str, Any]:
    """Retourne les champs persistables d'un schema Pydantic."""
    return entity.model_dump()


class SqlAlchemyParcelleRepository(RepositoryInterface[ParcelleResponse]):
    """Repository PostgreSQL/SQLAlchemy pour les parcelles."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, entity: ParcelleResponse) -> ParcelleResponse:
        data = _values(entity)
        data.pop("id", None)
        model = ParcelleModel(**data)
        self.session.add(model)
        self.session.flush()
        return ParcelleResponse.model_validate(model)

    def add(self, entity: ParcelleResponse) -> ParcelleResponse:
        model = self.session.get(ParcelleModel, entity.id)
        data = _values(entity)
        if model is None:
            model = ParcelleModel(**data)
            self.session.add(model)
        else:
            for key, value in data.items():
                setattr(model, key, value)
        self.session.flush()
        return ParcelleResponse.model_validate(model)

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def get_by_id(self, entity_id: int) -> ParcelleResponse | None:
        model = self.session.get(ParcelleModel, entity_id)
        return None if model is None else ParcelleResponse.model_validate(model)

    def get_all(self) -> list[ParcelleResponse]:
        stmt = select(ParcelleModel).order_by(ParcelleModel.id)
        return [ParcelleResponse.model_validate(m) for m in self.session.scalars(stmt)]

    def delete(self, entity_id: int) -> None:
        self.session.execute(delete(ParcelleModel).where(ParcelleModel.id == entity_id))
        self.session.flush()


class SqlAlchemyUserRepository(UserRepositoryInterface):
    """Repository PostgreSQL/SQLAlchemy pour les utilisateurs."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, entity: UserResponse) -> UserResponse:
        data = _values(entity)
        data.pop("id", None)
        model = UserModel(**data)
        self.session.add(model)
        self.session.flush()
        return UserResponse.model_validate(model)

    def add(self, entity: UserResponse) -> UserResponse:
        model = self.session.get(UserModel, entity.id)
        data = _values(entity)
        if model is None:
            model = UserModel(**data)
            self.session.add(model)
        else:
            for key, value in data.items():
                setattr(model, key, value)
        self.session.flush()
        return UserResponse.model_validate(model)

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def get_by_id(self, entity_id: int) -> UserResponse | None:
        model = self.session.get(UserModel, entity_id)
        return None if model is None else UserResponse.model_validate(model)

    def get_all(self) -> list[UserResponse]:
        stmt = select(UserModel).order_by(UserModel.id)
        return [UserResponse.model_validate(m) for m in self.session.scalars(stmt)]

    def delete(self, entity_id: int) -> None:
        self.session.execute(delete(UserModel).where(UserModel.id == entity_id))
        self.session.flush()

    def get_by_phone(self, phone_number: str) -> UserResponse | None:
        stmt = select(UserModel).where(UserModel.phone_number == phone_number)
        model = self.session.scalar(stmt)
        return None if model is None else UserResponse.model_validate(model)


class SqlAlchemyJournalRepository(RepositoryInterface[JournalEntryResponse]):
    """Repository PostgreSQL/SQLAlchemy pour le journal agricole."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, entity: JournalEntryResponse) -> JournalEntryResponse:
        data = _values(entity)
        data.pop("id", None)
        model = JournalEntryModel(**data)
        self.session.add(model)
        self.session.flush()
        return JournalEntryResponse.model_validate(model)

    def add(self, entity: JournalEntryResponse) -> JournalEntryResponse:
        model = self.session.get(JournalEntryModel, entity.id)
        data = _values(entity)
        if model is None:
            model = JournalEntryModel(**data)
            self.session.add(model)
        else:
            for key, value in data.items():
                setattr(model, key, value)
        self.session.flush()
        return JournalEntryResponse.model_validate(model)

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def get_by_id(self, entity_id: int) -> JournalEntryResponse | None:
        model = self.session.get(JournalEntryModel, entity_id)
        return None if model is None else JournalEntryResponse.model_validate(model)

    def get_all(self) -> list[JournalEntryResponse]:
        stmt = select(JournalEntryModel).order_by(JournalEntryModel.id)
        return [
            JournalEntryResponse.model_validate(m) for m in self.session.scalars(stmt)
        ]

    def delete(self, entity_id: int) -> None:
        self.session.execute(
            delete(JournalEntryModel).where(JournalEntryModel.id == entity_id)
        )
        self.session.flush()

    def list_by_parcelle(self, parcelle_id: int) -> list[JournalEntryResponse]:
        stmt = (
            select(JournalEntryModel)
            .where(JournalEntryModel.parcelle_id == parcelle_id)
            .order_by(JournalEntryModel.created_at)
        )
        return [
            JournalEntryResponse.model_validate(m) for m in self.session.scalars(stmt)
        ]


class SqlAlchemyPhotoRepository(RepositoryInterface[PhotoResponse]):
    """Repository SQLAlchemy pour les photos."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def create(self, entity: PhotoResponse) -> PhotoResponse:
        data = _values(entity)
        data.pop("id", None)
        data.pop("created_at", None)

        model = PhotoModel(**data)
        self.session.add(model)
        self.session.flush()

        return PhotoResponse.model_validate(model)

    def get_by_id(self, entity_id: int) -> PhotoResponse | None:
        model = self.session.get(PhotoModel, entity_id)

        return None if model is None else PhotoResponse.model_validate(model)

    def get_all(self) -> list[PhotoResponse]:
        stmt = select(PhotoModel).order_by(PhotoModel.id)

        return [
            PhotoResponse.model_validate(model) for model in self.session.scalars(stmt)
        ]

    def add(self, entity: PhotoResponse) -> PhotoResponse:
        model = self.session.get(PhotoModel, entity.id)
        data = _values(entity)

        if model is None:
            model = PhotoModel(**data)
            self.session.add(model)
        else:
            for key, value in data.items():
                setattr(model, key, value)

        self.session.flush()

        return PhotoResponse.model_validate(model)

    def delete(self, entity_id: int) -> None:
        self.session.execute(delete(PhotoModel).where(PhotoModel.id == entity_id))
        self.session.flush()


class SqlAlchemyPrixRepository(PrixRepositoryInterface):
    """Repository SQLAlchemy pour les relevés de prix."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def create(self, entity: PrixResponse) -> PrixResponse:
        """Crée un nouveau relevé de prix."""

        data = _values(entity)

        data.pop("id", None)
        data.pop("created_at", None)

        model = PrixModel(**data)

        self.session.add(model)
        self.session.flush()

        return PrixResponse.model_validate(model)

    def get_by_id(self, entity_id: int) -> PrixResponse | None:
        """Récupère un prix par son ID."""

        model = self.session.get(
            PrixModel,
            entity_id,
        )

        if model is None:
            return None

        return PrixResponse.model_validate(model)

    def get_all(self) -> list[PrixResponse]:
        """Récupère tous les relevés de prix."""

        stmt = select(PrixModel).order_by(
            PrixModel.date_releve,
            PrixModel.id,
        )

        return [
            PrixResponse.model_validate(model) for model in self.session.scalars(stmt)
        ]

    def add(self, entity: PrixResponse) -> PrixResponse:
        """Ajoute ou met à jour un relevé."""

        model = self.session.get(
            PrixModel,
            entity.id,
        )

        data = _values(entity)

        if model is None:
            model = PrixModel(**data)
            self.session.add(model)
        else:
            for key, value in data.items():
                if key != "id":
                    setattr(model, key, value)

        self.session.flush()

        return PrixResponse.model_validate(model)

    def delete(self, entity_id: int) -> None:
        """Supprime un relevé de prix."""

        model = self.session.get(
            PrixModel,
            entity_id,
        )

        if model is not None:
            self.session.delete(model)
            self.session.flush()

    def list_by_culture(
        self,
        culture: CultureType,
    ) -> list[PrixResponse]:
        """Récupère tous les prix pour une culture."""

        stmt = (
            select(PrixModel)
            .where(PrixModel.culture == culture)
            .order_by(
                PrixModel.date_releve,
                PrixModel.id,
            )
        )

        return [
            PrixResponse.model_validate(model) for model in self.session.scalars(stmt)
        ]

    def list_by_marche(
        self,
        marche: str,
    ) -> list[PrixResponse]:
        """Récupère tous les prix d'un marché."""

        stmt = (
            select(PrixModel)
            .where(PrixModel.marche == marche)
            .order_by(
                PrixModel.date_releve,
                PrixModel.id,
            )
        )

        return [
            PrixResponse.model_validate(model) for model in self.session.scalars(stmt)
        ]

    def list_by_culture_and_marche(
        self,
        culture: CultureType,
        marche: str,
    ) -> list[PrixResponse]:
        """Récupère les prix d'une culture sur un marché."""

        stmt = (
            select(PrixModel)
            .where(
                PrixModel.culture == culture,
                PrixModel.marche == marche,
            )
            .order_by(
                PrixModel.date_releve,
                PrixModel.id,
            )
        )

        return [
            PrixResponse.model_validate(model) for model in self.session.scalars(stmt)
        ]


class SqlAlchemyDiagnosticRepository(RepositoryInterface[DiagnosticResponse]):
    """Repository SQLAlchemy pour les diagnostics."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def create(self, entity: DiagnosticResponse) -> DiagnosticResponse:
        data = _values(entity)
        data.pop("id", None)
        data.pop("created_at", None)

        model = DiagnosticModel(**data)
        self.session.add(model)
        self.session.flush()

        return DiagnosticResponse.model_validate(model)

    def get_by_id(self, entity_id: int) -> DiagnosticResponse | None:
        model = self.session.get(DiagnosticModel, entity_id)

        return None if model is None else DiagnosticResponse.model_validate(model)

    def get_all(self) -> list[DiagnosticResponse]:
        stmt = select(DiagnosticModel).order_by(DiagnosticModel.id)

        return [
            DiagnosticResponse.model_validate(model)
            for model in self.session.scalars(stmt)
        ]

    def add(self, entity: DiagnosticResponse) -> DiagnosticResponse:
        model = self.session.get(DiagnosticModel, entity.id)
        data = _values(entity)

        if model is None:
            model = DiagnosticModel(**data)
            self.session.add(model)
        else:
            for key, value in data.items():
                setattr(model, key, value)

        self.session.flush()

        return DiagnosticResponse.model_validate(model)

    def delete(self, entity_id: int) -> None:
        self.session.execute(
            delete(DiagnosticModel).where(DiagnosticModel.id == entity_id)
        )
        self.session.flush()


class SqlAlchemyHarvestRepository(RepositoryInterface[HarvestResponse]):
    """Repository SQLAlchemy pour les récoltes."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def create(self, entity: HarvestResponse) -> HarvestResponse:
        data = _values(entity)
        data.pop("id", None)

        model = HarvestModel(**data)
        self.session.add(model)
        self.session.flush()

        return HarvestResponse.model_validate(model)

    def get_by_id(self, entity_id: int) -> HarvestResponse | None:
        model = self.session.get(HarvestModel, entity_id)

        return None if model is None else HarvestResponse.model_validate(model)

    def get_all(self) -> list[HarvestResponse]:
        stmt = select(HarvestModel).order_by(HarvestModel.id)

        return [
            HarvestResponse.model_validate(model)
            for model in self.session.scalars(stmt)
        ]

    def add(self, entity: HarvestResponse) -> HarvestResponse:
        model = self.session.get(HarvestModel, entity.id)

        if model is None:
            raise ValueError(f"Récolte avec l'ID {entity.id} introuvable.")

        data = _values(entity)

        for key, value in data.items():
            if key != "id":
                setattr(model, key, value)

        self.session.flush()

        return HarvestResponse.model_validate(model)

    def delete(self, entity_id: int) -> None:
        model = self.session.get(HarvestModel, entity_id)

        if model is not None:
            self.session.delete(model)
            self.session.flush()


class SqlAlchemySeasonRepository(RepositoryInterface[SeasonResponse]):
    """Repository SQLAlchemy pour les saisons."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_next_id(self) -> int:
        raise RuntimeError("Les IDs PostgreSQL sont générés par la base via create().")

    def create(self, entity: SeasonResponse) -> SeasonResponse:
        data = _values(entity)
        data.pop("id", None)

        model = SeasonModel(**data)
        self.session.add(model)
        self.session.flush()

        return SeasonResponse.model_validate(model)

    def get_by_id(self, entity_id: int) -> SeasonResponse | None:
        model = self.session.get(SeasonModel, entity_id)

        return None if model is None else SeasonResponse.model_validate(model)

    def get_all(self) -> list[SeasonResponse]:
        stmt = select(SeasonModel).order_by(
            SeasonModel.year,
            SeasonModel.start_date,
        )

        return [
            SeasonResponse.model_validate(model) for model in self.session.scalars(stmt)
        ]

    def add(self, entity: SeasonResponse) -> SeasonResponse:
        model = self.session.get(SeasonModel, entity.id)

        if model is None:
            raise ValueError(f"Saison avec l'ID {entity.id} introuvable.")

        data = _values(entity)

        for key, value in data.items():
            if key != "id":
                setattr(model, key, value)

        self.session.flush()

        return SeasonResponse.model_validate(model)

    def delete(self, entity_id: int) -> None:
        model = self.session.get(SeasonModel, entity_id)

        if model is not None:
            self.session.delete(model)
            self.session.flush()
