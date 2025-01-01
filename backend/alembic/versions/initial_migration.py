"""Initial migration

Revision ID: initial_migration
Create Date: 2024-03-14 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('department', sa.String(), nullable=False),
        sa.Column('office', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_index(op.f('ix_employees_last_name'), 'employees', ['last_name'], unique=False)

    # Create requests table
    op.create_table(
        'requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='new'),
        sa.Column('priority', sa.String(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)

def downgrade() -> None:
    op.drop_table('requests')
    op.drop_table('employees')