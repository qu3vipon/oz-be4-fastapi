"""add created_at index

Revision ID: f6bee820755e
Revises: f59a558c2a9c
Create Date: 2024-09-30 11:58:37.778315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6bee820755e'
down_revision: Union[str, None] = 'f59a558c2a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_service_user_created_at', 'service_user', ['created_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_service_user_created_at', table_name='service_user')
    # ### end Alembic commands ###
