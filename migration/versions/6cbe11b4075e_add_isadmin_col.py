"""add_isadmin_col

Revision ID: 6cbe11b4075e
Revises: 5efaeb747c4c
Create Date: 2024-12-15 22:24:36.374617

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = '6cbe11b4075e'
down_revision = '5efaeb747c4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('false'), nullable=False), schema='my_app_schema')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin', schema='my_app_schema')
    # ### end Alembic commands ###
