from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from sini.models.diagnostic import DiagnosticModel
from sini.models.journal import JournalEntryModel
from sini.models.parcelle import ParcelleModel
from sini.models.photo import PhotoModel
from sini.models.prix import PrixModel
from sini.models.user import UserModel
from sini.repositories.base import RepositoryInterface
from sini.schemas.diagnostic import DiagnosticResponse
from sini.schemas.journal import JournalEntryResponse
from sini.schemas.parcelle import ParcelleResponse
from sini.schemas.photo import PhotoResponse
from sini.schemas.prix import PrixResponse
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


class SqlAlchemyUserRepository(RepositoryInterface[UserResponse]):
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


class SqlAlchemyPhotoRepository:
    """Repository SQLAlchemy pour les photos."""

    def __init__(self, session: Session) -> None:
        self.session = session

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
        return [PhotoResponse.model_validate(m) for m in self.session.scalars(stmt)]


class SqlAlchemyPrixRepository:
    """Repository SQLAlchemy pour les relevés de prix."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, entity: PrixResponse) -> PrixResponse:
        data = _values(entity)
        data.pop("id", None)
        data.pop("created_at", None)
        model = PrixModel(**data)
        self.session.add(model)
        self.session.flush()
        return PrixResponse.model_validate(model)

    def get_by_id(self, entity_id: int) -> PrixResponse | None:
        model = self.session.get(PrixModel, entity_id)
        return None if model is None else PrixResponse.model_validate(model)

    def get_all(self) -> list[PrixResponse]:
        stmt = select(PrixModel).order_by(PrixModel.date_releve, PrixModel.id)
        return [PrixResponse.model_validate(m) for m in self.session.scalars(stmt)]


class SqlAlchemyDiagnosticRepository:
    """Repository SQLAlchemy pour les diagnostics."""

    def __init__(self, session: Session) -> None:
        self.session = session

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
            DiagnosticResponse.model_validate(m) for m in self.session.scalars(stmt)
        ]
