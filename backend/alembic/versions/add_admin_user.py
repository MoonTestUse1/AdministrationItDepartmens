"""add admin user

Revision ID: add_admin_user
Revises: initial_schema
Create Date: 2024-01-03 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_admin_user'
down_revision = 'initial_schema'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Добавляем админа с id = -1
    op.execute("""
        INSERT INTO employees (id, first_name, last_name, department, office, hashed_password)
        VALUES (-1, 'Admin', 'Admin', 'IT', 'HQ', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYEPFr.6Ja')
        ON CONFLICT (id) DO NOTHING;
    """)

def downgrade() -> None:
    op.execute("DELETE FROM employees WHERE id = -1;") 