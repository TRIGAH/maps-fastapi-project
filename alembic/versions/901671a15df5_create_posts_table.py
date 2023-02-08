"""create posts table

Revision ID: 901671a15df5
Revises: 
Create Date: 2023-02-03 00:40:48.312041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '901671a15df5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(),nullable=False,primary_key = True),
     sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
