from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from sini.api.dependencies import CurrentAdminDep, CurrentUserDep
from sini.db.session import get_session
from sini.factories.service_factory import ServiceFactory
from sini.schemas.parcelle import CultureType
from sini.schemas.prix import (
    PrixCreate,
    PrixPredictionResponse,
    PrixResponse,
    PrixUpdate,
    UnitePrix,
)
from sini.services.exceptions import EntityNotFoundError
from sini.services.prix_service import PrixService

router = APIRouter(
    prefix="/prix",
    tags=["Prix"],
)


SessionDep = Annotated[
    Session,
    Depends(get_session),
]


def get_prix_service(
    session: SessionDep,
) -> PrixService:
    """Crée un PrixService avec le modèle Random Forest."""

    return ServiceFactory.create_prix_service(session)


PrixServiceDep = Annotated[
    PrixService,
    Depends(get_prix_service),
]


@router.post(
    "",
    response_model=PrixResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prix(
    data: PrixCreate,
    service: PrixServiceDep,
    current_admin: CurrentAdminDep,
) -> PrixResponse:
    """Crée un nouveau relevé de prix."""

    try:
        return service.create(data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PrixResponse],
)
def get_all_prix(
    service: PrixServiceDep,
    current_user: CurrentUserDep,
) -> list[PrixResponse]:
    """Récupère tous les relevés de prix."""

    return service.get_all()


@router.get(
    "/culture/{culture}",
    response_model=list[PrixResponse],
)
def get_prix_by_culture(
    culture: CultureType,
    service: PrixServiceDep,
    current_user: CurrentUserDep,
) -> list[PrixResponse]:
    """Récupère les relevés de prix pour une culture."""

    return service.list_by_culture(culture)


@router.get(
    "/marche/{marche}",
    response_model=list[PrixResponse],
)
def get_prix_by_marche(
    marche: str,
    service: PrixServiceDep,
    current_user: CurrentUserDep,
) -> list[PrixResponse]:
    """Récupère les relevés de prix pour un marché."""

    return service.list_by_marche(marche)


@router.get("/prediction", response_model=PrixPredictionResponse)
def predict_prix(
    culture: CultureType,
    marche: str,
    target_date: date,
    service: PrixServiceDep,
    current_user: CurrentUserDep,
) -> PrixPredictionResponse:
    """Prédit le prix d'une culture sur un marché."""
    try:
        prediction = service.predict_price(
            culture=culture,
            marche=marche,
            target_date=target_date,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return PrixPredictionResponse(
        culture=culture,
        marche=marche,
        date_prediction=target_date,
        prix_predit=prediction,
        unite=UnitePrix.KG,
    )


@router.get(
    "/{prix_id}",
    response_model=PrixResponse,
)
def get_prix(
    prix_id: int,
    service: PrixServiceDep,
    current_user: CurrentUserDep,
) -> PrixResponse:
    """Récupère un relevé de prix par son ID."""

    try:
        return service.get_by_id(prix_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{prix_id}",
    response_model=PrixResponse,
)
def update_prix(
    prix_id: int,
    data: PrixUpdate,
    service: PrixServiceDep,
    current_admin: CurrentAdminDep,
) -> PrixResponse:
    """Met à jour un relevé de prix."""

    try:
        return service.update(prix_id, data)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{prix_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_prix(
    prix_id: int,
    service: PrixServiceDep,
    current_admin: CurrentAdminDep,
) -> Response:
    """Supprime un relevé de prix."""

    try:
        service.delete(prix_id)
    except EntityNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
