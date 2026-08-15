import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar, cast

# Configuration basique du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sini.services")

F = TypeVar("F", bound=Callable[..., Any])


def timer(func: F) -> F:
    """Décorateur pour mesurer le temps d'exécution d'une méthode de service."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"[PERF] {func.__name__} a pris {elapsed:.6f}s")
        return result

    return cast(F, wrapper)
