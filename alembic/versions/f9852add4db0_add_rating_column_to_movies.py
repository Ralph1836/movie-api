"""add rating column to movies

Revision ID: f9852add4db0
Revises: 3c8a1a2c3237
Create Date: 2025-07-21 19:32:37.467147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'f9852add4db0'
down_revision: Union[str, Sequence[str], None] = '3c8a1a2c3237'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the 'rating' column as a string of length 5, default 'NR' (Not Rated)
    op.add_column('movies', sa.Column('rating', sa.String(length=5), nullable=False, server_default="NR"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('movies', 'rating')
