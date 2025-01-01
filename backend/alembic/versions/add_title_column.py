"""Add title column to requests table

Revision ID: add_title_column
Create Date: 2024-03-14 13:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_title_column'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add title column to requests table
    op.add_column('requests', sa.Column('title', sa.String(), nullable=False, server_default=''))
    op.alter_column('requests', 'title', nullable=False, server_default=None)

def downgrade() -> None:
    # Remove title column from requests table
    op.drop_column('requests', 'title') 