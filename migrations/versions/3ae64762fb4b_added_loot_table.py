"""Added Loot Table

Revision ID: 3ae64762fb4b
Revises: 
Create Date: 2021-01-25 22:47:12.808969

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3ae64762fb4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'loot',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('guild_id', sa.String(), nullable=False),
        sa.Column('item', sa.String(), nullable=False),
        sa.Column('belongs_to', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('loot')
