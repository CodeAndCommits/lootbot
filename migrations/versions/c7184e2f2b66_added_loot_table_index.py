"""Added Loot Table Index

Revision ID: c7184e2f2b66
Revises: 3ae64762fb4b
Create Date: 2021-01-26 20:57:42.466519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7184e2f2b66'
down_revision = '3ae64762fb4b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        'idx_guild_id_member_id',
        'loot',
        ['guild_id', 'belongs_to'],
    )


def downgrade():
    op.drop_index(
        'idx_guild_id_member_id',
        'loot',
    )
