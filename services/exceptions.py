class SiniServiceError(Exception):
    """Base exception pour la couche service de Sini."""
    pass

class EntityNotFoundError(SiniServiceError):
    """Levée lorsqu'une ressource recherchée n'existe pas."""
    def __init__(self, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} avec l'ID {entity_id} introuvable.")
        