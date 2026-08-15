from sini.factories.service_factory import ServiceFactory
from sini.schemas.parcelle import (
    CultureType,
    ParcelleCreate,
    ParcelleUpdate,
    RegionMali,
)
from sini.services.exceptions import EntityNotFoundError


def main() -> None:
    print("Démarrage de l'application Sini (Validation Semaine 4)...\n")

    # 1. Instanciation du service via la Factory
    service = ServiceFactory.create_parcelle_service(env="dev")

    # 2. Création d'une parcelle
    print("--- 1. Création d'une parcelle ---")
    nouvelle_parcelle_data = ParcelleCreate(
        name="Champ de Coton de Ségou",
        superficie_ha=4.5,
        culture=CultureType.COTON,
        region=RegionMali.SEGOU,
        commune="Pelengana",
        owner_id=1,
    )

    parcelle = service.create_parcelle(nouvelle_parcelle_data)
    print(
        f"[OK] Parcelle créée avec succès !"
        f"\n   ID: {parcelle.id}"
        f"\n   Nom: {parcelle.name}"
        f"\n   Région: {parcelle.region.value}"
        f"\n   Date de création: {parcelle.created_at}\n"
    )

    # 3. Récupération par ID
    print("--- 2. Récupération par ID ---")
    parcelle_recuperee = service.get_by_id(parcelle.id)
    print(f"Parcelle retrouvée: {parcelle_recuperee.name}\n")

    # 4. Mise à jour partielle
    print("--- 3. Mise à jour de la parcelle ---")
    update_data = ParcelleUpdate(superficie_ha=6.0, commune="Ségou Coura")
    parcelle_maj = service.updated_parcelle(parcelle.id, update_data)
    print(
        f"[OK] Parcelle mise à jour !"
        f"\n   Nouvelle superficie: {parcelle_maj.superficie_ha} ha"
        f"\n   Nouvelle commune: {parcelle_maj.commune}"
        f"\n   Dernière modification: {parcelle_maj.update_at}\n"
    )

    # 5. Test du service d'alerte Météo + SMS
    print("--- 4. Test du workflow Météo + SMS ---")
    service.verifier_et_alerter(
        parcelle_id=parcelle.id,
        telephone_owner="+22370000000",  # Format Mali
    )
    print()

    # 6. Suppression et vérification de la gestion d'erreur
    print("--- 5. Test de suppression et gestion des erreurs ---")
    service.delete_parcelle(parcelle.id)
    print(f"Parcelle ID {parcelle.id} supprimée.")

    try:
        service.get_by_id(parcelle.id)
    except EntityNotFoundError as e:
        print(f"[OK] Exception attrapée avec succès: {e}\n")

    print("Tous les tests manuels du main.py ont réussi !")


if __name__ == "__main__":
    main()
