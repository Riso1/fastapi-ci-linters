"""merge migration heads

Revision ID: ec3c6ac13442
Revises: 302b3d127016, 3479d2730222
Create Date: 2026-06-11 15:03:16.774944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec3c6ac13442'
down_revision: Union[str, Sequence[str], None] = ('302b3d127016', '3479d2730222')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
