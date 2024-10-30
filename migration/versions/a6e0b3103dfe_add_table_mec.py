"""add_table_mec

Revision ID: a6e0b3103dfe
Revises: 9d09e1cb9b76
Create Date: 2024-10-30 08:15:03.113620

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = 'a6e0b3103dfe'
down_revision = '9d09e1cb9b76'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mechanics',
    sa.Column('passport_number', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('full_name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
    sa.Column('experience_years', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('passport_number'),
    schema=settings.POSTGRES_SCHEMA
    )


def downgrade():
    op.drop_table('mechanics', schema=settings.POSTGRES_SCHEMA)
