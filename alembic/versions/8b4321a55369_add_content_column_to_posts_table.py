"""add Content column to Posts table

Revision ID: 8b4321a55369
Revises: 901671a15df5
Create Date: 2023-02-09 00:04:36.518247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b4321a55369'
down_revision = '901671a15df5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
