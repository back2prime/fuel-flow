"""add max length constraints to user fields

Revision ID: 62eecbb19cbc
Revises: 6c3714e4f91b
Create Date: 2026-06-12 21:11:52.435390

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "62eecbb19cbc"
down_revision: Union[str, Sequence[str], None] = "6c3714e4f91b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "name", type_=sa.String(50))
    op.alter_column("users", "surname", type_=sa.String(50))


def downgrade() -> None:
    op.alter_column("users", "name", type_=sa.String())
    op.alter_column("users", "surname", type_=sa.String())
