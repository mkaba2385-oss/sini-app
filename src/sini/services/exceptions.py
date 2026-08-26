class SiniServiceError(Exception):
    """Base exception pour la couche service de Sini."""

    pass


class EntityNotFoundError(SiniServiceError):
    """Levée lorsqu'une ressource recherchée n'existe pas."""

    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} avec l'ID {entity_id} introuvable.")


class PermissionDeniedError(SiniServiceError):
    """Levée lorsqu'un utilisateur n'a pas la permission d'accéder à une ressource."""

    def __init__(self, message: str = "Accès non autorisé à cette ressource."):
        super().__init__(message)


class UnauthorizedAccessError(SiniServiceError):
    """Levée lorsqu'un utilisateur tente d'accéder à une ressource non autorisée."""

    def __init__(self) -> None:
        super().__init__("Vous n'êtes pas autorisé à accéder à cette ressource.")
