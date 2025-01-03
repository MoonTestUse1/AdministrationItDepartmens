"""add created_at column

Revision ID: add_created_at
Revises: add_admin_user
Create Date: 2024-01-03 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_created_at'
down_revision = 'add_admin_user'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Добавляем колонку created_at
    op.add_column('employees',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

def downgrade() -> None:
    op.drop_column('employees', 'created_at') 