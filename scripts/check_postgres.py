"""Vérifie que Sini peut se connecter à PostgreSQL."""

import logging

from sqlalchemy import text

from sini.db.session import engine

logger = logging.getLogger(__name__)


def main() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        logger.info("Connexion PostgreSQL OK : %s", result.scalar_one())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
