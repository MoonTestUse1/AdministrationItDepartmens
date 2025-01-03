"""merge heads

Revision ID: merge_heads_new
Revises: initial_migration, create_tokens_table_new
Create Date: 2024-01-03 20:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'merge_heads_new'
down_revision = None
branch_labels = None
depends_on = ['initial_migration', 'create_tokens_table_new']

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass 