"""merge heads

Revision ID: merge_heads
Revises: create_tokens_table
Create Date: 2024-01-03 10:50:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'merge_heads'
down_revision = 'create_tokens_table'
branch_labels = None
depends_on = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass 