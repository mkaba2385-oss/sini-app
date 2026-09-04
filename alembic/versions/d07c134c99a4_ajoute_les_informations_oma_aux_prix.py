"""ajoute les informations OMA aux prix

Revision ID: d07c134c99a4
Revises: 3b8567178d9d
Create Date: 2026-09-04 15:56:58.502588

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d07c134c99a4"
down_revision: Union[str, Sequence[str], None] = "3b8567178d9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ajoute les informations nécessaires aux prix OMA."""

    op.add_column(
        "prices",
        sa.Column(
            "variete",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "prices",
        sa.Column(
            "type_prix",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "prices",
        sa.Column(
            "source",
            sa.String(length=255),
            nullable=True,
        ),
    )

    # Les anciens prix présents en base proviennent de l'OMA.
    # Leur type précis n'était pas conservé dans l'ancien modèle.
    op.execute(
        """
        UPDATE prices
        SET type_prix = 'detaillant',
            source = 'OMA'
        WHERE type_prix IS NULL
        """
    )

    op.alter_column(
        "prices",
        "type_prix",
        existing_type=sa.String(length=50),
        nullable=False,
    )

    op.alter_column(
        "prices",
        "source",
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.create_index(
        "ix_prices_type_prix",
        "prices",
        ["type_prix"],
    )


def downgrade() -> None:
    """Supprime les informations ajoutées aux prix."""

    op.drop_index(
        "ix_prices_type_prix",
        table_name="prices",
    )

    op.drop_column("prices", "source")
    op.drop_column("prices", "type_prix")
    op.drop_column("prices", "variete")