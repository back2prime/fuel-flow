"""add max length constraints to user fields

Revision ID: 6c3714e4f91b
Revises: 2ecabec2081f
Create Date: 2026-06-12 21:07:56.741482

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6c3714e4f91b"
down_revision: Union[str, Sequence[str], None] = "2ecabec2081f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
