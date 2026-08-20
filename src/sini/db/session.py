from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from sini.db.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    """Fournit une session SQLAlchemy et la ferme après utilisation."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
