"""remove is_open from favourites

Revision ID: 2ecabec2081f
Revises: b2ef56ad218f
Create Date: 2026-06-12 20:11:20.779763

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2ecabec2081f"
down_revision: Union[str, Sequence[str], None] = "b2ef56ad218f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("favourites", "is_open")


def downgrade() -> None:
    op.add_column("favourites", sa.Column("is_open", sa.Boolean(), nullable=True))
