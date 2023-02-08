"""add last few columns to posts table

Revision ID: fa7a9bce2dee
Revises: 80500dd735a4
Create Date: 2023-02-09 00:45:32.648273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa7a9bce2dee'
down_revision = '80500dd735a4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False, server_default='TRUE'),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()')),)

    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
