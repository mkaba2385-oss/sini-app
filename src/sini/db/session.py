from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from sini.db.config import DATABASE_URL

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL n'est pas configurée.")

database_url = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg://",
    1,
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


def get_session() -> Generator[Session, None, None]:
    """Fournit une session SQLAlchemy et gère la transaction."""

    session = SessionLocal()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
