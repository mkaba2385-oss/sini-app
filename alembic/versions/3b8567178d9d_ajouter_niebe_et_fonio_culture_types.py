"""ajouter  niebe et  fonio culture types

Revision ID: 3b8567178d9d
Revises: 7a2d1f5c9b31
Create Date: 2026-09-04 15:04:55.615959

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3b8567178d9d'
down_revision: Union[str, Sequence[str], None] = '7a2d1f5c9b31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute Niébé et Fonio à l'ENUM culture_type."""
    op.execute("ALTER TYPE culture_type ADD VALUE IF NOT EXISTS 'NIEBE'")
    op.execute("ALTER TYPE culture_type ADD VALUE IF NOT EXISTS 'FONIO'")


def downgrade() -> None:
    """Les valeurs d'un ENUM PostgreSQL ne sont pas supprimées directement."""
    pass