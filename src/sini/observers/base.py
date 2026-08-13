from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Event:
    """Structure d'un événement métier."""

    name: str
    payload: dict[str, Any]


class Observer(ABC):
    """Interface d'un observateur."""

    @abstractmethod
    def update(self, event: Event) -> None:
        pass


class EventPublisher:
    """Gestionnaire de publication d'événements."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: Event) -> None:
        for observer in self._observers:
            observer.update(event)
