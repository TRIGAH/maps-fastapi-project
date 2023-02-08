"""add foreign key to posts table

Revision ID: 80500dd735a4
Revises: efd9039cb108
Create Date: 2023-02-09 00:33:20.770078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80500dd735a4'
down_revision = 'efd9039cb108'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
