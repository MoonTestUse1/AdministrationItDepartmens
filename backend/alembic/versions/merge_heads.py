"""merge heads

Revision ID: merge_heads
Revises: initial_migration, create_tokens_table
Create Date: 2024-01-03 10:52:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'merge_heads'
down_revision = None
branch_labels = None
depends_on = ('initial_migration', 'create_tokens_table')

def upgrade():
    pass

def downgrade():
    pass 