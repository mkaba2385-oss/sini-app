from datetime import date
from typing import Optional


class JournalEntry:
    """Modèle domaine pour une activité consignée sur une parcelle."""

    DEVISE = "FCFA"  # Attribut de classe

    def __init__(
        self,
        entry_id: int,
        parcelle_id: int,
        action: str,
        description: str,
        cout_fcfa: float = 0.0,
        entry_date: Optional[date] = None,
    ) -> None:
        self.id = entry_id
        self.parcelle_id = parcelle_id
        self.action = action
        self.description = description
        self._cout_fcfa = cout_fcfa
        self.entry_date = entry_date or date.today()

    @property
    def cout_fcfa(self) -> float:
        return self._cout_fcfa

    @cout_fcfa.setter
    def cout_fcfa(self, montant: float) -> None:
        """Validation via Property."""
        if montant < 0:
            raise ValueError("Le coût d'une activité ne peut pas être négatif.")
        self._cout_fcfa = montant

    def to_summary(self) -> str:
        """Résumé formaté de l'activité."""
        cost_info = (
            f" ({self.cout_fcfa} {self.DEVISE})" if self.cout_fcfa > 0 else ""
        )
        date_str = self.entry_date.strftime("%d/%m/%Y")
        return f"[{date_str}] {self.action}: {self.description}{cost_info}"

    def __repr__(self) -> str:
        return (
            f"<JournalEntry id={self.id} action='{self.action}' "
            f"date='{self.entry_date}'>"
        )