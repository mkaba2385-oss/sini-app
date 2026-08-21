"""ajout saisons et récoltes

Revision ID: 7a2d1f5c9b31
Revises: 103bbbac3930
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "7a2d1f5c9b31"
down_revision: Union[str, Sequence[str], None] = "103bbbac3930"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.CheckConstraint("end_date >= start_date", name="ck_seasons_dates"),
        sa.CheckConstraint("year >= 2000", name="ck_seasons_year"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_seasons_year"), "seasons", ["year"], unique=False)

    op.create_table(
        "harvests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("parcelle_id", sa.Integer(), nullable=False),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("quantite_recoltee", sa.Float(), nullable=False),
        sa.Column("unite", sa.String(length=20), nullable=False),
        sa.Column("date_recolte", sa.Date(), nullable=False),
        sa.CheckConstraint(
            "quantite_recoltee > 0", name="ck_harvests_quantity_positive"
        ),
        sa.ForeignKeyConstraint(["parcelle_id"], ["parcelles.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["season_id"], ["seasons.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_harvests_parcelle_id"), "harvests", ["parcelle_id"], unique=False
    )
    op.create_index(
        op.f("ix_harvests_season_id"), "harvests", ["season_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_harvests_season_id"), table_name="harvests")
    op.drop_index(op.f("ix_harvests_parcelle_id"), table_name="harvests")
    op.drop_table("harvests")
    op.drop_index(op.f("ix_seasons_year"), table_name="seasons")
    op.drop_table("seasons")
