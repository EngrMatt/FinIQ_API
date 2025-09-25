"""add_account_to_users

Revision ID: 88dede6b4a54
Revises: af0db7612361
Create Date: 2025-09-26 01:23:21.315375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '88dede6b4a54'
down_revision: Union[str, None] = 'af0db7612361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("account", sa.String(length=255), nullable=True, unique=True)
    )


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("account", sa.String(length=255), nullable=True, unique=True)
    )